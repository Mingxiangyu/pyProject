import chardet

path = r'/Users/ming/Downloads/AFG_rrd/igsg0070.22i.Z'
f = open(path, 'rb')
data = f.read()
print(chardet.detect(data))
{'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
