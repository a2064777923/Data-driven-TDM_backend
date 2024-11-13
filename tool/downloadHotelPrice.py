import time

import requests
import os
from calendar import month_abbr


def download_reports(start_year, end_year, save_dir):
    # 如果保存目录不存在，则创建目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    base_url = "https://dataplus.macaotourism.gov.mo/document/CHT/Report/HotelsOccupancyRate"

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # 获取月份的缩写，例如 Jan, Feb 等
            month_abbreviation = month_abbr[month]
            # 构建下载链接
            #Hotels%20Occupancy%20Rate%20-%20
            file_url = f"{base_url}/{year}/MHA%20Monthly%20Report%20-%20{month_abbreviation}%20{str(year)}.pdf"
            # 构建本地文件名
            file_name = f"Hotels_Occupancy_Rate_{month_abbreviation}_{year}.pdf"
            file_path = os.path.join(save_dir, file_name)

            try:
                # 下载文件
                response = requests.get(file_url)
                time.sleep(3)
                response.raise_for_status()  # 检查请求是否成功
                # 将内容写入本地文件
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {file_name}")
            except requests.HTTPError as e:
                print(f"Failed to download {file_name}: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    # 下载从2015年到2024年的文件，保存到指定目录
    download_reports(2024, 2024, "macao_tourism_reports")
