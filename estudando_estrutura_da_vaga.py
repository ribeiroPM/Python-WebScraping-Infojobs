import json
from os import system
import os


def importar_arquivo():
	arq = open("2024-02-28-2033.json")
	saida = arq.read()
	saida = json.loads(saida)


	arq.close()

	return saida

dados = importar_arquivo()

dados_de_interesse = {"nmr_vagas": "Número de vagas"}

# for id_vaga, descricao in dados.items():
# 	cargo = descricao["cargo"]
# 	desc = descricao["descricao"]

# 	# print(desc.find("Número de vagas"))
# 	local_numero_vagas = desc.find("Número de vagas")
# 	numero_de_vagas = int(desc[local_numero_vagas+17:local_numero_vagas+19].strip())
# 	print(numero_de_vagas)
# 	# print(desc.split("\n")[9])



print(dir(os))

print(os.listdir())