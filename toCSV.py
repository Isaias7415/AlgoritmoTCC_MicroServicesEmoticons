# -*- coding: utf-8 -*-
from builtins import set

import os
import pandas as pd
import emoji
import json

# lista = [{"1108510904168169483":{"text":"Boa noite galera! Twitter novo na pista Pois aquele foi removido por motivo de data errada... Segue aí  🤜🤛","data":"Wed Mar 20 23:29:29 +0000 2019","dispositivo":"Twitter for Android"}}]

arqPostagensJson = open(".\PostagensJsonTotal21-04-2019.json", encoding='utf-8')
postagensJsonAux = arqPostagensJson.read()
arqPostagensJson.close()
postagensJson = json.loads(postagensJsonAux)
# print(postagensJson)
# print(len(postagensJson))
# exit()

#-------------------------------------------------------------
#Quando o id for corrigido, basta excluir esse bloco de codigo
# Coloca o id como atributo do json
nova_lista = []
for v in postagensJson:
# for v in lista:
    # print(type(v))
    aux = list(v.keys())
    v = v.get(aux[0])
    v["id"] = aux[0]
    nova_lista += [v]
#-------------------------------------------------------------
# onlyEmoticons = []  # Variavel apra armazenar aepans as postagens com emoticons
# onlyPostAttr = []  # Variavel apra armazenar aepans as postagens sem emoticons

# Separa em dois arrays, um contendo apenas postagens com emoticons e outro contendo as sem emoticons CORRETO
def onlyPostEmoticons(listaPostagens):
    auxPostEmoticons = []
    auxPost = []
    for elem in listaPostagens:
        string_list = [x for x in elem["text"]]
        for elem2 in string_list:
            if elem2 in emoji.UNICODE_EMOJI:
                if elem not in auxPostEmoticons:
                    auxPostEmoticons.append(elem)
                    break
        if elem not in auxPostEmoticons:
            if elem not in auxPost:
                auxPost.append(elem)
    return auxPostEmoticons, auxPost

# Remove as postagens duplicadas CORRETO
def removeDuplicata(auxOnlyEmoticons):
    aux = []
    for elem3 in auxOnlyEmoticons:
        if elem3 not in aux:
            aux.append(elem3)
    return aux

# Verifica a quantidade de emoticons por dispositivo CORRETO
def verificaQtdEmojiDispositivo(auxOnlyEmoticons):
    tweetAndroid = []
    tweetIOS = []
    tweetWebApp = []
    tweetWebClient = []
    tweetIpad = []
    tweetWinPhone = []
    tweetNotCataloged = []
    # print(len(onlyEmoticons))
    for elem4 in auxOnlyEmoticons:
        if elem4["dispositivo"] == "Twitter for Android":
            tweetAndroid.append(elem4)
        elif elem4["dispositivo"] == "Twitter for iPhone":
            tweetIOS.append(elem4)
        elif elem4["dispositivo"] == "Twitter Web App":
            tweetWebApp.append(elem4)
        elif elem4["dispositivo"] == "Twitter Web Client":
            tweetWebClient.append(elem4)
        elif elem4["dispositivo"] == "Twitter for iPad":
            tweetIpad.append(elem4)
        elif elem4["dispositivo"] == "Twitter for Windows Phone":
            tweetWinPhone.append(elem4)
        else:
            tweetNotCataloged.append(elem4)
    print("Android: " + str(len(tweetAndroid)))
    print("iPhone: " + str(len(tweetIOS)))
    print("Web App: " + str(len(tweetWebApp)))
    print("Web Client: " + str(len(tweetWebClient)))
    print("iPad: " + str(len(tweetIpad)))
    print("Windows Phone: " + str(len(tweetWinPhone)))
    print("Not Cataloged: " + str(len(tweetNotCataloged)))

# Metodo para separar apenas os emojis em uma lista
def getEmoticons(auxOnlyEmoticons):
    emojiPostTotal = []  # Guarda todos emojis
    for elem5 in auxOnlyEmoticons:
        string_list = [x for x in elem5["text"]]
        for elem6 in string_list:
            if elem6 in emoji.UNICODE_EMOJI:
                emojiPostTotal.append(elem6)
    return emojiPostTotal

#Metodo para contar a repeitição dos emojis em todas as postagens
def countEmojiRepetidos(auxOnlyEmoticons):
    auxEmojiPost = removeDuplicata(getEmoticons(auxOnlyEmoticons))  # Guarda os emojis sem repetilos
    # jsonEmoticon = {}  # Json, que relaciona EMOJI = QUANTIDADE DE REPETIÇÕES
    listJsonEmoticon = [] # Lista que guarda os dicionários
    for elem7 in auxEmojiPost:  # Guarda os emojis sem repetilos
        jsonEmoticon = {}  # Json que relaciona EMOJI = QUANTIDADE DE REPETIÇÕES
        auxCount = getEmoticons(auxOnlyEmoticons).count(elem7)
        jsonEmoticon["Emoticon"] = elem7
        jsonEmoticon["Quantidade Total"] = auxCount
        # dictAux["Emoticon"] = elem7
        # dictAux["Quantidade Total"] = auxCount
        listJsonEmoticon.append(jsonEmoticon)

    return listJsonEmoticon

# Coleta os emoticons relacionados a cada postagem
def emoticonPostagem(auxOnlyEmoticons):
    # auxEmojis = ""
    listJsonCountEmojiPost = [] #Guarda o numero de vezes que o emoticons se repete por postagem
    # jsonPostEmoticon = {} #Guarda os a contagem dos emoticons relacionado ao post
    for elem8 in auxOnlyEmoticons:
        auxEmojis = ""
        string_list = [x for x in elem8["text"]]
        jsonPostEmoticon = {} #Guarda os a contagem dos emoticons relacionado ao post
        for elem9 in string_list:
            if elem9 in emoji.UNICODE_EMOJI:
                if elem9 not in auxEmojis:
                    jsonPostEmoticon["text"] = elem8["text"]
                    # jsonPostEmoticon[elem9] = string_list.count(elem9)
                    auxEmojis += elem9 + "(" + str(string_list.count(elem9)) + ")"
                    # listJsonCountEmojiPost.append(jsonPostEmoticon)

        jsonPostEmoticon["Emojis"] = auxEmojis
        listJsonCountEmojiPost.append(jsonPostEmoticon)
    return listJsonCountEmojiPost
    # return removeDuplicata(listJsonCountEmojiPost)

# Json, com todas a postagens que possuem emojis , sem duplicatas
# onlyEmoticons = onlyPostEmoticons(nova_lista)

# Json, com todas as postagens que não possuem emojis, sem duplicatas
# onlyPostAttr = onlyPost(nova_lista)

# Novo metodo, que retorna ambos os json com emoticons e sem, separados
onlyEmoticons , withoutEmoticons = onlyPostEmoticons(nova_lista)

print(len(nova_lista))
print(len(removeDuplicata(nova_lista)))
print(len(onlyEmoticons))
print(len(withoutEmoticons))
# exit()
print("Dispositivos Emoticons\n")
verificaQtdEmojiDispositivo(onlyEmoticons)
print("\n")
print("Dispositivos sem Emoticons")
verificaQtdEmojiDispositivo(withoutEmoticons)
# exit()

#Transformar o dicionário de contagem de emoticons por postagem em csv
dir = "/EmoticonPostSeparados"
if "EmoticonPostSeparados" not in os.listdir("../Teste"):
    os.mkdir(dir)
df = pd.DataFrame(emoticonPostagem(onlyEmoticons))
df.to_excel("../AlgoritmoTCC_MicroServicesEmoticons/EmoticonPostSeparados/EmoticonsJsonTotal21-04-2019.xlsx")


#Transformar o dicionário de contagem total de emoticons em csv
dir = "/EmoticonTotaisSeparados"
if "EmoticonTotaisSeparados" not in os.listdir("../Teste"):
    os.mkdir(dir)
df = pd.DataFrame(countEmojiRepetidos(onlyEmoticons))
df = df.sort_values("Quantidade Total", ascending = False)
aux2 = [i for i in range(len(df))]
df.index = aux2
df.to_excel("../AlgoritmoTCC_MicroServicesEmoticons/EmoticonTotaisSeparados/EmoticonsJsonTotal21-04-2019.xlsx")

# Transforma o dicionário de postagem em um csv
df = pd.DataFrame(onlyEmoticons)
df.to_excel("./CSVPOstagensEmoticons/PostagensJsonTotal21-04-2019.xlsx")
# df.to_excel("teste3OP.xlsx")
# df.to_csv("PostagensEmoticons20-03-2019-Adjetivos.csv")
