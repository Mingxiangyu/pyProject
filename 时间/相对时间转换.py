from sinan import Sinan

obj = Sinan('明天晚上八点提十公斤的礼物，徒步往西走两公里，原地等待三个小时，如果发 现温度低于十六度，就给我打电话，我的手机号是：16758493028')
result = obj.parse()
print(result)
