import pandas as pd

"""
此工具幫助將Excel文件轉換成SQL語句
暫未實現批量轉(應該倒不需要這麼懶吧...)
"""
excelPath = "./resources/festival_event_table.xlsx" #填入Excel文件路徑
sheetName = "Sheet 1" #表名
tableName = "" #表名有特殊要求填這，否則用Excel名了

if tableName == "":
    tableName = excelPath.split("/")[-1].split(".")[0]

print(tableName)
data = pd.read_excel( excelPath, sheet_name=sheetName, index_col=None)


def generate_create_table_sql(data, tableName):
    columnTypes = {
        'int64': 'INT',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        # 添加其他需要的類型映射
    }

    columns = []
    for columnName, dtype in data.dtypes.items():
        sql_type = columnTypes.get(str(dtype), 'VARCHAR(255)')
        columns.append(f"{columnName} {sql_type}")

    columnsSQL = ", ".join(columns)
    return f"CREATE TABLE {tableName} ({columnsSQL});"

def generate_insert_sql(df, tableName):
    insertStatements = []
    for _, row in df.iterrows():
        values = ', '.join([f"'{str(value).replace("'", "''")}'" for value in row])
        insertStatements.append(f"INSERT INTO {tableName} VALUES ({values});")
    return insertStatements



if __name__ == "__main__":
    create_table_sql = generate_create_table_sql(data, tableName)
    print(create_table_sql)
    insert_sqls = generate_insert_sql(data, tableName)
    for sql in insert_sqls:
        print(sql)
