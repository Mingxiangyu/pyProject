import requests

pt_key="AAJjBDhuADDZ8yENaKxZKpGtZ_dF6eK5pz_CSw7GZnl6F6C2a3YOo1gQ7-0uBb3wXsfPlt8PO0M"
pt_pin="jd_5aaad450dceeb"
cookie="pt_key={}; pt_pin={}".format(pt_key, pt_pin)
url = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld";
headers = {
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
    "Cookie": cookie
}
response = requests.post(url=url, headers=headers)
print(response.text)