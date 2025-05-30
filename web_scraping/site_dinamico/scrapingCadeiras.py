# Módulo para controlar o navegador web
from selenium import webdriver

# Localizador de elementos
from selenium.webdriver.common.by import By

# Serviço par configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avançadas. Ex: Mover do mouse, clique/arrasta
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explícita ate que uma condicão seja satisfeita. Ex: Que um elemento apareça
from selenium.webdriver.support.ui import WebDriverWait

# Condições esperadas usadas com o 'WebDriverWait'
from selenium.webdriver.support import expected_conditions as ec

# Lida com DataFrames
import pandas as pd

# Uso de funções relacionadas ao tempo
import time

# Uso de tratamento de exceção
from selenium.common.exceptions import TimeoutException



# Deninir o caminho do chromedriver
chromedriver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

# Configurar o WebDriver
servico = Service(chromedriver_path) # Navegador controlado pelo Selenium

# Configurar as opções do navegador
controle = webdriver.ChromeOptions() 
controle.add_argument("--disable-gpu") # Evita possíveis erros gráficos
controle.add_argument("--window-size=1920,1080") # Define uma resolução fixa

# Inicializar o WebDriver
executador = webdriver.Chrome(service= servico, options= controle)

# URL inicial
url_site= "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"
executador.get(url_site)
time.sleep(5) # Aguarda 5 seg para garantir que a página carregue corretamente

# Criar um dicionário para armazenar os marcas e o preços das cadeiras
dict_produtos = {
        "Nome": [],
        "Preco": []
    }

# Iniciando na página 1 e incrementamos o valor a cada troca de página
pagina_atual = 1

while True:
    print(f"\n Coletando dados da página {pagina_atual}...")

    try:
        WebDriverWait(executador, 10).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard")))
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")

    produtos = executador.find_elements(By.CLASS_NAME, "productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{nome} / {preco}")

            dict_produtos["Nome"].append(nome)
            dict_produtos["Preco"].append(preco)

        except Exception:
            print("Erro ao coletar dados:", Exception)

    # Encontrar botão da próxima página
    try:
        # Encontrar o elemento
        botao_proximo = WebDriverWait(executador, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            executador.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(5)

            # Clicar no botão
            executador.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a página {pagina_atual}")
            pagina_atual += 1
            time.sleep(5)
        else:
            print("Programa encerrado. Última página alcançada.")
            break
    except Exception as e:
        print("Erro! Falha ao tentar avançar para a próxima página...", e)
        break

# Encerra o navegador
executador.quit()

# dataframe
df_cadeiras = pd.DataFrame(dict_produtos)

# csv
df_cadeiras.to_excel("cadeiras.xlsx", index=False)

print(f"Arquivo 'cadeiras' salvo com sucesso! {len(df_cadeiras)} produtos coletados!")

        



