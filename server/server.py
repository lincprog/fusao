from flask import Flask, jsonify, request, send_file, send_from_directory, safe_join, abort
from flask_cors import CORS, cross_origin
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
import pathlib
from bson import json_util
from datetime import datetime
from subprocess import DEVNULL, STDOUT, check_call

path_server = pathlib.Path(__file__).parent.absolute()


mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
fusao = mongoclient["fusao"]
col_co = fusao["consumidor"]
col_ra = fusao["reclameaqui"]
col_columns = fusao["columns"]

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
                r["data"]= datetime.strptime(r["data"], "%d/%m/%Y")
                col_co.update_one(r, {"$set": r}, upsert=True)
        
        if "reclameaqui" in parameters:
            print("Loading data from ReclameAQUI.com.br ...")
            ra = parameters["reclameaqui"]
            results_ra = ReclameAqui.crawl(ra["id"], ra["qtdPaginas"], ra["qtdItens"], ra["shortname"], ra["pular"])
            for r in results_ra:
                r["dataTime"] = datetime.strptime(r["dataTime"], "%Y-%m-%dT%H:%M:%S")
                col_ra.update_one(r, {"$set": r}, upsert=True)
        
        #TODO: ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~~~
        
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "status": "Internal Server Error"}), 500

        

@app.route("/name", methods=['POST'])
@cross_origin()
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
        columns = parameters["columns"]
        filters = parameters["filters"]
        platforms = parameters["platforms"]
        mongoexport = "mongoexport --db=fusao --collection={collection} --type=csv --fields={fields} --out="+os.path.join(path_server,'temp','{collection}')+".csv {query}"
        query=""
        
        for file in ["consumidor.csv", "reclameaqui.csv", "result.csv"]:
            if os.path.exists(os.path.join(path_server,'temp',file)):
                os.remove(os.path.join(path_server,'temp',file))
        
        for platform in ["consumidor", "reclameaqui"]:
            if platform in platforms:
                params = platforms[platform]
                platform_fields = ",".join(list(map(lambda col_name: col_columns.find_one({"name": col_name}, {platform:1})[platform], columns)))
                dict_query = { "company" : params["company"] }
                if "date" in params:
                    date = params["date"]
                    if date["type"] == "day":
                        print(date["day"]) # alter dict_query
                    elif date["type"] == "interval":
                        date_from = date["from"]
                        date_until = date["until"]
                        print(date["from"],date["until"]) # alter dict_query
                platform_query = "--query=\"{query}\"".format(query = str(dict_query).replace('\'', '\\"')) if "query" in params else query
                platform_mongoexport = mongoexport.format(collection = platform, fields = platform_fields, query = platform_query)
                check_call(platform_mongoexport, stdout=DEVNULL, stderr=STDOUT)
        
        with open(os.path.join(path_server,'temp','result.csv'), 'w', encoding='utf-8') as result_csv:
            cols = ",".join(columns)
            result_csv.write("platform," + cols + '\n')
            for filename in ["consumidor", "reclameaqui"]:
                if os.path.exists(os.path.join(path_server,'temp',filename+'.csv')):
                    with open(os.path.join(path_server,'temp',filename+'.csv'), 'r', encoding='utf-8') as read_csv:
                        next(read_csv)  #skip header
                        for line in read_csv:
                            result_csv.write(filename + "," + line)
        
        return send_from_directory(os.path.join(path_server,'temp'), filename="result.csv", as_attachment=True)
    except:
        raise Exception()
        return jsonify({"success": False, "status": "Internal Server Error"}), 500

app.run(debug=True, host='0.0.0.0')


#ra_nome = soup.find('div', {'class' :'tit-nome'}).text