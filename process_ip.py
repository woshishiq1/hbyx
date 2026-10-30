import time
import requests

IP_URL = "https://ip.ehb.cc.cd/198"
GEOIP_API_URL = "https://api.ip.sb/geoip/{}"

def get_ip_list():
    """从目标 URL 获取 IP 列表"""
    print(f"▶ 正在从 {IP_URL} 获取 IP 列表...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(IP_URL, headers=headers, timeout=15)
        response.raise_for_status()
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"❌ 获取 IP 列表失败: {e}")
        return []

def main():
    raw_ips = get_ip_list()
    if not raw_ips:
        print("⚠️ 未读取到有效 IP 数据，程序终止。")
        return

    result_lines = []
    print(f"▶ 共获取到 {len(raw_ips)} 条数据，开始通过 api.ip.sb 查询归属地...")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for index, item in enumerate(raw_ips, 1):
        # 提取纯 IP
        clean_ip = item.split("#")[0].split(":")[0].strip()
        location = "未知地区"

        if clean_ip:
            try:
                res = requests.get(GEOIP_API_URL.format(clean_ip), headers=headers, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    country = data.get("country")
                    if country:
                        location = country
            except Exception as e:
                print(f"⚠️ 查询 IP {clean_ip} 出错: {e}")

        # 格式化拼接: IP:443#联通天花板大段 地区
        formatted_line = f"{clean_ip}:443#联通天花板大段 {location}"
        result_lines.append(formatted_line)
        print(f"[{index}/{len(raw_ips)}] {formatted_line}")

        # 控制请求频率：限制在每秒 1.5 次左右（约 0.6 秒间隔）
        time.sleep(0.6)

    # 导出文件 output.txt
    output_filename = "output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(result_lines) + "\n")
    
    print(f"🎉 处理完成！已生成 {output_filename}（共 {len(result_lines)} 行）")

if __name__ == "__main__":
    main()
