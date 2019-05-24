# -*- coding: utf-8 -*-
import os
import pandas as pd
import json
from collections import defaultdict

# Recebe o xlsx e formata em uma lista de discionarios
def toFormatJsonBDPostagens(path):
    arqPostagenCsv = open(path, encoding='utf-8')
    postagensCsvAux = pd.read_csv(arqPostagenCsv)
    arqPostagenCsv.close()
    postagensDF = pd.DataFrame(postagensCsvAux)
    # print(postagensDF.head())
    # exit()
    jsonPostagensAux = []
    for i in postagensDF.index:
        jsonAux = {}
        a1 = postagensDF["Seleção"][i]
        a2 = postagensDF["ID_Usuário"][i]
        a3 = postagensDF["Título"][i]
        a4 = postagensDF["Data"][i].split("/")
        a5 = postagensDF["PRU/N-PRU"][i]
        a6 = postagensDF["Tipo de PRU"][i].replace(" ", "").split(",")
        a7 = postagensDF["Polaridade"][i]
        a8 = postagensDF["Funcionalidade"][i]
        a9 = postagensDF["Elogio"][i]
        a10 = postagensDF["Ajuda"][i]
        a11 = postagensDF["Crítica"][i]
        a12 = postagensDF["Dúvida"][i]
        a13 = postagensDF["Comparação"][i]
        a14 = postagensDF["Sugestão"][i]
        a15 = postagensDF["Positivo"][i]
        a16 = postagensDF["Negativo"][i]
        a17 = postagensDF["Neutro"][i]

        # jsonAux["ID_Usuário"] = a2 jsonAux["Seleção"] = a1 jsonAux["Título"] = a3
        jsonAux["Data"] = a4
        # jsonAux["Pru/N-PRU"] = a5
        jsonAux["Tipo de PRU"] = a6
        jsonAux["Polaridade"] = a7
        jsonAux["Funcionalidade"] = a8
        # jsonAux["Artefato"] = a9

        jsonPostagensAux.append(jsonAux)

    return jsonPostagensAux

# Remove as postagens duplicadas CORRETO
def removeDuplicata(auxOnlyEmoticons):
    aux = []
    for elem3 in auxOnlyEmoticons:
        if elem3 not in aux:
            aux.append(elem3)
    return aux

def obterFuncionalidade(auxCsv):
    aux = []
    for elem in auxCsv:
        jsonAux = {}
        jsonAux = elem["Funcionalidade"]
        aux.append(jsonAux)

    return removeDuplicata(aux)

def contaTipo(listTipo):
    # listTipo = [{'Data': ['6', '1', '2011'], 'Tipo de PRU': ['Ajuda'], 'Polaridade': 'Neutro', 'Funcionalidade': 'Matrícula'}]
    # print(listTipo)
    # exit()
    retornoAux = []
    elogioAux, criticaAux, duvidaAux, comparacaoAux, ajudaAux, sugestaoAux = 0, 0, 0, 0, 0, 0
    for i in range(len(listTipo)):
        if listTipo[i] == "Elogio":
            elogioAux += 1
        elif listTipo[i] == "Crítica":
            criticaAux += 1
        elif listTipo[i] == "Dúvida":
            duvidaAux += 1
        elif listTipo[i] == "Comparação":
            comparacaoAux += 1
        elif listTipo[i] == "Ajuda":
            ajudaAux += 1
        elif listTipo[i] == "Sugestão":
            sugestaoAux += 1
    retornoAux.append(elogioAux); retornoAux.append(criticaAux); retornoAux.append(duvidaAux)
    retornoAux.append(comparacaoAux); retornoAux.append(ajudaAux); retornoAux.append(sugestaoAux)
    return retornoAux

def incrementaVector(auxVector, auxDados):
    retornoAux = [0 for i in range(6)]
    for i in range(len(auxDados)):
        retornoAux[i] = auxVector[i] + auxDados[i]
        # auxVector[i] += auxDados[i]
        # print(auxVector)
    # print(auxVector)
    # exit()
    return retornoAux

def contaTipoPorMêsEFuncionalidade(listaFuncionalidade, bdAux):
    # b = {'Data': '6/1/2011'.split("/"), 'Tipo de PRU': 'Ajuda', 'Polaridade': 'Neutro', 'Funcionalidade': 'Matrícula'}
    # a = {'Data': '6/1/2011'.split("/"), 'Tipo de PRU': 'Ajuda', 'Polaridade': 'Neutro', 'Funcionalidade': 'Matrícula'}
    # bdAux.clear()
    # bdAux.append(a); bdAux.append(b)
    # listaFuncionalidade.clear()
    # listaFuncionalidade = obterFuncionalidade(bdAux)
    retornoFinal = []
    retornoAux = []
    auxJan,auxFev,auxMar,auxAbr,auxMaio,auxJun = [0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)]
    auxJul,auxAgo,auxSet,auxOut,auxNov,auxDez = [0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)],[0 for i in range(6)]
    for elem in listaFuncionalidade:
        jsonAux = {}
        for elem2 in bdAux:
            jsonAux["Funcionalidade"] = elem
            if elem == elem2["Funcionalidade"]:
                if elem2["Data"][1] == "1":
                    auxJan = incrementaVector(auxJan, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Jan"] = auxJan
                elif elem2["Data"][1] == "2":
                    auxFev = incrementaVector(auxFev, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Fev"] = auxFev
                elif elem2["Data"][1] == "3":
                    auxMar = incrementaVector(auxMar, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Mar"] = auxMar
                elif elem2["Data"][1] == "4":
                    auxAbr = incrementaVector(auxAbr, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Abr"] = auxAbr
                elif elem2["Data"][1] == "5":
                    auxMaio = incrementaVector(auxMaio, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Maio"] = auxMaio
                elif elem2["Data"][1] == "6":
                    auxJun = incrementaVector(auxJun, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Jun"] = auxJun
                elif elem2["Data"][1] == "7":
                    auxJul = incrementaVector(auxJul, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Jul"] = auxJul
                elif elem2["Data"][1] == "8":
                    auxAgo = incrementaVector(auxAgo, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Ago"] = auxAgo
                elif elem2["Data"][1] == "9":
                    auxSet = incrementaVector(auxSet, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Set"] = auxSet
                elif elem2["Data"][1] == "10":
                    auxOut = incrementaVector(auxOut, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Out"] = auxOut
                elif elem2["Data"][1] == "11":
                    auxNov = incrementaVector(auxNov, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Nov"] = auxNov
                elif elem2["Data"][1] == "12":
                    auxDez = incrementaVector(auxDez, contaTipo(elem2["Tipo de PRU"]))
                    jsonAux["Dez"] = auxDez
        retornoAux.append(jsonAux)
    return retornoAux

planilhaAux = toFormatJsonBDPostagens(".\Classificação - Artigo análise longitudinal - 2011.csv")
funcionalidadesAux = obterFuncionalidade(planilhaAux)
# print(planilhaAux)
# exit()
contagemFinal = contaTipoPorMêsEFuncionalidade(funcionalidadesAux, planilhaAux)

a = list(contagemFinal[0].keys())
print(contagemFinal[0])
# exit()
df = pd.DataFrame(contagemFinal)
df = df[a]
df.to_excel(".\classificaçãoThiago.xlsx")
exit()