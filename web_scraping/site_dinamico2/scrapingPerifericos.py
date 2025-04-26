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

# Caminho do ChromeDriver
chromedriver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"


servico = Service(chromedriver_path)
controle = webdriver.ChromeOptions()

# Opções configuráveis
controle.add_argument("--disable-gpu") 
controle.add_argument("--window-size=1920,1080")
controle.add_argument("--headless")

# Configurando a variável que inicia o navegador
executador = webdriver.Chrome(service= servico, options= controle)

url_site= "https://www.kabum.com.br/promocao/PERIFERICOSOFFICE"

# Abre o site com base na URL
executador.get(url_site)
time.sleep(5)

perifericos = {
        "Nome": [],
        "Preco": [],
        "Pagamento": [],
        "Frete": [],
        "Desconto": []
    }

pagina_atual = 1

# Loop infinito para continuar navegando pelas páginas até que não haja mais páginas disponíveis
while True:
    print(f"\n Coletando dados da página {pagina_atual}...")

    # Aguarda até que todos os elementos com a classe 'productCard' estejam presentes na página
    try:
        WebDriverWait(executador, 10).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard")))
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        # Caso os elementos não apareçam dentro de 10 segundos, exibe erro
        print("Tempo de espera excedido!")

    # Coleta todos os elementos que representam os produtos
    produtos = executador.find_elements(By.CLASS_NAME, "productCard")

    # Itera sobre cada produto encontrado
    for produto in produtos:
        try:
            # Coleta nome, preço e condições de pagamento do produto
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()
            pagamento = produto.find_element(By.CLASS_NAME, "priceTextCard").text

            # Verifica se o frete é grátis. Se não encontrar a classe, considera como frete pago
            try:
                produto.find_element(By.CLASS_NAME, "bg-success-500")
                frete = "Grátis"
            except:
                frete = "Pago"
            # Verifica se tem desconto. Se não encontrar a classe, considera como 0%
            try:
                desconto = produto.find_element(By.CLASS_NAME, "rounded-8").text.strip()
            except:
                desconto = "0%"

            # Exibe os dados no console
            print(f"{nome} / {preco} / {pagamento} / {desconto} / {frete}")

            # Adiciona os dados ao dicionário "perifericos"
            perifericos["Nome"].append(nome)
            perifericos["Preco"].append(preco)
            perifericos["Pagamento"].append(pagamento)
            perifericos["Frete"].append(frete)
            perifericos["Desconto"].append(desconto)

        except Exception:
            # Caso ocorra qualquer erro ao coletar os dados de um produto, exibe mensagem
            print("Erro ao coletar dados:", Exception)

    # Tenta encontrar e clicar no botão "próxima página"
    try:
        botao_proximo = WebDriverWait(executador, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            # Rola até o botão para garantir que está visível e clica
            executador.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(5)  # Espera a rolagem concluir

            executador.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a página {pagina_atual}")
            pagina_atual += 1
            time.sleep(5)  # Aguarda o carregamento da próxima página
        else:
            # Se o botão não for encontrado, o programa encerra
            print("Programa encerrado. Última página alcançada.")
            break
    except Exception as e:
        # Caso ocorra erro ao tentar clicar no botão da próxima página
        print("Erro! Falha ao tentar avançar para a próxima página...", e)
        break

executador.quit()

df_perifericos = pd.DataFrame(perifericos)

df_perifericos.to_excel("web_scraping/site_dinamico2/perifericos.xlsx", index=False)

print(f"Arquivo 'perifericos' salvo com sucesso! {len(df_perifericos)} produtos coletados!")
