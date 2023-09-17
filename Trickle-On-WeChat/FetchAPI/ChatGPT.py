import requests
import datetime
import CONFIG


def GPT3_5(sys_prompt=None, user_msg=None, user_name=None, user_puid=None):
    current_contents = [{"role": "system", "content": sys_prompt},
                        {"role": "user", "content": user_msg}]
    # 当前时间
    now_time = datetime.datetime.now()
    # 格式化输出时间
    format_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CONFIG.API_KEY
    }
    post_dict = {
        "model": "gpt-3.5-turbo-16k",
        "temperature": 0.8,
        "max_tokens": 600,
        "stream": False,
        "messages": current_contents
    }
    try:
        response = requests.post("https://frostsnowjh.com/v1/chat/completions", json=post_dict, headers=header)
        if 'error' in response.json() or '504' in response:
            print(response.content)
            return "error"
        message = response.json()["choices"][0]["message"]
        if 'content' in message:
            content = message["content"]
            return content
        else:
            return -1
    except Exception as e:
        print(e)



if __name__ == '__main__':
    sys_prompt = ""
    user_msg = "一条蜿蜒的小溪"
    result = GPT3_5(sys_prompt,user_msg)
    print(result)