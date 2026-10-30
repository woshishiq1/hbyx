import time
import requests

IP_URL = "https://ip.ehb.cc.cd/198"
# 使用支持批量查询且对机房/CDN IP识别精准的免费接口
BATCH_API_URL = "https://api.ipquery.io/"

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

    # 提取纯 IP 列表并去重，同时保留原始对应关系
    ip_map = {}
    clean_ips = []
    for item in raw_ips:
        clean_ip = item.split("#")[0].split(":")[0].strip()
        if clean_ip and clean_ip not in ip_map:
            clean_ips.append(clean_ip)
            ip_map[clean_ip] = item

    print(f"▶ 共提取到 {len(clean_ips)} 个独立 IP，开始通过精准 API 查询归属地...")

    location_results = {}
    
    # ipquery.io 支持批量查询（每次最多批量处理，安全起见我们每 50 个一组发送）
    batch_size = 50
    for i in range(0, len(clean_ips), batch_size):
        batch = clean_ips[i:i+batch_size]
        # 拼接成逗号分隔的字符串进行批量请求
        query_str = ",".join(batch)
        try:
            res = requests.get(f"{BATCH_API_URL}{query_str}", timeout=15)
            if res.status_code == 200:
                data = res.json()
                # 如果是多条数据，返回的是一个列表
                if isinstance(data, list):
                    for item_data in data:
                        ip = item_data.get("ip")
                        # 严格获取国家名称，不进行任何虚假兜底
                        country = item_data.get("location", {}).get("country")
                        if country:
                            location_results[ip] = country
                elif isinstance(data, dict) and "ip" in data:
                    # 单条返回的兼容处理
                    ip = data.get("ip")
                    country = data.get("location", {}).get("country")
                    if country:
                        location_results[ip] = country
            
            # 适当停顿，防止请求过快
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ 批量查询某段 IP 时出错: {e}")

    # 组装最终结果
    result_lines = []
    for raw_item in raw_ips:
        clean_ip = raw_item.split("#")[0].split(":")[0].strip()
        # 获取真实的查询结果，如果实在查不到则如实显示“未知地区”（绝对不盲目瞎编兜底）
        location = location_results.get(clean_ip, "未知地区")
        
        formatted_line = f"{clean_ip}:443#联通天花板大段 {location}"
        result_lines.append(formatted_line)

    # 导出文件 output.txt
    output_filename = "output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(result_lines) + "\n")
    
    print(f"🎉 处理完成！已生成 {output_filename}（共 {len(result_lines)} 行）")

if __name__ == "__main__":
    main()
