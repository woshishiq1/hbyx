import os
import gzip
import shutil
import requests
import geoip2.database

# 数据源与离线数据库 CDN 地址
IP_URL = "https://ip.ehb.cc.cd/198"
# 自动获取 GitHub/jsDelivr 镜像维护的免费 GeoLite2 City 离线库
DB_URL = "https://cdn.jsdelivr.net/npm/geolite2-city/GeoLite2-City.mmdb.gz"
DB_GZ = "GeoLite2-City.mmdb.gz"
DB_FILE = "GeoLite2-City.mmdb"

def prepare_database():
    """自动下载并解压 GeoLite2 本地数据库"""
    if not os.path.exists(DB_FILE):
        print("▶ [1/4] 正在下载 GeoLite2 离线数据库...")
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(DB_URL, headers=headers, stream=True, timeout=30)
        res.raise_for_status()
        
        with open(DB_GZ, 'wb') as f:
            f.write(res.content)
        
        print("▶ [2/4] 正在解压数据库文件...")
        with gzip.open(DB_GZ, 'rb') as f_in:
            with open(DB_FILE, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # 清理压缩包
        if os.path.exists(DB_GZ):
            os.remove(DB_GZ)
        print("✔ 离线数据库准备就绪！")

def get_ip_list():
    """从目标 URL 获取 IP 列表"""
    print(f"▶ [3/4] 正在从 {IP_URL} 获取 IP 列表...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(IP_URL, headers=headers, timeout=15)
        response.raise_for_status()
        # 按行分割，过滤空白行
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"❌ 获取 IP 列表失败: {e}")
        return []

def main():
    prepare_database()
    raw_ips = get_ip_list()
    
    if not raw_ips:
        print("⚠️ 未读取到有效 IP 数据，程序终止。")
        return

    result_lines = []
    print(f"▶ [4/4] 共获取到 {len(raw_ips)} 条数据，开始离线解析...")

    # 加载本地 GeoLite2 数据库
    with geoip2.database.Reader(DB_FILE) as reader:
        for item in raw_ips:
            # 提取纯 IP（适配可能自带端口的情况，如 1.2.3.4 或 1.2.3.4:80）
            clean_ip = item.split("#")[0].split(":")[0].strip()
            
            try:
                # 离线查询地区
                response = reader.city(clean_ip)
                # 优先获取中文国家名称，若无则显示英文或默认未知
                location = response.country.names.get('zh-CN') or response.country.name or "未知地区"
            except Exception:
                location = "未知地区"

            # 格式化拼接: IP:443#联通天花板大段 地区
            formatted_line = f"{clean_ip}:443#联通天花板大段 {location}"
            result_lines.append(formatted_line)

    # 导出文件 output.txt
    output_filename = "output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(result_lines) + "\n")
    
    print(f"🎉 处理完成！已生成 {output_filename}（共 {len(result_lines)} 行）")

if __name__ == "__main__":
    main()
