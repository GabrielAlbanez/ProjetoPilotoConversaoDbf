import pandas as pd
import os

print("-------------------- Tabela de Faturanento ----------------------")

getArquivoFaturamentoCliente = "PandaMoreExecell/Files/faturamento_por_cliente.csv"


numeroPego = input("digite 1 para ver o valor total de todos os clientes | digite 2 para escolher um nome de um cliente especifico para visualizar seu valor total: ")

number = int(numeroPego)

def ListeningAll():
    try:
        takeCsvFaturamentoCliente = pd.read_csv(getArquivoFaturamentoCliente)
        print("Tabela de faturamento de todos os clientes:")
        print(takeCsvFaturamentoCliente)
    except FileNotFoundError:
        print("Arquivo 'faturamento_por_cliente.csv' não encontrado.")
        # Saia da função, mas não do programa
        return
    
def ListeningFilterName():
    name  = input("digite o nome da pessoa de quem desejar buscar: ")
    takeCsvFaturamentoCliente = pd.read_csv(getArquivoFaturamentoCliente)
    takeCsvFaturamentoCliente[takeCsvFaturamentoCliente["cliente"] == name.islower()]
    return print("opção de listar pelo nome")


def caseListeningFaturamentoCLientes(option):
    switch = {
        1: ListeningAll,  # Armazenar a função, não chamá-la
        2: ListeningFilterName,
    }
    func = switch.get(option)
    if func:
        # option igual a 1
        #ficaria tipo func = ListeningAll
        func()  # ele adiciona so o parenteses ListeningAll()
    else:
        print("Escolha apenas os números 1 e 2.")


caseListeningFaturamentoCLientes(number)






# Caso queira ver apenas algumas linhas, pode usar:
# print(faturamento_cliente.head())  # Exibe as primeiras 5 linhas
# print(faturamento_cliente.tail())  # Exibe as últimas 5 linhas
# df_filtered = df[df['coluna'] > valor]  # Filtrar linhas com base em uma condição



