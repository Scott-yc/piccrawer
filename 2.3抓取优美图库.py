#1思路 先拿到网页源代码，然后提取子页面链接 href
#2 通过href 拿到子页面的内容 再从子页面找到图片的下载地址 img-》src
#3 下载图片

import requests
from bs4 import BeautifulSoup
import re
url = "https://www.umei.cc/gaoxiaotupian"
resp = requests.get(url)
resp.encoding = "utf-8" #处理乱码

#把源代码交给bs
main_page = BeautifulSoup(resp.text,"html.parser")
alist = main_page.find("div",class_="Clbc_top").find_all("a") #缩小范围找到相应需要的图片模块
# 正则表达式：筛选出包含 <img> 标签的 <a> 标签
for a in alist:
    # 使用正则表达式判断 <a> 标签内是否包含 <img> 标签
    if re.search(r'<img', str(a), re.IGNORECASE):  # 忽略大小写匹配
        href = "https://www.umei.cc" + a.get("href")  # 提取 href
        #拿到子页面的源码
        child_page_resp = requests.get(href)
        child_page_resp.encoding= "utf-8"
        child_page_text = child_page_resp.text
        #从子页面拿到下载地址
        child_page = BeautifulSoup(child_page_text, "html.parser")

        # 从子页面中查找带有 class="lazy" 的 <img> 标签
        img_tag = child_page.find("img", class_="lazy")

        if img_tag:
            # 提取图片下载地址，优先使用 data-original
            img_url = img_tag.get("data-original") or img_tag.get("src")

            # 检查图片是否为 .gif 格式，过滤掉 .gif 图片
            if not img_url.endswith(".gif"):
                print(f"real_image_address: {img_url}")






