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

def fetch_content_with_comments(url):
    """从指定网址获取内容，保留每行的原始 IP 和注释"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        valid_lines = []
        for line in response.text.splitlines():
            line = line.strip()
            # 过滤空行或非有效数据行
            if not line:
                continue
            valid_lines.append(line)
                
        return valid_lines
    except Exception as e:
        print(f"❌ 获取链接 {url} 失败: {e}")
        return []

def main():
    all_result_lines = []
    print("▶ 开始严格按分类顺序抓取（保留原始内容和注释）...")

    for target in TARGETS:
        name = target["name"]
        url = target["url"]
        print(f"正在处理: {name} -> {url}")
        
        raw_lines = fetch_content_with_comments(url)
        if not raw_lines:
            print(f"⚠️ 警告: {name} 未获取到有效数据。")
            continue

        # 严格按顺序追加该分类下的所有带注释的内容
        all_result_lines.extend(raw_lines)
        print(f"✅ {name} 处理完成，收录 {len(raw_lines)} 行。")

        # 稍微停顿，对服务器友好
        time.sleep(0.3)

    # 写入 wuya.txt（覆盖写入）
    output_filename = "wuya.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(all_result_lines) + "\n")
    
    print(f"\n🎉 全部完成！已生成 {output_filename}，总计合并了 {len(all_result_lines)} 行带注释的数据。")

if __name__ == "__main__":
    main()
