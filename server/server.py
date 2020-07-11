from flask import Flask, jsonify, request, send_from_directory
from flask_cors import cross_origin
import pymongo
import os
import pathlib
from datetime import datetime
from subprocess import DEVNULL, STDOUT, check_call
import json
import importlib
import lib

path_server = pathlib.Path(__file__).parent.absolute()

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
fusao = mongoclient["fusao"]

config = {}
with open(os.path.join(path_server, "fusaoapi", "crawlers", "config.json")) as json_file:
    config = json.load(json_file)

platform_modules = {}

for platform in config["platforms"]:
    platform_module = importlib.import_module( "fusaoapi.crawlers.{platform}".format(platform = platform) )
    platform_modules[platform] = platform_module
 
app = Flask(__name__)

@app.route("/")
@cross_origin()
def inicio():
    return "Bem vindo a API Fusao"


@app.route("/analysis", methods=["POST"])
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
            if platform in parameters:
                results_platform = {}
                print("Loading data from " + platform + " ...")
                parameters_platform = parameters[platform]
                results_platform = json.loads(platform_modules[platform].crawl(parameters_platform))
                for r in results_platform:
                    if "date" in r:
                        r["date"] = datetime.strptime(r["date"], "%Y-%m-%dT%H:%M:%S.000Z")
                    db_result = fusao[platform].update_one(
                        {"hash": r["hash"]}, {"$set": r}, upsert=True
                    )
                    db_result_id = (
                        db_result.raw_result["upserted"]
                        if db_result.raw_result["updatedExisting"] == False
                        else fusao[platform].find_one(r, {"_id": 1})[
                            "_id"
                        ]
                    )

                    obj_permission = {
                        "uid": "user_id",
                        "collection": platform,
                        "rid": db_result_id,
                    }

                    fusao["permission"].update_one(
                        obj_permission,
                        {"$set": obj_permission},
                        upsert=True
                    )

        # TODO: ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~~~

        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return (
            jsonify({"success": False, "status": "Internal Server Error"}),
            500,
        )


@app.route("/name", methods=["POST"])
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
            if platform in platforms:
                results[platform] = platform_modules[platform].name(name)
        return jsonify(results)
    except Exception as e:
        print(e)
        return (
            jsonify({"success": False, "status": "Internal Server Error"}),
            500,
        )


@app.route("/export", methods=["POST"])
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
        mongoexport = (
            "mongoexport --db=fusao --collection={collection} --type=csv --fields={fields} --out="
            + os.path.join(path_server, "temp", "{collection}")
            + ".csv {query}"
        )
        query = ""

        files = ["result.csv"]
        for platform in config["platforms"]:
            files.append(platform + ".csv")
        for file in files:
            if os.path.exists(os.path.join(path_server, "temp", file)):
                os.remove(os.path.join(path_server, "temp", file))

        for platform in [x["name"] for x in config["platforms"]]:
            if platform in platforms:
                params = platforms[platform]
                platform_fields = ",".join(
                    list(
                        map(
                            lambda col_name: fusao["columns"].find_one(
                                {"name": col_name}, {platform: 1}
                            )[platform],
                            columns,
                        )
                    )
                )
                dict_query = {"company": params["company"]}
                if "date" in params:
                    date = params["date"]
                    if date["type"] == "day":
                        print(date["day"])  # alter dict_query
                    elif date["type"] == "interval":
                        date_from = date["from"]
                        date_until = date["until"]
                        print(date["from"], date["until"])  # alter dict_query
                platform_query = (
                    '--query="{query}"'.format(
                        query=str(dict_query).replace("'", '\\"')
                    )
                    if "query" in params
                    else query
                )
                platform_mongoexport = mongoexport.format(
                    collection=platform,
                    fields=platform_fields,
                    query=platform_query,
                )
                check_call(platform_mongoexport, stdout=DEVNULL, stderr=STDOUT)

        with open(
            os.path.join(path_server, "temp", "result.csv"),
            "w",
            encoding="utf-8",
        ) as result_csv:
            cols = ",".join(columns)
            result_csv.write("platform," + cols + "\n")
            for filename in [x["name"] for x in config["platforms"]]:
                if os.path.exists(
                    os.path.join(path_server, "temp", filename + ".csv")
                ):
                    with open(
                        os.path.join(path_server, "temp", filename + ".csv"),
                        "r",
                        encoding="utf-8",
                    ) as read_csv:
                        next(read_csv)  # skip header
                        for line in read_csv:
                            result_csv.write(filename + "," + line)

        return send_from_directory(
            os.path.join(path_server, "temp"),
            filename="result.csv",
            as_attachment=True,
        )
    except:
        raise Exception()
        return (
            jsonify({"success": False, "status": "Internal Server Error"}),
            500,
        )


app.run(debug=True, host="0.0.0.0")
