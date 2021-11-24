# -*- coding: utf-8 -*-
import base64
import requests
import time
from requests import Session


def get_github_file_sha(token, url):
    url = url
    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": "token " + token,
    }
    response = requests.get(url, headers=headers).json()
    if response.get("sha"):
        return response["sha"]
    return ""


def update_github_file(token, url, string):
    url = url
    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": "token " + token,
    }
    data = {
        "content": base64.b64encode(string.encode("utf-8")).decode("utf-8"),
        "message": "update by actions",
        "sha": get_github_file_sha(token, url)
    }
    resp = requests.put(url=url, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"{ url } updated.")
    else:
        print(f"update { url }  failed!")


def get_subscribe_content():
    session = Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                    "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    # 先获取cookie
    session.get("https://feiniaoyun.tk/")
    username = get_username()
    data = {
        "email": f"{username}@gmail.com",
        "password": f"{username}",
        "invite_code": "",
        "email_code": "",
    }
    # 注册
    print(session.post("https://feiniaoyun.tk/api/v1/passport/auth/register", data=data).text)
    # 获取订阅链接
    resp = session.get("https://feiniaoyun.tk/api/v1/user/getSubscribe")
    print(resp.json())
    subscribe_url = resp.json()["data"]["subscribe_url"]
    print("sub url:", subscribe_url)
    resp = session.get(subscribe_url)
    return resp.text


def get_username():
    ts = str(int(time.time()))
    name = ts + "Robot_" + ts[-3:]
    return name


if __name__ == "__main__":
    token = input()
    clash_url = "https://api.github.com/repos/liangguijing/ss/contents/clash"
    content = get_subscribe_content()
    update_github_file(token, clash_url, content)
