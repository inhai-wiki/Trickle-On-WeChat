import time
import json
import hashlib
import random
import requests
import CONFIG

secret_id = CONFIG.SECRET_ID  # 密钥信息
secret_key = CONFIG.SECRET_KEY  # 密钥信息

def describe(image_url = None,image_base64 = None):
    # 签名对象
    getSha256 = lambda content: hashlib.sha256(content.encode("utf-8")).hexdigest()

    # 请求地址
    url = "https://api.aigcaas.cn/v3/application/image_recognition/action/resnest101"
    # 构建请求头
    nonce = str(random.randint(1, 10000))
    timestamp = str(int(time.time()))
    token = getSha256(("%s%s%s" % (timestamp, secret_key, nonce)))
    headers = {
        'SecretID': secret_id,
        'Nonce': nonce,
        'Token': token,
        'Timestamp': timestamp,
        'Content-Type': 'application/json'
    }

    # 构建请求 body，可以自行根据上面的内容，添加更多参数
    data = {
        "image_url":image_url,
        "image_base64":image_base64,
    }

    # 获取响应
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    # print(response_dict)
    if "error" in response_dict:
        return -1
    elif response_dict['status'] == 'Success':
        res_msg = response_dict["data"]["labels"]
        return res_msg
    else:
        return -1

if __name__ == '__main__':
    res = describe(image_url = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg.alicdn.com%2Fi4%2F1620781558%2FO1CN01n5ye621NNbcxW0FZB_%21%211620781558.jpg&refer=http%3A%2F%2Fimg.alicdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1697287866&t=821b97b3cdaef29c00872a10e1f0e050")
    print(res)