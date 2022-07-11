import cpca


def 简单():
    location_str = [
        "广东省深圳市福田区巴丁街深南中路1025号新城大厦1层",
        "特斯拉上海超级工厂是特斯拉汽车首座美国本土以外的超级工厂，位于中华人民共和国上海市。",
        "三星堆遗址位于中国四川省广汉市城西三星堆镇的鸭子河畔，属青铜时代文化遗址"
    ]
    # df = cpca.transform(location_str)
    # 想获知程序是从字符串的那个位置提取出省市区名的，可以添加一个 pos_sensitive=True
    df = cpca.transform(location_str, pos_sensitive=True)
    print(df)


def 大段文字():
    long_text = "对一个城市的评价总会包含个人的感情。如果你喜欢一个城市，很有可能是喜欢彼时彼地的自己。" \
                "在广州、香港读过书，工作过，在深圳买过房、短暂生活过，去北京出了几次差。" \
                "想重点比较一下广州、深圳和香港，顺带说一下北京。总的来说，觉得广州舒适、" \
                "香港精致、深圳年轻气氛好、北京大气又粗糙。答主目前选择了广州。"

    df = cpca.transform_text_with_addrs(long_text)
    # df = cpca.transform_text_with_addrs(long_text, pos_sensitive=True)
    print(df)

# 主程序接口
if __name__ == '__main__':
    大段文字()