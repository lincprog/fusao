from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
import pymongo
import os
import pathlib
from datetime import datetime
from subprocess import DEVNULL, STDOUT, check_call
import json

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
fusao = mongoclient["fusao"]
#db_cols = {"columns": fusao["columns"]}

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)
    
for platform in config["platforms"]:
    exec("import " + platform['crawler'])

#for platform in config['platforms']:
#    db_cols[platform["name"]] = fusao[platform["name"]]

path_server = pathlib.Path(__file__).parent.absolute()
app = Flask(__name__)

@app.route("/")
@cross_origin()
def inicio():
    return "Bem vindo a API Fusao"

@app.route("/analysis", methods=['POST'])
@cross_origin()
def analysis():
    try:
        if not request.is_json:
            raise Exception()
    except:
        return jsonify({"success": False, "status": "Bad Request"}), 400
    try:
        parameters = request.get_json()
        for platform in config["platforms"]:
            if platform["name"] in parameters:
                results_platform = {}
                print("Loading data from " + platform["name"] +" ...")
                parameters_platform = parameters[platform["name"]]
                results_platform = eval('json.loads(' + platform['crawler'] + '.crawl(parameters_platform))')
                for r in results_platform:
                    r[platform["dateField"]] = datetime.strptime(r[platform["dateField"]], platform["datePattern"])
                    #print('updating ' + platform["name"])
                    db_result = fusao[platform["name"]].update_one(r, {"$set": r}, upsert=True)
                    #message_jrl = "inserido" if db_result.raw_result['nModified'] == 0 else "alterado"
                    #print(message_jrl)
                    db_result_id = db_result.raw_result['upserted'] if db_result.raw_result['nModified'] == 0 else fusao[platform["name"]].find_one(r, {"_id":1})["_id"]
                    fusao["permission"].insert_one({"uid":"user_id", "collection":platform["name"], "rid":db_result_id})
                
        
        #TODO: ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~~~
        
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "status": "Internal Servder Error"}), 500

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
        
        results = {"success": True}
        for platform in config["platforms"]:
            if platform["name"] in platforms:
                exec("results[platform['name']] = json.loads(" + platform['crawler'] + ".name(name))")
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"success": False, "status": "Internal Server Error"}), 500

@app.route("/export", methods=['POST'])
@cross_origin()
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
        
        files = ["result.csv"]
        for platform in config["platforms"]:
            files.append(platform["name"] + ".csv")
        for file in files:
            if os.path.exists(os.path.join(path_server,'temp',file)):
                os.remove(os.path.join(path_server,'temp',file))
        
        for platform in [x["name"] for x in config["platforms"]]:
            if platform in platforms:
                params = platforms[platform]
                platform_fields = ",".join(list(map(lambda col_name: fusao["columns"].find_one({"name": col_name}, {platform:1})[platform], columns)))
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
            for filename in [x["name"] for x in config["platforms"]]:
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