import time
import json
import hashlib
import random
import requests
import CONFIG
import base64


secret_id = CONFIG.SECRET_ID  # 密钥信息
secret_key = CONFIG.SECRET_KEY  # 密钥信息


def img2text(img_path):
    # 将图片转换为Base64字符串
    with open(img_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    # 签名对象
    getSha256 = lambda content: hashlib.sha256(content.encode("utf-8")).hexdigest()
    application_name = 'sdtagger'  # 应用名称
    api_name = 'tagger'  # 接口名称

    # 请求地址
    url = "https://api.aigcaas.cn/v2/application/%s/api/%s" % (application_name, api_name)
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
    # 构建请求 body
    data = {
        "model": "wd14-vit-v2-git",
        "image": "data:image/png;base64," + str(base64_image)
    }

    # 获取响应
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    request_id = response.headers["Aigcaas-Request-Id"]
    # 任务开始时间
    start_time = time.time()
    while True:
        time.sleep(3)
        if time.time() - start_time > 300:  # 如果时间超过5分钟
            print("Failed to Image2Text within 5 minutes.")
            break
        url = "https://api.aigcaas.cn/v2/async"
        # 构建请求头
        nonce = str(random.randint(1, 10000))
        timestamp = str(int(time.time()))
        token = getSha256(("%s%s%s" % (timestamp, secret_key, nonce)))
        headers = {
            'SecretID': secret_id,
            'RequestID': request_id,
            'Nonce': nonce,
            'Token': token,
            'Timestamp': timestamp,
            'Content-Type': 'application/json'
        }
        async_response = requests.request("GET", url, headers=headers, data=json.dumps(data))
        print(async_response.status_code, async_response.content)
        if async_response.status_code != 202:
            # 如果是413则直接失败
            if async_response.status_code == 413:
                print("程序出现异常:{}".format(async_response.content))
            response_content = json.loads(async_response.content)
            # print(response_content)
            tags = response_content["tags"]
            sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
            top_25_keys = [item[0] for item in sorted_tags[:25]]
            prompts = ', '.join(str(x) for x in top_25_keys)
            # print(prompts)
            return prompts
            break

if __name__ == '__main__':
    prompts = img2text("/Users/joseph/Desktop/TuTu/PICS/1.png")
    print(prompts)