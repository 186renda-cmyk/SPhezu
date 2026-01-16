import requests
import json

# ================= 配置区域 =================
# 您的域名
HOST = "sphezu.top"
# IndexNow 密钥
KEY = "303e9826bedb4fa986ba635f0d8b8819"
# 密钥文件在网站上的位置
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

# 需要推送到搜索引擎的 URL 列表
# 我们自动包含了首页、隐私页以及 blog 目录下的所有文章
URL_LIST = [
    f"https://{HOST}/",
    f"https://{HOST}/blog/",
    f"https://{HOST}/privacy",
    f"https://{HOST}/blog/spotify-free-vs-premium",
    f"https://{HOST}/blog/spotify-premium-pricing-guide",
    f"https://{HOST}/blog/is-spotify-premium-worth-it",
    f"https://{HOST}/blog/how-to-use-spotify-for-free",
    f"https://{HOST}/blog/spotify-vs-apple-music",
    f"https://{HOST}/blog/how-to-download-spotify-music"
]
# ===========================================

def submit_to_indexnow():
    # IndexNow API 端点 (Bing 和 Yandex 等搜索引擎共享此接口)
    api_endpoint = "https://api.indexnow.org/indexnow"
    
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": URL_LIST
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    print(f"🚀 准备推送 {len(URL_LIST)} 个链接到 IndexNow...")
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
