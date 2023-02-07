# -*- codeing = utf-8 -*-
# @Time :2023/2/7 9:52
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  解析浏览器的请求头信息.py
from curl2py.curlParseTool import curlCmdGenPyScript

curl_cmd = """curl "https://fanyi.baidu.com/mtpe/user/getInfo?_=1675734753701" ^
  -H "Accept: */*" ^
  -H "Accept-Language: zh-CN,zh;q=0.9,sq;q=0.8,is;q=0.7" ^
  -H "Connection: keep-alive" ^
  -H "Cookie: BIDUPSID=C040D3FD4929760F23AC59449DEEA0DC; PSTM=1650424457; BDUSS=h6VXlHNWpsRE5wTWo5amwzMGZlWlVTczRQdFRBY09XNThvT3U1QUtBazVEcGRpRVFBQUFBJCQAAAAAAAAAAAEAAABVyeE~U3RhcmVfQm95AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmBb2I5gW9iRz; BDUSS_BFESS=h6VXlHNWpsRE5wTWo5amwzMGZlWlVTczRQdFRBY09XNThvT3U1QUtBazVEcGRpRVFBQUFBJCQAAAAAAAAAAAEAAABVyeE~U3RhcmVfQm95AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmBb2I5gW9iRz; FANYI_WORD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=C040D3FD4929760F03137EE68F3E9AB9:SL=0:NR=10:FG=1; APPGUIDE_10_0_2=1; MCITY=-^%^3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=848k2ka1058ka12g810g84ss1hu1cjl1l; BAIDUID_BFESS=C040D3FD4929760F03137EE68F3E9AB9:SL=0:NR=10:FG=1; ZFY=RsG20i:Ar3qX2F712yVZoS6qB3tFYgTT3z97MQADmdEE:C; BAIDU_WISE_UID=wapp_1675670175456_827; __bid_n=185fc1c665914951504207; arialoadData=false; FPTOKEN=/MyhbxpkKZDAS2Kc3IwEXE0SJUo3VAqTC+YNHd145D9v8mneEtFarTiXonWP92saQKapUc3bTFXbCf2OMhZvcHXxhd+QzXcXJo5vdpyUTPm3oo7f0zLkqzH2CzrzoZQ2iQyV0pyOSbfmxaqORuPr11qrO+4v+MAqKDS6AQ6J3pmVMcBQj6cp8DCSS9neIN9Dr9T9TgemlKAtvfoRTCuuX3Qli6+rIVuu5bf8n7pcVrCmlzUkxQVJej5TDEIONiYHPJC5gDxnSBZhYeJp2kuzaLaQExJsjmE8SUOMqURFGij46urcs4IzlelQJK5+NXNwIpKfAEiafnp7Em7x9qMBzKmiRKQ7XnbUt0UZjilVno9TUUghvQi0Dm1j9k4aJQFrjrlIq8uxXwMcVxpTzA/dgWtV6eywyAnXNj29QqyuL95/Ps6a44eMV1K9UhaT79Lb^|u3nFefLmsaessbrrsJHcpxAKmXkUUrlJb+1DOls48/s=^|10^|042046ddce107a7a5c8d278d06ef5dc0; ariaDefaultTheme=undefined; RT=^\^"z=1&dm=baidu.com&si=e01f4166-76a0-4738-a437-32589a5d2f39&ss=ldsnqsj9&sl=0&tt=0&bcn=https^%^3A^%^2F^%^2Ffclog.baidu.com^%^2Flog^%^2Fweirwood^%^3Ftype^%^3Dperf&ul=hth&hd=hu0^\^"; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1673936276,1674220129,1675045659,1675734750; ab_sr=1.0.1_MTM5MjQ5YTViZmRlZjZlNDJmYzNmNGJhMTJhM2ZmMmQ5NmM1NDAzM2QwNjg1MWU0YmU4ZWI5NTZjYTE4YmQyNmFkOGI5YWE5NDcxNzY3YzQ0ZWE0NzE1MzkyYTgxZDdjMWNkNWMzNTAzMmEyMzY4MGYxNTZhMTAyZWMyMmIyZmM3NGE3ZWEwMGEwYTQ5Nzc0MzdkNWRjNzZiZmExMDUxM2M0NDE1MDY3Nzk2ZTYyNTM1Njk3ZTczYzRjNTkzYzI4; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1675734754" ^
  -H "Referer: https://fanyi.baidu.com/" ^
  -H "Sec-Fetch-Dest: empty" ^
  -H "Sec-Fetch-Mode: cors" ^
  -H "Sec-Fetch-Site: same-origin" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36" ^
  -H "sec-ch-ua: ^\^" Not A;Brand^\^";v=^\^"99^\^", ^\^"Chromium^\^";v=^\^"100^\^", ^\^"Google Chrome^\^";v=^\^"100^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  --compressed"""

output = curlCmdGenPyScript(curl_cmd)
print(output)
