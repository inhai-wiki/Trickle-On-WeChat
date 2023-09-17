from AIGCaaS import PaddleOCR,resnest101
from FetchAPI import ChatGPT
import base64

def Img_Summary(img_path):
    try:
        print("正在执行图片解析任务...")
        # 将图片转换为Base64字符串
        with open(img_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")
        text = PaddleOCR.Img_To_Text(image_base64 = base64_image)
        # print(text)
        desc = resnest101.describe(image_base64 = base64_image)
        # print(desc)

        sys_prompt = """
            - 你会将图片通过OCR后的文本信息整合总结，请一步一步思考，你会挖掘不同单词和信息之间的联系，
            你会用各种信息分析方法（如：统计、聚类...等）完成信息整理任务，翻译成中文回复。
            - 输出格式：
              "
              # 标题
              {填充信息：通过一句话概括成标题，不超过15字}
              
              # 概要
              {填充信息：通过一句话描述整体内容，不超过30字}
            
              {填充信息：分点显示，整合信息后总结，最多不超过8点，每条信息不超过20字，保留关键值，如人名、地名...}
              
              # 标签
              {填充信息：为该信息3-5个分类标签，例如：#科学、#艺术、#文学、#科技}
              "
        """
        try:
            print("正在执行图片总结任务...")
            user_msg = "这张图是{},图中文字信息：{}".format(desc,text)
            summary  = ChatGPT.GPT3_5(sys_prompt = sys_prompt,user_msg = user_msg)
            if summary == -1:
                return "我已经睡了，别喊我起来!"
            else:
                return summary
        except Exception as e:
            print("ChatGPT总结任务失败:{}".format(e))
            return -1
    except:
        return -1

if __name__ == '__main__':
    res = Img_Summary("/Users/joseph/Desktop/TuTu/PICS/230914-214529.png")
    print(res)