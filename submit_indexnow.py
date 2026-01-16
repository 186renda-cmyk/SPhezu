import requests
import json
import xml.etree.ElementTree as ET
import os

# ================= 配置区域 =================
# 您的域名
HOST = "sphezu.top"
# IndexNow 密钥
KEY = "303e9826bedb4fa986ba635f0d8b8819"
# 密钥文件在网站上的位置
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
# Sitemap 文件路径
SITEMAP_PATH = "sitemap.xml"

# ===========================================

def get_urls_from_sitemap(sitemap_path):
    """
    从 sitemap.xml 文件中提取所有 URL
    """
    if not os.path.exists(sitemap_path):
        print(f"❌ 错误: 找不到 Sitemap 文件: {sitemap_path}")
        return []

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Sitemap XML 命名空间
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = []
        for url in root.findall('ns:url', namespace):
            loc = url.find('ns:loc', namespace)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
        
        print(f"📄 从 Sitemap 中提取到 {len(urls)} 个 URL")
        return urls
    except Exception as e:
        print(f"❌ 解析 Sitemap 失败: {str(e)}")
        return []

def submit_to_indexnow():
    # 获取 URL 列表
    url_list = get_urls_from_sitemap(SITEMAP_PATH)
    
    if not url_list:
        print("⚠️ 没有找到可提交的 URL，脚本终止。")
        return

    # IndexNow API 端点 (Bing 和 Yandex 等搜索引擎共享此接口)
    api_endpoint = "https://api.indexnow.org/indexnow"
    
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    print(f"🚀 准备推送 {len(url_list)} 个链接到 IndexNow...")
    print(f"📍 密钥位置: {KEY_LOCATION}")
    
    try:
        response = requests.post(api_endpoint, data=json.dumps(payload), headers=headers, timeout=10)
        
        # 200 OK 或 202 Accepted 都表示成功
        if response.status_code in [200, 202]:
            print("\n✅ 推送成功！")
            print("搜索引擎已接收您的 URL 更新请求。")
            print("注意：实际索引生效可能需要几天时间。")
        else:
            print(f"\n❌ 推送失败。")
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        print("请检查您的网络连接是否正常。")

if __name__ == "__main__":
    submit_to_indexnow()
