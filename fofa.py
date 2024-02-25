# -*- coding: utf-8 -*-
import requests
import csv
from tqdm import tqdm
import base64

# 请替换为你自己的fofa API密钥
FOFA_EMAIL = "x@qq.com"
FOFA_KEY = "x"

def get_subdomains(domain):
    """
    使用fofa API查询子域名信息
    """
    all_results = []
    page = 1
    size = 9999  # 修改查询数量上限为9999
    while True:
        query = f'domain="{domain}"'
        url = f'https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={base64.b64encode(query.encode()).decode()}&page={page}&size={size}'
        res = requests.get(url)
        data = res.json()
        if data["error"]:
            print(f"查询{domain}时出错: {data['errmsg']}")
            return []
        else:
            all_results.extend(data["results"])
            if len(data["results"]) < size:
                break
            page += 1
    return all_results

def export_to_csv(data, filename):
    """
    将数据导出到csv文件中
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['subdomain', 'ip', 'port']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    # 读取包含根域名的文件
    with open("domains.txt", "r") as f:
        domains = [line.strip() for line in f.readlines()]

    all_data = []
    for i, domain in enumerate(tqdm(domains)):
        print(f"正在查询第{i+1}个根域名: {domain}")
        subdomains = get_subdomains(domain)
        for subdomain in subdomains:
            all_data.append({
                "subdomain": subdomain[0],
                "ip": subdomain[1],
                "port": subdomain[2]
            })

    # 导出结果到csv文件中
    export_to_csv(all_data, "all.csv")

if __name__ == "__main__":
    main()