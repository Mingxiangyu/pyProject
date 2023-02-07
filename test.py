# -*- codeing = utf-8 -*-
# @Time :2022/7/17 18:42
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  test.py
# Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions
import feapder


class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self):
        url = "https://www.zhihu.com/api/v4/me"
        params = {
            "include": "email,account_status,is_bind_phone,url_token,is_realname,is_destroy_waiting"
        }
        yield feapder.Request(url, params=params, method="GET")

    def download_midware(self, request):
        request.headers = {
            "authority": "www.zhihu.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,sq;q=0.8,is;q=0.7",
            "origin": "https://zhuanlan.zhihu.com",
            "referer": "https://zhuanlan.zhihu.com/p/585452696",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "x-ab-param": "",
            "x-ab-pb": "CmQIABsAPwBHALQAaQFqAXQBOwLMAtcC2AK3A9YEEQVRBYsFjAWeBTAGMQbrBicHdAh2CHkIPwlgCfQJBApJCmUKawq+Cv4KQwtxC4cLjQvXC+AL5QvmCzgMcQyPDKwMwwzJDPgMEjICAAAAAAIBAAAAAAAABAABAAABAAEAAAABBgABAwAAAAAAAAEAAAUCAAAAAgYAAAAAAA==",
            "x-requested-with": "fetch",
            "x-zse-93": "101_3_3.0",
            "x-zse-96": "2.0_1m3/a6k=c8cO3WIH/+F91Z36RH9IHWb+WkR+ShjHU3vMYUjXG4JufoVjaTzJNpIz"
        }
        request.cookies = {
            "_zap": "89550b50-2368-47fc-b479-9db802f3a60a",
            "d_c0": "\"ALDQuQVW0RSPTjbKSbGsb3pb8U3m7wXZsEs=|1650425686\"",
            "_xsrf": "qp5Wkg5iemAGT4zzQasYyBd2lfsEAkUc",
            "YD00517437729195%3AWM_NI": "BF2zIROz69GkktbGTfTWF9yMU2INrwpzWyINX1ZFQ4aEsNK%2Fd4GPrjFOFQmfVhxvhPPlYlHgZ97GuiDZIRfU9qHEP1MW5fi0qO%2B5iFekSKpmWeME5brs%2FZ43VV2Jp9%2BDc1k%3D",
            "YD00517437729195%3AWM_NIKE": "9ca17ae2e6ffcda170e2e6ee9ad467a29ba5d0aa66ed9e8bb3c85a878e8f82d1439cb7fab5d64d90b387b4c62af0fea7c3b92a829afe9bcc5a8da6fadac661a9acaea8d76e98898adafc4797ee87aff17db4a6999acc469cef96a7d440a39bbdafca25a8ec89b1f16286918ab2f06e96b8b897eb5c94b4978dcb6d9ae7f9a8f863888687b3e55ffbaf88a6d33b8f89fb87ec3cb391e5d6ec4ea7b59dacf36795bb83a6b86ab2ade1bbb739968afeabf333e99cadd2ea37e2a3",
            "YD00517437729195%3AWM_TID": "r6oXnvaiQG1EBAFQVAbBNX37WHXK2ZXD",
            "q_c1": "775f48034ee94617acb42c0a56672ccc|1669112138000|1669112138000",
            "ISSW": "1",
            "z_c0": "2|1:0|10:1675068402|4:z_c0|80:MS4xTzc4T0F3QUFBQUFtQUFBQVlBSlZUZkxSeEdSVy1qNFRrWGthdlFkQlR1OXN4T3RTNFFKTVFRPT0=|97d808aa1dfa81913c33c55e4e758fcaa9fdc08f958964997529819fc76f112a",
            "tst": "r",
            "arialoadData": "false",
            "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49": "1675142806,1675411916,1675663793,1675735022",
            "Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49": "1675735508",
            "KLBRSID": "2177cbf908056c6654e972f5ddc96dc2|1675735508|1675735022"
        }
        return request

    def parse(self, request, response):
        print(response.text)
        print(response)


if __name__ == "__main__":
    AirSpiderDemo(thread_count=1).start()

