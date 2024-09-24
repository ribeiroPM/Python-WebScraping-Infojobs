from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep 
from os import system, listdir
from time import strftime as st
import json


"""
Script simples que capta vagas de emprego de um determinado site (infojobs), faz o tratamento de dados e os aramzena em um arquivo json;
Principais funções:
	> Captar vagas de emprego de acordo com a cidade informada;
	> Roda todas as páginas, uma à uma, pegando vaga por vaga;
	> Armazena as vagas em um arquivo JSON;
	> Consegue definir se houve alguma vaga nova publicada;
	> Consegue navegar por vagas anteriores.

Possíveis Bugs:
	> Se a cidade informada tiver poucas vagas (apenas uma página), vai dar erro;
	> A mesma vaga vai para o tratamento de dados mais de uma vez.


"""

# Data para criação do nome do novo arquivo
data_atual = f'{st("%Y")}-{st("%m")}-{st("%d")}-{st("%H")}{st("%M")}'
tem_novas_vagas = False

# Variaveis Globais
dados_das_vagas = {} # Coleção com todos os Dados Captados
local = "Taubate"#input("Diga sua cidade: ").strip().lower()
link = f"https://www.infojobs.com.br/vagas-de-emprego-{local}.aspx?page=1&campo=griddate&orden=desc"

# Instancia as opcoes de janela e outros atributos
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Instancia o navegador
driver = webdriver.Edge(options=options)

def iniciar_driver():
	driver.get(link)


def aceitar_cookies():
	# Função responsavel por aceitar os cookies
	while True:
		try:
			# Irá procurar o botão "aceitar"  dos cookies 
			sleep(1)
			botao_aceitar_cookies = driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
		except:
			pass
		else:
			botao_aceitar_cookies.click()
			break

def checar_final_pagina(npp):
	# Caso ele chegue à uma pagina em branco, irá retornar False
	link = f"https://www.infojobs.com.br/vagas-de-emprego-{local}.aspx?page={npp}&campo=griddate&orden=desc"
	driver.get(link)
	sleep(1)
	# Frase que deveria ser exibida numa pagina em branco sem vagas
	frase_final = "Ops! Nenhuma vaga foi encontrada com os filtros selecionados, mas não se preocupe, veja o que você pode fazer:"
	# Procura a frase em questao na pagina
	try:
		frase_final_pagina = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div/h2').text.strip()
	except:
		# Caso nao encontre a frase, o retorno sera positivo tambem
		return True
	else:
		# Caso encontre a frase, retornara falso, dizendo que nao ha mais vagas
		return frase_final_pagina != frase_final


def exportar_dados(dados_vaga, nome_arquivo=""):
	nome_arquivo = f"{data_atual}.json" if nome_arquivo == "" else nome_arquivo
	# Função responsável por exportar (salvar) a lista de vagas e suas respectivas descrições em um arquivo externo, no formato JSON
	arquivo = open(nome_arquivo, "w")
	arquivo.write(json.dumps(dados_vaga, indent=4))
	arquivo.close()


def importar_arquivo(nome_arquivo):
	arquivo = open(nome_arquivo)
	saida = arquivo.read() # Abre o arquivo para leitura, em formato string
	saida = json.loads(saida) # Converte de string para dicionario (pelo formato que os dados foram armazenados)
	arquivo.close()
	return saida


def tratar_dados(dados_vaga):
	global dados_das_vagas
	# O cargo sempre é exibido no topo do detalhamento da vaga, no caso a primeira linha dos dados
	cargo = dados_vaga.split("\n")[0] # Particiona toda a informação, pelo caractere de quebra de linha("\n"), e pega apenas o Primeiro item (o cargo)

	# Cria um ID, afinal coleções em forma de dicionario aceitam apenas chaves exclusivas, e podem haver vagas com mesmo nome
	# O ID consiste em um numero de 6 dígitos, sendo a quantidade total de caracteres que coontém na descrição da vaga, mais o  "cargo", captado anteriormente.
	# se houver uma vaga com mesmo nome e mesma quantidade de caracteres será muita coincidencia (improvável).
	id_vaga = f"{len(dados_vaga):0>6}_" + cargo.split()[0].upper()

	# O buscador de vagas as vezes retorna a mesma vaga mais de uma vez, com preguça de identificar o erro, fiz este if, que garante que a vaga seja tratada apenas uma vez
	if id_vaga not in dados_das_vagas:
		print(cargo)
		dados_das_vagas[id_vaga] = {}
		dados_das_vagas[id_vaga]["cargo"] = cargo
		dados_das_vagas[id_vaga]["descricao"] = dados_vaga


def verificar_se_tem_vagas_novas(dados_atuais):
	global tem_novas_vagas # Variável que diz se existem novas vagas
	# Lista de arquivos de busca anteriores
	dados_anteriores = [arquivo for arquivo in listdir() if "json" in arquivo][-1]
	arquivo_anterior = importar_arquivo(dados_anteriores)

	nmr_vagas_novas = 0 # Quantidade de vagas novas (se houverem)
	vagas_novas = {} # Coleção para novas vagas
	for id_vaga in dados_atuais.keys():
		if id_vaga not in arquivo_anterior:
			nmr_vagas_novas += 1
			vagas_novas[id_vaga] = dados_atuais[id_vaga]
	tem_novas_vagas = nmr_vagas_novas > 0
	if tem_novas_vagas:
		# Se houverem novas vagas, vai exportar a coleção com elas
		exportar_dados(vagas_novas, "vagas_novas.json")


def buscador_de_vaga():
	# Loop responsavel por rodar todas as vagas da página
	numero_vaga = 1
	numero_proxima_pagina = 2
	quantidade_de_vagas = 0
	global a
	while True:
		try:
			# Tentará achar as vagas na página em questão
			# vaga = driver.find_element(By.XPATH, f'/html/body/main/div[2]/form/div/div[1]/div[2]/div[{numero_vaga}]')
			vaga = driver.find_element(By.XPATH, f'//*[@id="filterSideBar"]/div/div[{numero_vaga}]')
			//*[@id="filterSideBar"]/div[6]/div[2]
		except:
			print("Erro")
			if checar_final_pagina(numero_proxima_pagina):
				# Se possível, irá para outra página
				# Sleep para dar tempo de carregar a nova página
				numero_vaga = 1
				numero_proxima_pagina += 1
			else:
				verificar_se_tem_vagas_novas(dados_das_vagas)
				if tem_novas_vagas:
					# Caso tenha encontrado novas vagas, irá exportar
					exportar_dados(dados_das_vagas)
				break
		else:
			# Encontrada a vaga, irá clicar nela para exibir detalhes
			vaga.click()
			quantidade_de_vagas += 1
			while True:
				# Loop para ter certeza que as informações da vaga foram carregados
				try:
					# Capta os dados da vaga
					informacoes_da_vaga = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div')
				except:
					pass
				else:
					# Caso os dados da vaga não tenham carregados, seu valor será zero, reiniciando o loop
					if len(informacoes_da_vaga.text) > 0:
						break
			# Caso o loop anterior tenha terminado com êxito, os dados vão para tratamento
			print(a)
			# print(informacoes_da_vaga.text)

			a+=1
			tratar_dados(informacoes_da_vaga.text)

			# Após o tratamento da vaga anterior, parte para a próxima
			numero_vaga += 1
a = 0

def menu(msg, opcoes):
	# lista de opcoes para o menu
	opcoes = opcoes.split(", ")
	nmr_opcoes = len(opcoes)
	# Menu de escolha
	menu_titulo_adicional = "."
	while True:
		system("cls")
		print("MENU" + menu_titulo_adicional)
		for n_opc, opc in enumerate(opcoes):
			print(f"[{n_opc+1}] - {opc.upper()}")
		saida = input(msg)
		try:
			saida = int(saida)
		except:
			menu_titulo_adicional = ". Opção inválida! Tente um número."
		else:
			if 0 < saida < nmr_opcoes+1:
				break
			else:
				menu_titulo_adicional = f". Opção inválida! Tente um número entre 1 e {nmr_opcoes}."
	return saida


def visualizador_de_vagas(opc=1):
	if opc == 1:
		# Neste caso voce podera escolher entre todas as listas de vagas encontradas até o momento
		lista_de_vagas_coletadas = [arquivo for arquivo in listdir() if "json" in arquivo]
		escolha = menu("Qual arquivo deseja visualizar: ", ", ".join(lista_de_vagas_coletadas)) - 1 # Menos 1 pois os index começam em 0

		arquivo_selecionado = importar_arquivo(lista_de_vagas_coletadas[escolha])
	else:
		# Neste else, voce vera apenas a lista de vagas novas
		arquivo_selecionado = importar_arquivo("vagas_novas.json")

	for id_vaga, descricao in arquivo_selecionado.items():
		system("cls")
		desc = descricao["descricao"]
		print(desc)
		input("\nTecle enter para proxima vaga...")

		escolha_atual = menu("Escolha: ", "Proxima Vaga, sair")
		if escolha_atual == 2:
			break


while True:
	if tem_novas_vagas:
		escolha = menu("O que deseja: ", "Escanear vagas, Olhar Vagas Encontradas, Sair, Ver novas vagas")
	else:
		escolha = menu("O que deseja: ", "Escanear vagas, Olhar Vagas Encontradas, Sair")
	system("cls")
	if escolha == 3:
		break
	elif escolha == 2:
		visualizador_de_vagas()
	elif escolha == 4:
		visualizador_de_vagas(2)
	elif escolha == 1:
		print("Ok! Procurando novas vagas")
		iniciar_driver()
		aceitar_cookies()
		buscador_de_vaga()

# Fecha o navegador
driver.quit()
exit()

