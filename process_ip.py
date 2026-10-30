import time
import requests

# 定义需要抓取的网址及其对应的专属注释
TARGETS = [
    {
        "url": "https://ip.ehb.cc.cd/all",
        "comment": "流光全域 · IPv4 诸源融合"
    },
    {
        "url": "https://ip.ehb.cc.cd/cm",
        "comment": "中国移动 · 极速聚合 (IPv4)"
    },
    {
        "url": "https://ip.ehb.cc.cd/ct",
        "comment": "中国电信 · 稳健美西 (IPv4)"
    },
    {
        "url": "https://ip.ehb.cc.cd/cu",
        "comment": "中国联通 · 满速天花板 (IPv4)"
    },
    {
        "url": "https://ip.ehb.cc.cd/104",
        "comment": "104.16.0.0/13 官方大分类全域池"
    },
    {
        "url": "https://ip.ehb.cc.cd/104.17",
        "comment": "104.17 移动起飞段"
    },
    {
        "url": "https://ip.ehb.cc.cd/104.19",
        "comment": "104.19 移动防 QoS 段"
    },
    {
        "url": "https://ip.ehb.cc.cd/104.16",
        "comment": "104.16 经典老牌段"
    },
    {
        "url": "https://ip.ehb.cc.cd/162",
        "comment": "162.158.0.0/15 官方大分类全域池"
    },
    {
        "url": "https://ip.ehb.cc.cd/162.159-saas",
        "comment": "162.159 SaaS / DoH 高优段"
    },
    {
        "url": "https://ip.ehb.cc.cd/162.159-ct",
        "comment": "162.159 电信美西最稳段"
    },
    {
        "url": "https://ip.ehb.cc.cd/172",
        "comment": "172.64.0.0/13 官方大分类全域池"
    },
    {
        "url": "https://ip.ehb.cc.cd/172.64",
        "comment": "172.64 联通/电信主力段"
    },
    {
        "url": "https://ip.ehb.cc.cd/172.67",
        "comment": "172.67 动态反代段"
    },
    {
        "url": "https://ip.ehb.cc.cd/198",
        "comment": "198.41.128.0/17 联通天花板大段"
    },
    {
        "url": "https://ip.ehb.cc.cd/108",
        "comment": "108.162.192.0/18 三网通用兜底大段"
    }
]

def fetch_ips_from_url(url):
    """从指定网址获取 IP 列表"""
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
    print("▶ 开始依序抓取并合并所有线路的 IP 数据...")

    for target in TARGETS:
        url = target["url"]
        comment = target["comment"]
        print(f"正在处理: {comment} ({url})")
        
        raw_lines = fetch_ips_from_url(url)
        if not raw_lines:
            continue

        for item in raw_lines:
            # 清洗提取纯 IP 地址（兼容原本带端口或带旧注释的行）
            clean_ip = item.split("#")[0].split(":")[0].strip()
            if clean_ip:
                # 拼接成要求的格式：IP:443#对应注释
                formatted_line = f"{clean_ip}:443#{comment}"
                all_result_lines.append(formatted_line)

        # 稍微停顿，对服务器友好
        time.sleep(0.3)

    # 去重（可选：如果不同链接有重复 IP，可以保持整洁。不清空则注释：这里不清空以保留各自原汁原味）
    # 写入 output.txt
    output_filename = "output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(all_result_lines) + "\n")
    
    print(f"🎉 合并完成！已生成 {output_filename}，总计合并了 {len(all_result_lines)} 行 IP 数据。")

if __name__ == "__main__":
    main()
