# -*- coding: utf-8 -*-
import os
import pandas as pd
import emoji
import json
#import toCsv.toCSV

#Abre um arquivo csv e passa para Json, usando a biblioteca PANDAS
def CsvtoJson(path):
    arqEmoticonCSV = open(path, encoding='utf-8')
    emoticonCsvAux = pd.read_csv(arqEmoticonCSV)
    arqEmoticonCSV.close()
    #emoticonDF = pd.DataFrame(emoticonCsvAux)
    #emoticonJsonAux = emoticonDF.to_json(path)
    print(emoticonCsvAux)
#CsvtoJson(".\PlanilhaBDEmoticon.csv")

#Abre um arquivo Json
def openJson(path):
    arqEmoticonJson = open(path, encoding='utf-8')
    emoticonJsonAux = arqEmoticonJson.read()
    arqEmoticonJson.close()
    emoticonJson = json.loads(emoticonJsonAux)
    return emoticonJson
#emoticonBDAux = openJson(".\JsonBDEmoticon.json")

#Abre um arquivo csv e passa para Json, em uma formatação especifica.
def toFormatJson(path):
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
        jsonAux["id"] = i
        jsonAux["Emoticon"] = a1
        jsonAux["Positiva"] = a2
        jsonAux["Neutra"] = a3
        jsonAux["Negativa"] = a4
        jsonEmoticonAux.append(jsonAux)

    return jsonEmoticonAux

#Abre o csv de Postagens e passa para json
def openCsv(path):
    arqPostagensJson = open(path, encoding='utf-8')
    postagensJsonAux = arqPostagensJson.read()
    arqPostagensJson.close()
    postagensJson = json.loads(postagensJsonAux)

    nova_lista = []
    for v in postagensJson:
        aux = list(v.keys())
        v = v.get(aux[0])
        v["id"] = aux[0]
        nova_lista += [v]
    return nova_lista
#postagensJson = openCsv(".\PostagensJsonTotal09-05-2019.json")
#print(postagensJson)
#postagensJson = toCsv.toCSV

emoticonBDAux = toFormatJson(".\PlanilhaBDEmoticon.csv")

def calculaPolaridade(jsonBD):
    emoticonPolaridade = []
    for elem in jsonBD:
        jsonAux = {}
        auxPos = elem["Positiva"] - elem["Neutra"]
        auxNeg = elem["Negativa"] - elem["Neutra"]
        if(auxPos - auxNeg < 5):#Classifica o emoticon como neutro
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Polaridade"] = "Neutra"
            emoticonPolaridade.append(jsonAux)
        elif(auxPos - auxNeg > 5):#Classifica o emoticon como positivo
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Polaridade"] = "Positiva"
            emoticonPolaridade.append(jsonAux)
        elif(auxPos - auxNeg > -5):#Classifica o emoticon como negativo
            jsonAux["Emoticon"] = elem["Emoticon"]
            jsonAux["Polaridade"] = "Negativa"
            emoticonPolaridade.append(jsonAux)
    return emoticonPolaridade
print(calculaPolaridade(emoticonBDAux))