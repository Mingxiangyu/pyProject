# -*- codeing = utf-8 -*-
# @Time :2022/11/21 16:05
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  nasa数据下载.py

# !/usr/bin/env python3
#
# A valid .netrc file in the user home ($HOME) directory, or a valid appkey is required.
#
#   Example .netrc:
#    machine urs.earthdata.nasa.gov login USERNAME password PASSWD
#
#   An appkey can be obtained from:
#    https://oceandata.sci.gsfc.nasa.gov/appkey/
#
# from obdaac_download import httpdl
#
# server = 'oceandata.sci.gsfc.nasa.gov'
# request = '/ob/getfile/T2017004001500.L1A_LAC.bz2'
#
# status = httpdl(server, request, uncompress=True)
#
import argparse
import hashlib
import logging
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter

DEFAULT_CHUNK_SIZE = 131072
BLOCKSIZE = 65536

# requests session object used to keep connections around
obpgSession = None


def getSession(verbose=0, ntries=5):
    global obpgSession

    if not obpgSession:
        # turn on debug statements for requests
        if verbose > 1:
            print("Session started")
            logging.basicConfig(level=logging.DEBUG)

        obpgSession = requests.Session()
        obpgSession.mount('https://', HTTPAdapter(max_retries=ntries))

    else:
        if verbose > 1:
            print("Reusing existing session")

    return obpgSession


def isRequestAuthFailure(req):
    ctype = req.headers.get('Content-Type')
    if ctype and ctype.startswith('text/html'):
        if "<title>Earthdata Login</title>" in req.text:
            return True
    return False


def httpdl(server, request, localpath='.', outputfilename=None, ntries=5,
           uncompress=False, timeout=30., verbose=0, force_download=False,
           chunk_size=DEFAULT_CHUNK_SIZE):
    status = 0
    urlStr = 'https://' + server + request

    global obpgSession
    localpath = Path(localpath)
    getSession(verbose=verbose, ntries=ntries)

    modified_since = None
    headers = {}

    if not force_download:
        if outputfilename:
            ofile = localpath / outputfilename
            modified_since = get_file_time(ofile)
        else:
            rpath = Path(request.rstrip())
            if 'requested_files' in request:
                rpath = Path(request.rstrip().split('?')[0])
            ofile = localpath / rpath.name
            if re.search(r'(?<=\?)(\w+)', ofile.name):
                ofile = Path(ofile.name.split('?')[0])

            modified_since = get_file_time(ofile)

        if modified_since:
            headers = {"If-Modified-Since": modified_since.strftime("%a, %d %b %Y %H:%M:%S GMT")}

    with obpgSession.get(urlStr, stream=True, timeout=timeout, headers=headers) as req:

        if req.status_code != 200:
            status = req.status_code
        elif isRequestAuthFailure(req):
            status = 401
        else:
            if not Path.exists(localpath):
                os.umask(0o02)
                Path.mkdir(localpath, mode=0o2775, parents=True)

            if not outputfilename:
                cd = req.headers.get('Content-Disposition')
                if cd:
                    outputfilename = re.findall("filename=(.+)", cd)[0]
                else:
                    outputfilename = urlStr.split('/')[-1]

            ofile = localpath / outputfilename

            # This is here just in case we didn't get a 304 when we should have...
            download = True
            if 'last-modified' in req.headers:
                remote_lmt = req.headers['last-modified']
                remote_ftime = datetime.strptime(remote_lmt, "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=None)
                if modified_since and not force_download:
                    if (remote_ftime - modified_since).total_seconds() < 0:
                        download = False
                        if verbose:
                            print("Skipping download of %s" % outputfilename)

            if download:
                total_length = req.headers.get('content-length')
                length_downloaded = 0
                total_length = int(total_length)
                if verbose > 0:
                    print("Downloading %s (%8.2f MBs)" % (outputfilename, total_length / 1024 / 1024))

                with open(ofile, 'wb') as fd:

                    for chunk in req.iter_content(chunk_size=chunk_size):
                        if chunk:  # filter out keep-alive new chunks
                            length_downloaded += len(chunk)
                            fd.write(chunk)
                            if verbose > 0:
                                percent_done = int(50 * length_downloaded / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * percent_done, ' ' * (50 - percent_done)))
                                sys.stdout.flush()

                if uncompress:
                    if ofile.suffix in {'.Z', '.gz', '.bz2'}:
                        if verbose:
                            print("\nUncompressing {}".format(ofile))
                        compressStatus = uncompressFile(ofile)
                        if compressStatus:
                            status = compressStatus
                else:
                    status = 0

                if verbose:
                    print("\n...Done")

    return status


def uncompressFile(compressed_file):
    """
    uncompress file
    compression methods:
        bzip2
        gzip
        UNIX compress
    """

    compProg = {".gz": "gunzip -f ", ".Z": "gunzip -f ", ".bz2": "bunzip2 -f "}
    exten = Path(compressed_file).suffix
    unzip = compProg[exten]
    p = subprocess.Popen(unzip + str(compressed_file.resolve()), shell=True)
    status = os.waitpid(p.pid, 0)[1]
    if status:
        print("Warning! Unable to decompress %s" % compressed_file)
        return status
    else:
        return 0


def get_file_time(localFile):
    ftime = None
    localFile = Path(localFile)
    if not Path.is_file(localFile):
        while localFile.suffix in {'.Z', '.gz', '.bz2'}:
            localFile = localFile.with_suffix('')

    if Path.is_file(localFile):
        ftime = datetime.fromtimestamp(localFile.stat().st_mtime)

    return ftime


def compare_checksum(filepath, checksum):
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    if hasher.hexdigest() == checksum:
        return False
    else:
        return True


def retrieveURL(request, localpath='.', uncompress=False, verbose=0, force_download=False, appkey=False,
                checksum=False):
    if args.verbose:
        print("Retrieving %s" % request.rstrip())

    server = "oceandata.sci.gsfc.nasa.gov"
    parsedRequest = urlparse(request)
    netpath = parsedRequest.path

    if parsedRequest.netloc:
        server = parsedRequest.netloc
    else:
        if not re.match(".*getfile", netpath):
            netpath = '/ob/getfile/' + netpath

    joiner = '?'
    if (re.match(".*getfile", netpath)) and appkey:
        netpath = netpath + joiner + 'appkey=' + appkey
        joiner = '&'

    if parsedRequest.query:
        netpath = netpath + joiner + parsedRequest.query

    status = httpdl(server, netpath, localpath=localpath, uncompress=uncompress, verbose=verbose,
                    force_download=force_download)

    if checksum and not uncompress:
        cksumURL = 'https://' + server + '/checkdata/' + parsedRequest.path
        dnldfile = localpath / parsedRequest.path
        if compare_checksum(dnldfile, requests.get(cksumURL).text):
            print("The file %s failed checksum test" % parsedRequest.path)
            status = 1

    return status


if __name__ == "__main__":
    # parse command line
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Download files archived at the OB.DAAC',
        epilog=textwrap.dedent('''
Provide one of either filename, --filelist or --http_manifest.

NOTE: For authentication, a valid .netrc file in the user home ($HOME) directory\nor a valid appkey is required.

    Example .netrc:
    machine urs.earthdata.nasa.gov login USERNAME password PASSWD\n

    An appkey can be obtained from:
    https://oceandata.sci.gsfc.nasa.gov/appkey/
'''
                               ))
    parser.add_argument('-v', '--verbose', help='print status messages',
                        action='count', default=0)
    parser.add_argument('filename', nargs='?', help='name of the file (or the URL of the file) to retreive')
    parser.add_argument('--filelist',
                        help='file containing list of filenames to retreive, one per line')
    parser.add_argument('--http_manifest',
                        help='URL to http_manifest file for OB.DAAC data order')
    parser.add_argument('--odir',
                        help='full path to desired output directory; \ndefaults to current working directory: %s' % Path.cwd(),
                        default=Path.cwd())
    parser.add_argument('--uncompress', action="store_true",
                        help='uncompress the retrieved files (if compressed)',
                        default=False)
    parser.add_argument('--checksum', action="store_true",
                        help='compare retrieved file checksum; cannot be used with --uncompress',
                        default=False)
    parser.add_argument('--failed', help='filename to contain list of files that failed to be retrieved')
    parser.add_argument('--appkey', help='value of the users application key')
    parser.add_argument('--force', action='store_true',
                        help='force download even if file already exists locally',
                        default=False)
    args = parser.parse_args()

    filelist = []

    if args.http_manifest:
        status = retrieveURL(args.http_manifest, verbose=args.verbose, force_download=True, appkey=args.appkey)
        if status:
            print("There was a problem retrieving %s (received status %d)" % (args.http_manifest, status))
            sys.exit("Bailing out...")
        else:
            with open('http_manifest.txt') as flist:
                for filename in flist:
                    filelist.append(filename.rstrip())
    elif args.filename:
        filelist.append(args.filename)
    elif args.filelist:
        with open(os.path.expandvars(args.filelist)) as flist:
            for filename in flist:
                filelist.append(os.path.expandvars(filename.rstrip()))

    if not len(filelist):
        parser.print_usage()
        sys.exit("Please provide a filename (or list file) to retrieve")

    if args.uncompress and args.checksum:
        parser.print_usage()
        sys.exit("--uncompress is incompatible with --checksum")

    outpath = Path.resolve(Path.expanduser(Path(os.path.expandvars(args.odir))))

    if args.verbose:
        print("Output directory: %s" % outpath)

    failed = None
    if args.failed:
        failed = open(args.failed, 'w')

    for request in filelist:
        status = retrieveURL(request, localpath=outpath, uncompress=args.uncompress,
                             verbose=args.verbose, force_download=args.force,
                             appkey=args.appkey, checksum=args.checksum)
        if status:
            if status == 304:
                if args.verbose:
                    print("%s is not newer than local copy, skipping download" % request)
            else:
                print("There was a problem retrieving %s (received status %d)" % (request, status))
                if failed:
                    failed.write(request)
                    failed.write("\n")

    if failed:
        failed.close()
