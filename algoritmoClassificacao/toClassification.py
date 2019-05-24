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
    print(postagensDF.head())
    exit()
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

def verificaMaximoRepetidos(valoresTipo):
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

# Função para calcular a polaridade principal de cada emoticon
def calculaPolaridade(jsonBD):
    emoticonPolaridade = []
    emoticonIndefinido = []
    # {'id': 0, 'Emoticon': '😂', 'Positiva': 9, 'Neutra': 7,
    #  'Negativa': 7, 'Crítica': 7, 'Elogio': 8, 'Dúvida': 4,
    #  'Comparação': 4, 'Sugestão': 0, 'Ajuda': 0}
    for elem in jsonBD:
        listAuxRepetidos = []
        jsonAux = {}
        listAux = []
        jsonAuxIndefinido = {}
        auxPos = elem["Positiva"]
        auxNeg = elem["Negativa"]
        auxNeu = elem["Neutra"]
        listAux.append(elem["Positiva"])
        listAux.append(elem["Negativa"])
        listAux.append(elem["Neutra"])
        listAuxRepetidos = verificaMaximoRepetidos(listAux)
        # print(len(listAuxRepetidos["Indices"]))
        # exit()
        if len(listAuxRepetidos["Indices"]) == 1:
            if listAuxRepetidos["Indices"][0] == 0:
                jsonAux["Emoticon"] = elem["Emoticon"]
                jsonAux["Polaridade"] = "Positiva"
                emoticonPolaridade.append(jsonAux)
            elif listAuxRepetidos["Indices"][0] == 1:
                jsonAux["Emoticon"] = elem["Emoticon"]
                jsonAux["Polaridade"] = "Negativa"
                emoticonPolaridade.append(jsonAux)
            elif listAuxRepetidos["Indices"][0] == 2:
                jsonAux["Emoticon"] = elem["Emoticon"]
                jsonAux["Polaridade"] = "Neutra"
                emoticonPolaridade.append(jsonAux)
        else:
            jsonAuxIndefinido["Emoticon"] = elem["Emoticon"]
            jsonAuxIndefinido["Polaridade"] = "Indefinida"
            emoticonPolaridade.append(jsonAuxIndefinido)

    return emoticonPolaridade, emoticonIndefinido

# Função para calcular o tipo principal de cada emoticon
def calculaValorDoTipo(jsonBD):
    # {'id': 0, 'Emoticon': '😂', 'Positiva': 9, 'Neutra': 7, 'Negativa': 7, 'Crítica': 7, 'Elogio': 8, 'Dúvida': 4,
     # 'Comparação': 4, 'Sugestão': 0, 'Ajuda': 0}
    emoticonPolaridade = []
    for elem in jsonBD:
        valorMaxRepetidoTipo = []
        listAuxTipos = []
        jsonAux = {}
        auxElogio = elem["Elogio"]; listAuxTipos.append(auxElogio)
        auxCritica = elem["Crítica"]; listAuxTipos.append(auxCritica)
        auxDuvida = elem["Dúvida"]; listAuxTipos.append(auxDuvida)
        auxComparacao = elem["Comparação"]; listAuxTipos.append(auxComparacao)
        auxAjuda = elem["Ajuda"]; listAuxTipos.append(auxAjuda)
        auxSugestao = elem["Sugestão"]; listAuxTipos.append(auxSugestao)
        valorMaxRepetidoTipo = verificaMaximoRepetidos(listAuxTipos)
        # print(valorMaxRepetidoTipo)
        # exit()
        jsonAux["Emoticon"] = elem["Emoticon"]
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
        emoticonPolaridade.append(jsonAux)
    return emoticonPolaridade
# pd.DataFrame(calculaValorDoTipo(toFormatJsonEmoticon(".\PlanilhaBDEmoticon.csv"))).to_csv("TesteTipo.csv")
# print(calculaValorDoTipo(toFormatJsonEmoticon(".\PlanilhaBDEmoticon.csv"))[0])
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

def classificaTipo(emoticonsBD, postagensAux):
    jsonClassificadoTipoAux = []
    for elem in postagensAux:
        # elem = {'ID': 1108482362386591746, 'N°': 2, 'Data': 'Wed Mar 20 21:36:04 +0000 2019',
        #  'text': 'Twitter novo é muito ruim 🙄😂', 'Emojis da Postagem': '🙄(1)', 'PRU/Não-PRU': 'PRU',
        #  'Tipo': 'Crítica', 'Analise de Sentimento': 'Negativa', 'Artefato': 'Twitter for Android'}
        valorMaxRepetidoTipo = {} #Armazena os tipos mais predominantes para cada postagem
        jsonAux = {}
        listAuxTipos = [] #Armazena os valores dos tipos presentens na sentença
        elogioAux, criticaAux, duvidaAux, comparacaoAux, ajudaAux, sugestaoAux = 0, 0, 0, 0, 0, 0
        for elem2 in emoticonsBD:
            if (elem["text"].find(elem2["Emoticon"])) >= 0:
                for elem3 in elem2["Tipo"]:
                    if elem3 == "Elogio":
                        elogioAux += 1
                    elif elem3 == "Crítica":
                        criticaAux += 1
                    elif elem3 == "Dúvida":
                        duvidaAux += 1
                    elif elem3 == "Comparação":
                        comparacaoAux += 1
                    elif elem3 == "Ajuda":
                        ajudaAux += 1
                    elif elem3 == "Sugestão":
                        sugestaoAux += 1
        listAuxTipos.append(elogioAux)
        listAuxTipos.append(criticaAux)
        listAuxTipos.append(duvidaAux)
        listAuxTipos.append(comparacaoAux)
        listAuxTipos.append(ajudaAux)
        listAuxTipos.append(sugestaoAux)
        valorMaxRepetidoTipo = verificaMaximoRepetidos(listAuxTipos)

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
    classificacaoPostagem = [] #Armazena as postagens e suas respectivas classificações
    classificacaoPolaridade = [] #Armazena as polaridades dos emoticons presentes na sentença
    classificacaoTipo = [] #Armazena os tipos referentes aos emoticons presentes na sentença
    emoticonBDAux = toFormatJsonEmoticon(".\PlanilhaBDEmoticon.csv")
    # Calcula a polaridade/tipo para a base de dados dos emoticons
    emoticonsPolaridade, emoticonsIndefinidos = calculaPolaridade(emoticonBDAux)
    emoticonsTipo = calculaValorDoTipo(emoticonBDAux)
    # Calcula a polaridade/tipo para a base de dados de postagens
    classificacaoPolaridade = classificaPolaridade(emoticonsPolaridade, postagensAux)
    classificacaoTipo = classificaTipo(emoticonsTipo, postagensAux)
    #Começa armazenar ambas classificações em uma unica variavel
    classificacaoPostagem = classificacaoPolaridade
    jsonAux = {}
    for i in range(len(classificacaoTipo)):
        jsonAux["Tipo"] = []
        jsonAux["Tipo"] = classificacaoTipo[i]["Tipo"]
        classificacaoPostagem[i].update(jsonAux)


    return classificacaoPostagem
# jsonPostagensClassificadas = classificaPostagem(toFormatJsonData(".\PostagensJsonTotal11-05-2019.json"))
onlyPru = separaPru(toFormatJsonBDPostagens(".\PlanilhaTotal11-05-2019.csv"))
jsonPostagensClassificadasPrus = classificaPostagem(onlyPru)
# df = pd.DataFrame(jsonPostagensClassificadasPrus)
# df = df[["Postagem", "Polaridade", "Tipo"]]
# df.to_excel("../PostagensClassificadas/PostagensPolaridadeJsonTotal11-05-2019.xlsx")
# exit()

# Verificação de acertos que a classificação de polaridade possui
def verificaAcertosPolaridade(postagensManual, postagensAutomatico):
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
    print("Polaridade")
    print("Total Postagens: "+str(len(postagensManual)))
    print("Acertos:"+str(acertos) + " Porcentagem: "+str(round((acertos*100)/len(postagensManual),2)))
    print("Erros: "+str(erros) + " Porcentagem: "+str(round((erros*100)/len(postagensManual),2)))
verificaAcertosPolaridade(onlyPru,jsonPostagensClassificadasPrus)
# exit()

def verificaAcertosTipo(postagensManual, postagensAutomatico):
    acertos = 0
    erros = 0
    postagensAcertadas = []
    postagensErradas = []
    # tipoAuxManual = postagensManual[3]["Tipo"].replace(" ","").split(",")
    # tipoAuxAutomatico = postagensAutomatico[3]["Tipo"]
    for i in range(len(postagensManual)):
        jsonAcertosAux = {}
        jsonErrosAux = {}
        tipoAuxManual = postagensManual[i]["Tipo"]
        tipoAuxAutomatico = postagensAutomatico[i]["Tipo"]
        if tipoAuxManual == tipoAuxAutomatico:
            acertos += 1
            jsonAcertosAux = postagensManual[i]
            postagensAcertadas.append(jsonAcertosAux)
        else:
            erros += 1
            jsonErrosAux = postagensManual[i]
            postagensErradas.append(jsonErrosAux)
    print("Tipo")
    print("Total Postagens: "+str(len(postagensManual)) )
    print("Acertos:"+str(acertos) + " Porcentagem: "+str(round((acertos*100)/len(postagensManual),2)))
    print("Erros: "+str(erros) + " Porcentagem: "+str(round((erros*100)/len(postagensManual),2)))
verificaAcertosTipo(onlyPru, jsonPostagensClassificadasPrus)
exit()
#Transformar o dicionário de classifica de postagens em csv
# dir = "/PostagensClassificadas"
# if "PostagensClassificadas" not in os.listdir("../../AlgoritmoTCC_MicroServicesEmoticons"):
#     print("das")
#     os.mkdir(dir)
# df = pd.DataFrame(jsonPostagensClassificadasPrus)
# df.to_excel("../PostagensClassificadas/PostagensPolaridadeJsonTotal09-05-2019.xlsx")
