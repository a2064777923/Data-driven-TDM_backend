from dbm import error

import requests
import json
import xml.etree.ElementTree as ET
import pandas as pd


def save_xml(data):
    title = "data"
    try:
        title = ET.fromstring(data).attrib['title']
    except KeyError as e:
        print(e)
    with open(f'{title}.xml', 'w', encoding='utf-8') as file:
        file.write(data)

def convert_xml_to_excel(data):
    root = ET.fromstring(data)
    all_data = []
    title = "data"
    try:
        title = ET.fromstring(data).attrib['title']
    except KeyError as e:
        print(e)

    def parse_element(element, parent_data):
        item_data = parent_data.copy()
        item_data.update(element.attrib)  # current element attribute
        all_data.append(item_data)

        for child in element:
            parse_element(child, item_data)

    parse_element(root, {})
    clean_data = [d for d in all_data if d]
    # should use method 2
    if len(clean_data) == 0:
        try:
            root = ET.fromstring(data)
            all_data = []

            for element in root.iter():
                item_data = {}
                for child in element:
                    item_data[child.tag] = child.text
                if item_data:
                    all_data.append(item_data)

        except ET.ParseError as e:
            print(f"解析错误: {e}")

    df = pd.DataFrame(all_data)
    df.to_excel(f'{title}.xlsx', index=False)



def save_json(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(data)

def convert_json_to_excel(data):
    json_data = json.loads(data)
    df = pd.DataFrame(json_data)
    df.to_excel('data_json.xlsx', index=False)


def main():
    api_url = input("Please Enter API: ")
    authorization = input("Please Enter Authorization: ")

    # if input nothing, the default data is car_park
    if api_url == "":
        api_url = "https://dsat.apigateway.data.gov.mo/car_park_detail"

    if authorization == "":
        authorization = "APPCODE 09d43a591fba407fb862412970667de4"

    headers = {
        'Authorization': authorization
    }
    try:

        response = requests.get(api_url, headers=headers)

        # see the content is XML or JSON
        content_type = response.headers.get('Content-Type')

        response.encoding = 'utf-8'
        data = response.text
    except error as e:
        print(e)
        return


    if 'application/xml' in content_type or 'text/xml' in content_type:
        # process XML
        save_xml(data)
        convert_xml_to_excel(data)
    elif 'application/json' in content_type:
        # process JSON
        save_json(data)
        convert_json_to_excel(data)
    else:
        print(data)



if __name__ == "__main__":
    main()
