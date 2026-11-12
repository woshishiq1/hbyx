import time
import requests

# 严格按此顺序：香港 -> 台湾 -> 日本 -> 韩国 -> 美国 -> 新加坡
TARGETS = [
    {"name": "香港 (HK)", "url": "https://776771.xyz/hk.txt"},
    {"name": "台湾 (TW)", "url": "https://776771.xyz/tw.txt"},
    {"name": "日本 (JP)", "url": "https://776771.xyz/jp.txt"},
    {"name": "韩国 (KR)", "url": "https://776771.xyz/kr.txt"},
    {"name": "美国 (US)", "url": "https://776771.xyz/us.txt"},
    {"name": "新加坡 (SG)", "url": "https://776771.xyz/sg.txt"}
]

def fetch_content_from_url(url):
    """从指定网址获取原始内容并按原样返回行列表"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        # 按行切分，过滤空白行，严格保持网站内的原有先后顺序
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"❌ 获取链接 {url} 失败: {e}")
        return []

def main():
    all_result_lines = []
    print("▶ 开始严格按顺序抓取并合并各地区内容...")

    for target in TARGETS:
        name = target["name"]
        url = target["url"]
        print(f"正在处理: {name} -> {url}")
        
        raw_lines = fetch_content_from_url(url)
        if not raw_lines:
            print(f"⚠️ 警告: {name} 未获取到任何数据或请求失败。")
            continue

        # 依次追加到总列表中，确保顺序：HK -> TW -> JP -> KR -> US -> SG
        for item in raw_lines:
            if item:
                all_result_lines.append(item)

        print(f"✅ {name} 抓取成功，获取到 {len(raw_lines)} 行数据。")
        # 稍微停顿，对服务器友好
        time.sleep(0.3)

    # 写入 wuya.txt（覆盖写入，确保不会残留旧数据）
    output_filename = "wuya.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(all_result_lines) + "\n")
    
    print(f"\n🎉 全部完成！已生成 {output_filename}，总计合并了 {len(all_result_lines)} 行数据。")

if __name__ == "__main__":
    main()
