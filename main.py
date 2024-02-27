from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep 


local = "taubate"#input("Diga sua cidade: ").strip().lower()
link = f"https://www.infojobs.com.br/vagas-de-emprego-{local}.aspx?page=1&campo=griddate&orden=desc"

# Instancia as opcoes de janela e outros atributos
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Instancia o navegador
driver = webdriver.Edge(options=options)
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

aceitar_cookies()



def tratar_dados(dados):
	print(dados)

def buscador_de_vaga():
	# Loop responsavel por rodar todas as vagas da página
	numero_vaga = 1
	numero_proxima_pagina = 2
	quantidade_de_vagas = 0
	while True:
		try:
			# Tentará achar as vagas na página em questão
			vaga = driver.find_element(By.XPATH, f'/html/body/main/div[2]/form/div/div[1]/div[2]/div[{numero_vaga}]')
		except:
			if checar_final_pagina(numero_proxima_pagina):
				# Se possível, irá para outra página
				# Sleep para dar tempo de carregar a nova página
				numero_vaga = 1
				numero_proxima_pagina += 1
			else:
				break
		else:
			# Encontrada a vaga, irá clicar nela para exibir detalhes
			sleep(0.01)
			vaga.click()
			quantidade_de_vagas += 1
			try:
				informacoes_da_vaga = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div')
			except:
				pass
			else:
				pass
				# tratar_dados(informacoes_da_vaga.text)


			numero_vaga += 1
	print(quantidade_de_vagas)

# /html/body/main/div[2]/form/div/div[1]/div[2]/div[1]
# /html/body/main/div[2]/form/div/div[1]/div[2]/div[1]

buscador_de_vaga()

# Fecha o navegador
driver.quit()

