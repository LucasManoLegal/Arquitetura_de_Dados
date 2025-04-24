
# Introdução ao Web Scraping

O **Web Scraping** é uma técnica utilizada para **extrair informações de páginas da web automaticamente**. Essa prática é muito útil para coletar dados públicos de sites, como notícias, preços de produtos, cotações, dados de eventos, entre outros.

---

## Sites Estáticos vs Dinâmicos

### Sites Estáticos

- Os dados estão **diretamente no HTML** da página.
- Você pode **acessar e extrair o conteúdo** com facilidade usando bibliotecas como `requests` e `BeautifulSoup`.

#### Exemplo de fluxo para scraping de site estático:

```python
import requests
from bs4 import BeautifulSoup

url = "https://exemplo.com"
resposta = requests.get(url)
sopa = BeautifulSoup(resposta.text, "html.parser")

titulo = sopa.find("h1").text
print(titulo)
```

---

### Sites Dinâmicos

- Os dados são carregados **via JavaScript**, depois que a página é exibida no navegador.
- O HTML inicial pode **não conter os dados desejados**.
- É necessário usar ferramentas que **simulem um navegador**, como `Selenium` ou `Playwright`.

#### Exemplo básico com Selenium:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

servico = Service('caminho/para/chromedriver')
driver = webdriver.Chrome(service=servico)

driver.get("https://site-dinamico.com")
elemento = driver.find_element(By.CLASS_NAME, "titulo")
print(elemento.text)

driver.quit()
```

---

## Boas Práticas

- Verifique sempre os **termos de uso** do site.
- Respeite as **políticas de acesso e frequência** (ex.: usar `time.sleep()` para pausar entre requisições).
- Prefira **APIs públicas**, se disponíveis.
- Utilize **headers** e **user-agents** para simular um navegador real e evitar bloqueios.

---

## Conclusão

- O Web Scraping é uma ferramenta poderosa para automação e coleta de dados.
- **Sites estáticos** são mais simples de manipular com HTML puro.
- **Sites dinâmicos** exigem ferramentas mais robustas que renderizem o conteúdo carregado via JavaScript.
