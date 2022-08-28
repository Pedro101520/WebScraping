import requests
from bs4 import BeautifulSoup
import json

lista = []
propriedades = []
resposta_final = {}

Response = requests.get('https://storage.googleapis.com/infosimples-public/commercia/case/product.html')
content = Response.content
site = BeautifulSoup(content, 'html.parser')

#Titulo
resposta_final['title'] = site.select_one('h2#product_title').get_text()

#Marca
resposta_final['brand'] = site.select_one('div.brand').get_text()

#Descricao
d = site.find('div', attrs={'class': 'product-details'})
descricao = d.find('p')
#Comando replace, usado para tirar o \n do arquivo .json
s = descricao.text
x = s.replace("\n", "")
resposta_final['description'] = x

#Categoria
categoria = site.find('nav', attrs={'class': 'current-category'})
a_tags = categoria.find_all('a')
#For utilizado para pegar as informações das tags a
for a in a_tags:
    lista.append(a.text)
resposta_final['categories'] = lista

#Nota media
media = site.find('div', attrs={'id': 'comments'})
resposta_final['reviews average score'] = media.select_one('h4').get_text()

#Propriedades
#Infelizmente não consegui deixar a parte das propriedades da forma que eu gostaria
tabela_div = site.find('div', attrs={'id': 'additional-properties'})
tabela = tabela_div.find('table', attrs={'class': 'pure-table pure-table-bordered'})
#For utilizado para pegar as informações das tags tr e td
for row in tabela.tbody.find_all('tr'):
    columns = row.find_all('td')
    if(columns != []):
        Propriedade = columns[0]
        Valor = columns[1]
        propriedades.append(Propriedade.text + "=====" + Valor.text) 
resposta_final['Propriedades'] = [propriedades]

#skus
#Os Arrays foram utilizados para armazenar as imformações extraidas do site
analise_titulo = []
analise_produto = []
analise_antigo = []
analise_disponivel = []
#Aqui utilizei a função findAll com o for para conseguir pegar as informações de tags que possuem a mesma class
produtos = site.findAll('div', attrs={'class': 'card-container'})
for produto in produtos:
    titulo = produto.find('div', attrs={'class': 'sku-name'})
    analise_titulo.append(titulo.text.replace("\n", ""))
    preco = produto.find('div', attrs={'class': 'sku-current-price'})
    preco_antigo = produto.find('div', attrs={'class': 'sku-old-price'})
    disponivel = produto.find('i')
    #Verificação, para imprimir os dados corretamente
    if (preco != None):
         analise_produto.append(preco.text.replace("\n", ""))
    else:
         analise_produto.append("Preco nao disponivel")
    if (preco_antigo != None):
          analise_antigo.append(preco_antigo.text.replace("\n", ""))
    else:
          analise_antigo.append("Preco antigo nao disponivel")
    if (disponivel == None):
          analise_disponivel.append("Produto está disponivel no estoque")
    else:
          analise_disponivel.append("Produto não está disponivel no estoque")
    resposta_final['Produto'] = {
        "Titulo": analise_titulo,
        "Preço": analise_produto,
        "Preço antigo": analise_antigo,
        "Estoque": analise_disponivel
        }

#reviews
#Arryas utilizados para armazenar informações extraidas do site
review_nome = []
review_data = []
review_score = []
review_texto = []
#Função findAll em conjunto do for, para extrair informações de tags com a mesma class
reviews = site.findAll('div', attrs={'class': 'review-box'})
for review in reviews:
      nome = review.find('span', attrs={'class': 'review-username'})
      review_nome.append(nome.text)
      data = review.find('span', attrs={'class': 'review-date'})
      review_data.append(data.text)
      score = review.find('span', attrs={'class': 'review-stars'})
      review_score.append(score.text)
      Texto = review.find('p')
      review_texto.append(Texto.text)

      resposta_final['Reviews'] = {
        "Nome": review_nome,
        "Data": review_data,
        "Score": review_score,
        "Texto": review_texto
        }

#Utilizei o ensure_ascii=False e o encoding='utf-8', para conseguir colocar palavras com acento no arquivo .json
#Utilizei o indent=4, sort_keys=True para deixar o arquivo com uma indentação = 4
json_resposta_final = json.dumps(resposta_final, indent=4, sort_keys=True, ensure_ascii=False)

with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)


