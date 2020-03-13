from flask import Flask, jsonify, request, send_file, send_from_directory, safe_join, abort
from bs4 import BeautifulSoup as bs
import urllib
import urllib.parse
import json
import requests
import consumidor
import ReclameAqui
import pymongo
import os
from csv import writer
from csv import reader
from zipfile import ZipFile

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
fusao = mongoclient["fusao"]
col_co = fusao["consumidor"]
col_ra = fusao["reclameaqui"]

app = Flask(__name__)


@app.route("/")
def inicio():
    return "Bem vindo a API Fusao"


@app.route("/analysis", methods=['POST'])
def analysis():
    try:
        if not request.is_json:
            raise Exception()
    except:
        return jsonify({"success": False, "status": "Bad Request"}), 400
    try:
        parameters = request.get_json()
        
        if "consumidor" in parameters:
            print("Loading data from Consumidor.gov.br ...")
            co = parameters["consumidor"]
            results_co = json.loads(consumidor.crawl(co["nome"], co["dataInicio"], co["dataTermino"]))
            for r in results_co:
                col_co.update_one(r, {"$set": r}, upsert=True)
        
        if "reclameaqui" in parameters:
            print("Loading data from ReclameAQUI.com.br ...")
            ra = parameters["reclameaqui"]
            results_ra = ReclameAqui.crawl(ra["id"], ra["qtdPaginas"], ra["qtdItens"], ra["shortname"], ra["pular"])
            for r in results_ra:
                col_ra.update_one(r, {"$set": r}, upsert=True)
        
        #TODO: ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~~~
        
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "status": "Internal Server Error"}), 500

        

@app.route("/name", methods=['POST'])
def name():
    try:
        if not request.is_json:
            raise Exception()
    except:
        return jsonify({"success": False, "status": "Bad Request"}), 400
    try:
        parameters = request.get_json()
        name = parameters["name"]
        platforms = parameters["platforms"]
        
        if "consumidor" in platforms:
            s = requests.Session()
            co_json = s.post('https://www.consumidor.gov.br/pages/empresa/listarPorNome.json', data={"query": name})
            co_results = json.loads(co_json.text)
            for i in co_results:
                if i["value"]=="-1":
                    co_results.remove(i)
            for i in co_results:
                co_html = s.get('https://www.consumidor.gov.br/pages/empresa/'+i['value']+'/')
                soup = bs(co_html.text, 'html.parser')
                co_name = soup.find('div', {'class' :'tit-nome'}).text
                i["name"] = co_name
                i["url"] = co_html.url
            co_names = list(map(lambda x: {"title": x["name"], "url": x["url"]}, co_results))
            s.close()
        
        if "reclameaqui" in platforms:
            s = requests.Session()
            name_encoded = urllib.parse.quote(name, safe='')
            print('https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/'+name_encoded)
            print(name_encoded)
            ra_json = s.get('https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/'+name_encoded)
            print(ra_json.text)
            ra_results = json.loads(ra_json.text)
            for r in ra_results["companies"]:
                r["url"] = "https://www.reclameaqui.com.br/empresa/"+r["shortname"]
            s.close()
        
        results = {"success": True}
        if "consumidor" in platforms:
            results["consumidor"] = co_names
        if "reclameaqui" in platforms:
            results["reclameaqui"] = ra_results["companies"]
        return jsonify(results)
    except:
        return jsonify({"success": False, "status": "Internal Server Error"}), 500

@app.route("/export", methods=['POST'])
def export():
    try:
        if not request.is_json:
            raise Exception()
    except:
        return jsonify({"success": False, "status": "Bad Request"}), 400
    try:
        parameters = request.get_json()
        platforms = parameters
        mongoexport = "mongoexport --db=fusao --collection={collection} --type=csv --fields={fields} --out=./temp/{collection}.csv {query}"
        query=""
        
        if os.path.exists('./temp/mongoexport.csv'):
            os.remove('./temp/mongoexport.csv')
        if os.path.exists('./temp/reclameaqui.csv'):
            os.remove('./temp/reclameaqui.csv')
        if os.path.exists('./temp/consumidor.csv'):
            os.remove('./temp/consumidor.csv')
        if os.path.exists('./temp/result.zip'):
            os.remove('./temp/result.zip')
        
        if "consumidor" in platforms:
            consumidor = platforms["consumidor"]
            co_fields = ",".join(consumidor["fields"])
            co_query = query #co_query = "--query='\{query}\'".format(query=consumidor["query"]) if "query" in consumidor else query
            co_mongoexport = mongoexport.format(collection="consumidor", fields=co_fields, query=co_query)
            os.system(co_mongoexport)
        
        if "reclameaqui" in platforms:
            reclameaqui = platforms["reclameaqui"]
            ra_fields = ",".join(reclameaqui["fields"])
            ra_query = query #co_query = "--query='\{query}\'".format(query=reclameaqui["query"]) if "query" in reclameaqui else query
            ra_mongoexport = mongoexport.format(collection="reclameaqui", fields=ra_fields, query=ra_query)
            os.system(ra_mongoexport)
                
        with ZipFile('./temp/result.zip', 'w') as f_zip:
            if os.path.exists('./temp/reclameaqui.csv'):
                f_zip.write('./temp/reclameaqui.csv')
            if os.path.exists('./temp/consumidor.csv'):
                f_zip.write('./temp/consumidor.csv')
        
        return send_from_directory('./temp', filename="result.zip", as_attachment=True)
    except:
        return jsonify({"success": False, "status": "Internal Server Error"}), 500

app.run(debug=True, host='0.0.0.0')


#ra_nome = soup.find('div', {'class' :'tit-nome'}).text