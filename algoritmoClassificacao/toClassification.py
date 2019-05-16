# -*- coding: utf-8 -*-
import os
import pandas as pd
import emoji
import json
from collections import defaultdict
#Abre um arquivo Json
def openJson(path):
    arqEmoticonJson = open(path, encoding='utf-8')
    emoticonJsonAux = arqEmoticonJson.read()
    arqEmoticonJson.close()
    emoticonJson = json.loads(emoticonJsonAux)
    return emoticonJson

#Abre um arquivo csv e passa para Json, em uma formatação especifica.
# Aqui é feito o carregamento do BD que possui os emoticons e a sua classificação de polaridade
def toFormatJsonEmoticon(path):
    arqEmoticonCSV = open(path, encoding='utf-8')
    emoticonCsvAux = pd.read_csv(arqEmoticonCSV)
    arqEmoticonCSV.close()
    emoticonDF = pd.DataFrame(emoticonCsvAux)

    jsonEmoticonAux = []
    for i in emoticonDF.index:
        jsonAux = {}
        a1 = emoticonDF["Emoticon"][i]
        a2 = emoticonDF["Positiva"][i]
        a3 = emoticonDF["Neutra"][i]
        a4 = emoticonDF["Negativa"][i]
        a5 = emoticonDF["Crítica"][i]
        a6 = emoticonDF["Elogio"][i]
        a7 = emoticonDF["Dúvida"][i]
        a8 = emoticonDF["Comparação"][i]
        a9 = emoticonDF["Sugestão"][i]
        a10 = emoticonDF["Ajuda"][i]

        jsonAux["id"] = i
        jsonAux["Emoticon"] = a1
        jsonAux["Positiva"] = a2
        jsonAux["Neutra"] = a3
        jsonAux["Negativa"] = a4
        jsonAux["Crítica"] = a5
        jsonAux["Elogio"] = a6
        jsonAux["Dúvida"] = a7
        jsonAux["Comparação"] = a8
        jsonAux["Sugestão"] = a9
        jsonAux["Ajuda"] = a10
        jsonEmoticonAux.append(jsonAux)

    return jsonEmoticonAux

def toFormatJsonBDPostagens(path):
    arqPostagenCSV = open(path, encoding='utf-8')
    postagensCsvAux = pd.read_csv(arqPostagenCSV)
    arqPostagenCSV.close()
    postagensDF = pd.DataFrame(postagensCsvAux)
    # print(postagensDF["PRU/Não-PRU"].head())
    # exit()
    jsonPostagensAux = []
    for i in postagensDF.index:
        jsonAux = {}
        a1 = postagensDF["N°"][i]
        a2 = postagensDF["Data"][i]
        a3 = postagensDF["ID"][i]
        a4 = postagensDF["Postagem"][i]
        a5 = postagensDF["Emojis da Postagem"][i]
        a6 = postagensDF["PRU/Não-PRU"][i]
        a7 = postagensDF["Tipo"][i]
        a8 = postagensDF["Analise de Sentimento"][i]
        a9 = postagensDF["Artefato"][i]

        jsonAux["ID"] = a3
        jsonAux["N°"] = a1
        jsonAux["Data"] = a2
        jsonAux["text"] = a4
        jsonAux["Emojis da Postagem"] = a5
        jsonAux["PRU/Não-PRU"] = a6
        jsonAux["Tipo"] = a7
        jsonAux["Analise de Sentimento"] = a8
        jsonAux["Artefato"] = a9

        jsonPostagensAux.append(jsonAux)

    return jsonPostagensAux

# print(toFormatJsonBDPostagens(".\PlanilhaTotal11-05-2019.csv"))
# exit()
def separaPru(postagensBD):
    onlyPrus = []

    for elem in postagensBD:
        jsonAux = {}
        if elem["PRU/Não-PRU"] == "PRU":
            jsonAux = elem
            onlyPrus.append(jsonAux)
    return onlyPrus
    # print(len(onlyPrus))
    # print(onlyPrus)

# separaPru(toFormatJsonBDPostagens(".\PlanilhaTotal09-05-2019.csv"))
# exit()

#Formata um Json de postagens para um formato especifico
# Json padrão usado em todo o trabalho, obtido na ferramenta UUX-Posts
def toFormatJsonData(path):
    postagensJsonAux = openJson(path)
    jsonListAux = []

    for i in postagensJsonAux["data"]:
        jsonAux = {}
        a1 = postagensJsonAux["data"][i]
        a2 = postagensJsonAux["dispositivo"][i]
        a3 = postagensJsonAux["id"][i]
        a4 = postagensJsonAux["text"][i]
        jsonAux["id"] = i
        jsonAux["data"] = a1
        jsonAux["dispositivo"] = a2
        jsonAux["text"] = a4
        jsonAux["idPostagem"] = a3
        jsonListAux.append(jsonAux)

    return jsonListAux
# print(toFormatJsonData(".\PostagensJsonTotal11-05-2019.json"))
# emoticonBDAux = toFormatJsonEmoticon(".\PlanilhaBDEmoticon.csv")

# Função para calcular a polaridade principal de cada emoticon
def calculaPolaridade(jsonBD):
    emoticonPolaridade = []
    emoticonIndefinido = []
    for elem in jsonBD:
        jsonAux = {}
        jsonAuxIndefinido = {}
        auxPos = elem["Positiva"]
        auxNeg = elem["Negativa"]
        auxNeu = elem["Neutra"]

        if(auxPos > auxNeg) and (auxPos > auxNeu):#Classifica o Emoticon como positivo
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Polaridade"] = "Positiva"
            emoticonPolaridade.append(jsonAux)
        elif(auxNeg > auxPos) and (auxNeg > auxNeu):#Classifica o Emoticon como negativo
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Polaridade"] = "Negativa"
            emoticonPolaridade.append(jsonAux)
        elif (auxNeu > auxPos) and (auxNeu > auxNeg):#Classifica o Emoticon como neutro
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Polaridade"] = "Neutra"
            emoticonPolaridade.append(jsonAux)
        else:
        	jsonAuxIndefinido["Emoticon"] = elem["Emoticon"]
        	jsonAuxIndefinido["Polaridade"] = "Indefinida"
        	emoticonPolaridade.append(jsonAuxIndefinido)

    return emoticonPolaridade,emoticonIndefinido

# Função para calcular o tipo principal de cada emoticon
def calculaValorDoTipo(jsonBD):
    emoticonPolaridade = []
    for elem in jsonBD:
        jsonAux = {}
        auxCritica = elem["Crítica"]
        auxElogio = elem["Elogio"]
        auxDuvida = elem["Dúvida"]
        auxComparacao = elem["Comparação"]
        auxSugestao = elem["Sugestão"]
        auxAjuda = elem["Ajuda"]

        if(auxCritica > auxElogio) and (auxCritica > auxDuvida)\
                and (auxCritica > auxComparacao) and (auxCritica > auxSugestao)\
                and (auxCritica > auxAjuda):#Classifica o Emoticon com o tipo Crítica
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Tipo"] = "Crítica"
            emoticonPolaridade.append(jsonAux)
        elif(auxElogio > auxCritica) and (auxElogio > auxDuvida)\
                and (auxElogio > auxComparacao) and (auxElogio > auxSugestao)\
                and (auxElogio > auxAjuda):#Classifica o Emoticon com o tipo Elogio
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Tipo"] = "Elogio"
            emoticonPolaridade.append(jsonAux)
        elif(auxDuvida > auxCritica) and (auxDuvida > auxElogio)\
                and (auxDuvida > auxComparacao) and (auxDuvida > auxSugestao)\
                and (auxDuvida > auxAjuda):#Classifica o Emoticon com o tipo Duvida
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Tipo"] = "Dúvida"
            emoticonPolaridade.append(jsonAux)
        elif (auxComparacao > auxCritica) and (auxComparacao > auxDuvida) \
                and (auxComparacao > auxElogio) and (auxComparacao > auxSugestao) \
                and (auxComparacao > auxAjuda):  # Classifica o Emoticon com o tipo Comparação
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Tipo"] = "Comparação"
            emoticonPolaridade.append(jsonAux)
        elif (auxSugestao > auxCritica) and (auxSugestao > auxDuvida) \
                and (auxSugestao > auxComparacao) and (auxSugestao > auxElogio) \
                and (auxSugestao > auxAjuda):  # Classifica o Emoticon com o tipo sugestão
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Tipo"] = "Sugestão"
            emoticonPolaridade.append(jsonAux)
        elif (auxAjuda > auxCritica) and (auxAjuda > auxDuvida) \
                and (auxAjuda > auxComparacao) and (auxAjuda > auxSugestao) \
                and (auxAjuda > auxElogio):  # Classifica o Emoticon com o tipo Ajuda
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Tipo"] = "Ajuda"
            emoticonPolaridade.append(jsonAux)

    return emoticonPolaridade
# pd.DataFrame(calculaValorDoTipo(toFormatJsonEmoticon(".\PlanilhaBDEmoticon.csv"))).to_csv("TesteTipo.csv")
# exit()

# Função para classificar a polaridade da cada postagem, com base no emoticon
def classificaPolaridade(emoticonsPolaridade, postagensAux):
    jsonClassificadoPolaridadeAux = []
    for elem in postagensAux:
        polaridadeAux = 0
        for elem2 in emoticonsPolaridade:
            jsonAux = {}
            if (elem["text"].find(elem2["Emoticon"])) >= 0:
                if elem2["Polaridade"] == "Positiva":
                    polaridadeAux += 1
                elif elem2["Polaridade"] == "Negativa":
                    polaridadeAux -= 1
        if polaridadeAux == 0:
            jsonAux["Postagem"] = elem["text"]
            jsonAux["Polaridade"] = "Neutra"
            jsonClassificadoPolaridadeAux.append(jsonAux)
        elif polaridadeAux > 0:
            jsonAux["Postagem"] = elem["text"]
            jsonAux["Polaridade"] = "Positiva"
            jsonClassificadoPolaridadeAux.append(jsonAux)
        if polaridadeAux < 0:
            jsonAux["Postagem"] = elem["text"]
            jsonAux["Polaridade"] = "Negativa"
            jsonClassificadoPolaridadeAux.append(jsonAux)
    return jsonClassificadoPolaridadeAux

def verificaRepetidos(valoresTipo):
    # Define o objeto que armazenará os índices de cada elemento:
    keys = defaultdict(list);
    jsonAux = {}
    # Percorre todos os elementos da lista:
    for key, value in enumerate(valoresTipo):
        # Adiciona o índice do valor na lista de índices:
        keys[value].append(key)
    # Exibe o resultado:
    for value in keys:
        # if len(keys[value]) > 1:
        if max(keys) == value:
            # print(value, keys[value])
            jsonAux["Valor"] = value
            jsonAux["Indices"] = keys[value]
    return jsonAux
# print(verificaRepetidos([1,3,2,2,5,3,5]))
# exit()

def classificaTipo(emoticonsBD, postagensAux):
    jsonClassificadoTipoAux = []
    for elem in postagensAux:
        valorMaxRepetidoTipo = {} #Armazena os tipos mais predominantes para cada postagem
        jsonAux = {}
        listAuxTipos = [] #Armazena os valores dos tipos presentens na sentença
        elogioAux, criticaAux, duvidaAux, comparacaoAux, ajudaAux, sugestaoAux = 0, 0, 0, 0, 0, 0
        for elem2 in emoticonsBD:
            if (elem["text"].find(elem2["Emoticon"])) >= 0:
                if elem2["Tipo"] == "Elogio":
                    elogioAux += 1
                elif elem2["Tipo"] == "Crítica":
                    criticaAux += 1
                elif elem2["Tipo"] == "Dúvida":
                    duvidaAux += 1
                elif elem2["Tipo"] == "Comparação":
                    comparacaoAux += 1
                elif elem2["Tipo"] == "Ajuda":
                    ajudaAux += 1
                elif elem2["Tipo"] == "Sugestão":
                    sugestaoAux += 1
        listAuxTipos.append(elogioAux)
        listAuxTipos.append(criticaAux)
        listAuxTipos.append(duvidaAux)
        listAuxTipos.append(comparacaoAux)
        listAuxTipos.append(ajudaAux)
        listAuxTipos.append(sugestaoAux)
        valorMaxRepetidoTipo = verificaRepetidos(listAuxTipos)

        # print(valorMaxRepetidoTipo)
        # exit()
        jsonAux["Postagem"] = elem["text"]
        jsonAux["Tipo"] = []
        for i in valorMaxRepetidoTipo["Indices"]:
            if i == 0:
                jsonAux["Tipo"] += ["Elogio"]
            elif i == 1:
                jsonAux["Tipo"] += ["Crítica"]
            elif i == 2:
                jsonAux["Tipo"] += ["Dúvida"]
            elif i == 3:
                jsonAux["Tipo"] += ["Comparação"]
            elif i == 4:
                jsonAux["Tipo"] += ["Ajuda"]
            elif i == 5:
                jsonAux["Tipo"] += ["Sugestão"]

        jsonClassificadoTipoAux.append(jsonAux)
    return jsonClassificadoTipoAux

# Executa a stack para classificar as postagens
def classificaPostagem(postagensAux):
    classificacaoPolaridade = []
    classificacaoTipo = []
    emoticonBDAux = toFormatJsonEmoticon(".\PlanilhaBDEmoticon.csv")
    emoticonsPolaridade,emoticonsIndefinidos = calculaPolaridade(emoticonBDAux)
    emoticonsTipo = calculaValorDoTipo(emoticonBDAux)

    # classificacaoPolaridade = classificaPolaridade(emoticonsPolaridade, postagensAux)
    classificacaoTipo = classificaTipo(emoticonsTipo,postagensAux)
    # jsonClassificadoPolaridadeAux = []
    # for elem in postagensAux:
    #     polaridadeAux = 0
    #     for elem2 in emoticonsPolaridade:
    #         jsonAux = {}
    #         if (elem["text"].find(elem2["Emoticon"])) >= 0:
    #             if elem2["Polaridade"] == "Positiva":
    #                 polaridadeAux += 1
    #             elif elem2["Polaridade"] == "Negativa":
    #                 polaridadeAux -= 1
    #     if polaridadeAux == 0:
    #         jsonAux["Postagem"] = elem["text"]
    #         jsonAux["Polaridade"] = "Neutra"
    #         jsonClassificadoPolaridadeAux.append(jsonAux)
    #     elif polaridadeAux > 0:
    #         jsonAux["Postagem"] = elem["text"]
    #         jsonAux["Polaridade"] = "Positiva"
    #         jsonClassificadoPolaridadeAux.append(jsonAux)
    #     if polaridadeAux < 0:
    #         jsonAux["Postagem"] = elem["text"]
    #         jsonAux["Polaridade"] = "Negativa"
    #         jsonClassificadoPolaridadeAux.append(jsonAux)
    # return jsonClassificadoPolaridadeAux

    return classificacaoPolaridade
# jsonPostagensClassificadas = classificaPostagem(toFormatJsonData(".\PostagensJsonTotal11-05-2019.json"))
onlyPru = separaPru(toFormatJsonBDPostagens(".\PlanilhaTotal11-05-2019.csv"))
jsonPostagensClassificadasPrus = classificaPostagem(onlyPru)

# pd.DataFrame(jsonPostagensClassificadasPrus).to_excel("../PostagensClassificadas/PostagensPolaridadeJsonTotal11-05-2019.xlsx")
# Verificação de acertos que a classificação de polaridade possui
def verificaAcertos(postagensManual, postagensAutomatico):
    acertos = 0
    erros = 0
    postagensAcertadas = []
    postagensErradas = []
    # print(len(postagensManual))
    # print(len(postagensAutomatico))
    # exit()
    for i in range(len(postagensManual)):
        jsonAcertosAux = {}
        jsonErrosAux = {}
        if postagensManual[i]["Analise de Sentimento"] == postagensAutomatico[i]["Polaridade"]:
            acertos += 1
            jsonAcertosAux = postagensManual[i]
            postagensAcertadas.append(jsonAcertosAux)
        else:
            erros += 1
            jsonErrosAux = postagensManual[i]
            postagensErradas.append(jsonErrosAux)
    print(len(postagensManual))
    print(acertos)
    print(erros)
verificaAcertos(onlyPru,jsonPostagensClassificadasPrus)
exit()

#Transformar o dicionário de classifica de postagens em csv
dir = "/PostagensClassificadas"
# if "PostagensClassificadas" not in os.listdir("../../AlgoritmoTCC_MicroServicesEmoticons"):
#     print("das")
#     os.mkdir(dir)
# df = pd.DataFrame(jsonPostagensClassificadasPrus)
# df.to_excel("../PostagensClassificadas/PostagensPolaridadeJsonTotal09-05-2019.xlsx")
