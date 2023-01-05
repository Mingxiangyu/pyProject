# # -*- codeing = utf-8 -*-
# # @Time :2022/7/17 18:42
# # @Author :xming
# # @Version :1.0
# # @Descriptioon :
# # @File :  test.py
#
# # 字典存储无序的数据
# name_map = {"name": "ljf", "age": 18, "price": 2.5};
# print(name_map);
# # 查询
# print(name_map["name"]);
# # 修改
# name_map["age"] = 19;
# print(name_map)
# # 添加
# name_map["adress"] = "beijing";
# print(name_map)
# # 删除
# name_map.pop("adress");
# print(name_map)
# # 统计字符串个数
# print(len(name_map))
# # 合并字典,合并时已经存在某个键值对，后者覆盖前者
# temp_map = {"address": "背景"}
# name_map.update(temp_map);
# print(name_map)
# # 遍历
# for m in name_map:
#     print("遍历:%s" % {m, name_map[m]});
# # 列表中存储字典，列表中存储多个字典
# name_list = [{"name": "beijing", "adCode": 110100}, {"name": "tianjing", "adCode": 234000},
#              {"name": "shanghai", "adCode": 45600}]
# for k in name_list:
#     print(k)
#
import json

json_data = """{
"favourite":{
"bkmrk":{
"id1490843709594066":{
"guid":"904eff52277f403b89f6410fe2758646.11",
"lcate":"1"
},
"id1490843712805183":{
"guid":"58457f60eca64025bc43a978f9c98345.16",
"lcate":"2"
},
"id149084371467327":{
"guid":"a0f907f9dc8b40f689b083f3eba7228b.16",
"lcate":"3"
},
"id1490843716295393":{
"guid":"eb75d929455e468bb712e7bc2025d11a.16",
"lcate":"4"
}
}
}
}"""

data = json.loads(json_data)
for v in data['favourite']['bkmrk'].values():
    print("%s;%s" % (v['lcate'], v['guid']))
