import csv
from requests import get
import pandas as pd


url = 'https://data.gov.ru/opendata/2636045265-vakansii/data-20220930T1501-structure-20220930T1501.csv'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}

data = get(url, headers=header)

with open('data.csv', 'wb') as f:
    f.write(data.content)

with open('data.csv', 'r', encoding='UTF-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    field_names = reader.fieldnames
    print(field_names)
    for row in reader:
        print(f"{row['post']}: {row['requirement']}\n")


# dataframe = pd.read_csv('data.csv', sep=',')
#
# result = dataframe[dataframe['subdivision'] == 'отдел охраны контроля и надзора за использованием объектов животного и растительного мира']
# print(result)
