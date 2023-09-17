import os
from PIL import Image
from wxpy import *
import logging
import CONFIG
from concurrent.futures import ThreadPoolExecutor
from FetchAPI import ChatGPT
from ApS import Img2Text
import time

bot = Bot(cache_path=True)
bot.enable_puid('bot.pkl')

print("TuTu is running...")

# 收到前一条信息的时间
prev_msg_time = None
# 已经处理的任务集合
task_map = []

"""
日志功能
"""
fh = logging.FileHandler('wxpy.log', encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', handlers=[fh])


# 监听并接收好友消息
@bot.register(Friend)
def auto_reply(msg):
    global prev_msg_time
    # 当前消息的时间
    msg_time = int(msg.create_time.timestamp())
    # 当前时间
    current_time = int(time.time())
    # 只处理60秒内的信息
    if current_time - msg_time < 60:
        # 图片消息
        if msg.type == 'Picture':
            user_name = msg.chat.nick_name
            user_puid = msg.sender.puid
            file_name = msg.file_name
            try:
                if file_name not in task_map:
                    task_map.append(file_name)
                    file = msg.get_file()
                    file_path = CONFIG.PICS_DIC + file_name
                    msg.reply("🔍 Observing...")
                    if '.gif' not in file_name:
                        with open(file_path, 'wb', buffering=4096000) as f:
                            f.write(file)
                        print('{}:{} 的图片已保存：{}'.format(user_name, user_puid, file_path))
                        # 验证图片尺寸
                        image = Image.open(file_path)
                        res = Img2Text.Img_Summary(file_path)
                        msg.reply(res)
            except Exception as e:
                print("{}的图片存储过程中发生错误:{}".format(user_name, e))



# 最大线程池数目
thread_pool = ThreadPoolExecutor(max_workers=CONFIG.MAX_LINE)

bot.join()