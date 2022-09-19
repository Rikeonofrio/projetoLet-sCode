from operator import delitem
from optparse import Option
from sys import displayhook
from tkinter import W
from typing import final
from PIL import Image
from IPython.display import display
import requests as r
import datetime as dt
import csv

url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)

print(resp.status_code)

raw_data = resp.json()


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])
final_data.insert(0, ['confirmados', 'obitos', 'recuperados','ativos', 'data'])

CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]

with open('brasil-covid.csv', 'w', encoding='utf-8') as file:
    writer =csv.writer(file, delimiter=',')
    writer.writerow(final_data)
    writer.writerow("\n")

for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA],'%Y-%m-%d')
print(final_data)

def get_datasets(y, labels):
    if type(y[0]) ==list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data' : y[i],
            })
        return datasets
    else:
        return [
            {
                'label' : labels[0],
                'data' : y
            }
        ]
        
def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return{
        'title':title,
        'display': display
    }
def create_chart(x, y, labels, kind='bar', title =''):
    datasets = get_datasets(y, labels)
    options = set_title(title)

    chart = {
        'type' : kind,
        'data' : {
            'labels' : x,
            'datasets' : datasets
        },
        'options': options
    }
    return chart

def get_api_charts(chart):
    url_base = 'https://quickchart.io/charts'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content

def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)

def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)

y_data_1 = []
for obs in final_data [1::30]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data [1::30]:
    y_data_1.append(obs[RECUPERADOS])

labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_data [1::30]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x,[y_data_1, y_data_2], labels, title='Grafico Confirmados vs Recuperados')
chart_content = get_api_charts(chart)
save_image('Meu-primeiro-grafico.png', chart_content)
display_image('Meu-primeiro-grafico.png')