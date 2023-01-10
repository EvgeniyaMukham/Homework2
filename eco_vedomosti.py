from bs4 import BeautifulSoup
import requests as rq
import pandas as pd

url = 'https://www.vedomosti.ru/ecology'
page = rq.get(url)
print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')
#print(soup.prettify())
for link in soup.find('body').find_all('a'):
    print(link.get('href'))

# на главной странице ссылки на выпуски
release_list = []

for link in soup.find('body').find_all('a'):
    if (link.get('href').startswith('/ecology/release/')):
        print(link.get('href'))
        release_list.append(link.get('href'))

article_list = []

for release in release_list:
    url = 'https://www.vedomosti.ru' + release
    page = rq.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    #добавляем ссылки на новости
    for link in soup.find_all('a'):
        try:
            if (link.get('href').startswith('/ecology/') and (('release') not in (link.get('href')))):
                print(link.get('href'))
                article_list.append(link.get('href'))
        except:
            pass

df_list = []

for article in article_list:
    article_data = []
    url = 'https://www.vedomosti.ru' + article
    page = rq.get(url)
    print(page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')

    article_data.append(url)

    # добавляем дату
    for link in soup.find_all('time'):
        # print(link.text)
        article_data.append(link.text.replace(' /', ''))
        # print(article_data)

    # заголовки
    for link in soup.find_all('h1'):
    # print(link.text)
        head = link.text.replace('\n', '').replace('  ', '')
        article_data.append(head)
        #print(article_data)

# добавляем текст
    text_ = ''
    for link in soup.find_all('p'):
    # print(link.text)
        if not link.text.startswith('\n'):
            text_ += (link.text)

    article_data.append(text_)

    df_list.append(article_data)

df = pd.DataFrame(df_list, columns=['Ссылка', 'Дата', 'Заголовок', 'Текст'])


df.to_excel('eco_vedomosti.xlsx')
df.to_csv('eco_vedomosti.csv', index=False)