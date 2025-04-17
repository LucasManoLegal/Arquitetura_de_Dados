import requests
from bs4 import BeautifulSoup
import pandas as pd

# Url do site a ser acessado
url = "http://books.toscrape.com/"

# Fazer a requisição HTTP
response = requests.get(url)
response.encoding = 'utf-8'

# Criar um objeto BeautifulSoup para analisar o HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Criar uma lista para armazenar os dados
books_data = []

# Encontrar os elementos
books = soup.find_all('article', class_='product_pod')

for book in books:
    title = book.h3.a.attrs['title']
    price = book.find('p', class_='price_color').text
    books_data.append([title, price])

df = pd.DataFrame(books_data, columns=['Título', 'Preço'])

df.to_excel('livros.xlsx', sheet_name='livros', index=False)

print('Dados salvos com sucesso!')