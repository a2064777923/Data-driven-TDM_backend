import pandas as pd
import json

def excel_to_json(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 创建一个空列表，用于存储 JSON 对象
    json_list = []
    print(len(df["name_en"].to_numpy()))
    print(df["name_en"].to_numpy().tolist())
    # 遍历每一行，并将其转换为字典
    for index, row in df.iterrows():
        # 将每一行数据转换为字典
        data = {
            'name': row['name_en'],  # 将 name_en 映射为 name
            'classname_en': row['classname_en'],
            'tel': row['tel'],
            'room_no': row['room_no'],
            'type':'hotel',
            'address_en': row['address_en'],
            'value': [ round(float(row['longitude']),6),round(float(row['latitude']),6)]  # 将 latitude 和 longitude 映射为 value
        }
        # 将字典添加到列表中
        json_list.append(data)

    # 将列表转换为 JSON 格式的字符串
    json_data = json.dumps(json_list, indent=2)

    return json_data


file_path = './resources/hotel_detail.xlsx'
json_result = excel_to_json(file_path)
print(json_result)
