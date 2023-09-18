# Trickle-On-WeChat
在微信端使用类似Trickle的图片信息识别和提炼，并进行图片信息管理的功能。
> 思路介绍：https://mp.weixin.qq.com/s/Q9ubSQHhEgpn2Yf6ndoi5w

## 功能演示：



https://github.com/PromptExpert/Trickle-On-WeChat/assets/46588426/40c83e2e-66ab-474b-a464-878b3e63a4df




图片识别自动提取关键信息
![image](https://github.com/PromptExpert/Trickle-On-WeChat/assets/46588426/d6b01120-0921-4dad-a8d9-245e2c55e7ed)

利用微信聊天记录关键词搜索定位关键信息：
![image](https://github.com/PromptExpert/Trickle-On-WeChat/assets/46588426/b5a7c8a9-d89d-4a7a-9506-14b2e454b071)

## 语言支持
Python

## 环境支持
MacOs、Windows、Linux

## 使用说明
⚠️ Python环境请务必保持在 3.6.x-3.7.x 版本，我使用的是3.7.0（惨痛教训：wxpy对Python的版本有要求）

- Step1:解压下载当前项目，并安装相关Python依赖
- Step2:根据Config中的信息，配置语言模型的Key、配置图像识别及OCR的Key
- Step3:运行Robot.py主程序
- Step4:程序启动后，通过手机扫描二维码的方式进行登录（若失败请反复扫描）

## 主要是用的wxpy库，中文文档（已停更）
该库的核心使用的是itchat，是通过网页扫码的方式登陆微信。
```
https://wxpy.readthedocs.io/zh/latest/
```
