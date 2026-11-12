import time
import requests

# 定义需要抓取的网址列表
TARGETS = [
    "https://776771.xyz/hk.txt",
    "https://776771.xyz/tw.txt",
    "https://776771.xyz/jp.txt",
    "https://776771.xyz/kr.txt",
    "https://776771.xyz/us.txt",
    "https://776771.xyz/sg.txt"
]

def fetch_content_from_url(url):
    """从指定网址获取原始内容"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        # 按行切分，过滤空白行
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"❌ 获取链接 {url} 失败: {e}")
        return []

def main():
    all_result_lines = []
    print("▶ 开始依序抓取并合并所有网址的内容...")

    for url in TARGETS:
        print(f"正在处理: {url}")
        
        raw_lines = fetch_content_from_url(url)
        if not raw_lines:
            continue

        for item in raw_lines:
            if item:
                all_result_lines.append(item)

        # 稍微停顿，对服务器友好
        time.sleep(0.3)

    # 写入 wuya.txt
    output_filename = "wuya.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(all_result_lines) + "\n")
    
    print(f"🎉 合并完成！已生成 {output_filename}，总计合并了 {len(all_result_lines)} 行数据。")

if __name__ == "__main__":
    main()
