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
