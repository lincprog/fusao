# Stacks Utilizadas
Flask 
Python 3
Vue Js
MongoDB

# Configuração

Requisitos: [MongoDB](https://www.mongodb.com/) e [Python](https://www.python.org/).
Instale as dependências do projeto:
```sh
$ pip install pymongo selenium flask bs4 requests
```

# Iniciando o servidor
Para iniciar o servidor:
```sh
$ python ./server.py
```
As requisições podem ser feitas agora a [https://127.0.0.1](https://127.0.0.1) ou [https://localhost](https://localhost).
# Rotas configuradas:
As seguintes rotas estão implementadas no servidor:
## /name
A esta rota deverá ser enviada uma requisição ```POST``` contendo um ```JSON``` com o nome da empresa a buscar e as plataformas a pesquisar. Ex.:
```json
{
	"name": "americanas",
	"platforms": ["consumidor", "reclameaqui"]
}
```
A resposta é um json contendo as empresas identificadas em cada plataforma:

```json
{
    "consumidor": [
        {
            "title": "Americanas Viagens",
            "url": "https://www.consumidor.gov.br/pages/empresa/20140206000001411/perfil"
        },
        {
            "title": "Americanas.com",
            "url": "https://www.consumidor.gov.br/pages/empresa/20140206000001407/perfil"
        }
    ],
    "reclameaqui": [
        {
            "companyName": "Americanas Marketplace",
            "count": 67190,
            "created": "2019-08-22T18:13:51",
            "fantasyName": "Americanas Marketplace",
            "finalScore": "7.5",
            "hasVerificada": false,
            "id": "97826",
            "logo": "https://raichu-uploads.s3.amazonaws.com/company_142ed4d8-665f-4124-b401-796783e932a7.png",
            "shortname": "americanas-marketplace",
            "solvedPercentual": "82.1",
            "status": "GOOD",
            "url": "https://www.reclameaqui.com.br/empresa/americanas-marketplace"
        }
	]
}
```
## /analysis
A esta rota deverá ser enviada uma requisição ```POST``` contendo um ```JSON``` com os dados necessários para realizar a análise em cada plataforma. Ex.:
```json
{
	"consumidor": {
		"nome": "Casas Bahia",
		"dataInicio": "02/01/2019",
		"dataTermino": "02/01/2019"
	},
	"reclameaqui": {
		"nome": "Casas Bahia - Loja Online",
		"id": "11871",
		"qtdPaginas": 1,
		"qtdItens": 50,
		"pular": 0
	}
}
```
A resposta é um json contendo o resultado da análise:

```json
{"success":true}
```
## /export
A esta rota deverá ser enviada uma requisição ```POST``` contendo um ```JSON``` com os dados necessários para exportar registros para formato csv. Ex.:
```json
{
	"consumidor": {
		"company": "Casas Bahia",
		"query": {
			"date":
			{
				"type":"day",
				"day":"01/01/2019"
			}
		},
		"fields": ["company", "data", "nota"]
	},
	"reclameaqui": {
		"company": "casas-bahia-loja-online",
		"query": {
			"date":
			{
				"type":"interval",
				"from":"13/03/2020",
				"until":"12/03/2020"
			}
		},
		"fields": ["company", "dataTime", "score"]
	}
}
```
A resposta é um arquivo .zip contendo o(s) arquivo(s) gerado.