"""
Abaixo segue um programa escrito em python 3.6 (robô) que irá capturar os valores do PLD encontrados no site da CCEE.
Para você poder usar este programa com extrema facilidade, logo abaixo encontram-se os pacotes que necessitam ser
baixados e ao longo do código podem ser encontrados comentários detalhando as funcionalidades do programa.
OBS: PARA ESTE PROGRAMA RODAR CORRETAMENTE VOCÊ DEVE:
          1 - BAIXAR O WEBDRIVER DO GOOGLE CHROME DA VERSÃO COMPATÍVEL COM O SEU NAVEGADOR;
          2 - COPIAR O (PATH) DO ARQUIVO EXECUTÁVEL DO WEBDRIVER JUNTO COM O NOME do arquivo executável PARA A VARIÁVEL path, SITUADA NA FUNÇÃO access. EX: PATH\chromedriver.exe

BIBLIOTECAS: 1- selenium; 2- datetime; 3- os; 4- time
FUNCIONALIDADES: 1- Acessar o site; 2- Capturar os dados; 3- Gerar arquivo txt com os dados retirados do site
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import os
import time

"""
FUNÇÃO PRINCIPAL, BASTA CHAMÁ-LA PARA O PROGRAMA RODAR
"""


def main():
    browser = access()
    catcher = collect(browser)
    archive(catcher[0], catcher[1])


"""
1ª PARTE
    Funcionalidades:
            Conectar o python ao Google Chrome;
            Abrir o site para capturar dos dados.
"""


def access():
    path = "C:\Program Files (x86)\chromedriver.exe"
    browser = webdriver.Chrome(path)
    browser.get("https://www.ccee.org.br/portal/faces/pages_publico/o-que-fazemos/como_ccee_atua/precos/preco_sombra"
                "?_afrLoop"
                "=19345636429405&_adf.ctrl-state=mj077qp2f_1#!%40%40%3F_afrLoop%3D19345636429405%26_adf.ctrl-state"
                "%3Dmj077qp2f_5 ")
    return browser


"""
2ª PARTE
    Funcionalidades:
            Interagir com cada botão (submercado);
            Capturar os dados (horas, PLD horario);
            Colocar os dados em listas (hour_list, price_lists).
"""


def collect(browser):
    price_lists = [None, None, None, None]
    submarkets = ["SUDESTE", "SUL", "NORDESTE", "NORTE"]
    try:
        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "sorting_1"), '00:00'))

        for i in range(4):
            """ 1ª etapa - Interagir com cada botão (submercado)"""
            li = browser.find_element_by_id(submarkets[i])
            li.find_element_by_tag_name("a").click()

            """2ª etapa - Capturar os dados (horas, PLD horario)"""
            WebDriverWait(browser, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "sorting_1"), '00:00'))
            main = browser.find_element_by_id("listaValoresPrecoHorario")
            tbody = main.find_element_by_tag_name("tbody")
            text = tbody.text

            """ 3ª etapa - Colocar os dados em listas (hour_list, price_lists) """
            list = text.split("\n")
            hour_list = [hour[0:5] for hour in list]
            price_lists[i] = [price[-6:-1] for price in list]

        print(hour_list, '\n', price_lists[0], '\n', price_lists[1], '\n', price_lists[2], '\n', price_lists[3])

        """
        3ª PARTE
            Funcionalidades:
                Gerar arquivo txt;
                Colocar dados das listas no arquivo txt.
        """
        hour_and_price_lists = [hour_list, price_lists]

    finally:
        browser.quit()

    return hour_and_price_lists


def archive(lst1, lst2):
    current_date = date.today()
    name = "PRECO_HORARIO_{}_0{}_{}.txt".format(current_date.year, current_date.month, current_date.day)
    if check_file(name) is True:
        os.remove(name)
        print("Arquivo {} excluido".format(name))
        time.sleep(2)
        create_file(name, lst1, lst2)
        print("Arquivo {} criado novamente".format(name))
    else:
        create_file(name, lst1, lst2)
        print("Arquivo {} criado".format(name))


def create_file(name, lst1, lst2):
    with open(name, 'w') as file:
        file.write("HORA" + ";" + "SE/CO" + ";" + "S" + ";" + "NE" + ";" + "N" "\n")
        for i in range(24):
            file.write(
                lst1[i] + ";" + lst2[0][i] + ";" + lst2[1][i] + ";" + lst2[2][i] + ";" + lst2[3][i] + '\n')
    return


def check_file(name):
    try:
        a = open(name, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


main()
