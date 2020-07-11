import json
import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import pathlib
import math
import platform
from datetime import datetime

import pymongo

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
fusao = mongoclient["fusao"]
col_ra = fusao["reclameaqui"]

chromedriver = (
    "chromedriver_83"
    if platform.system() == "Linux"
    else os.path.join(
            pathlib.Path(__file__).parent.absolute(),
            "chromedriver_83.exe",
        )
)


def crawl(parameters):

    # Getting parameters
    id = parameters["id"]
    name = parameters["name"]
    shortname = parameters["shortname"]
    quantity = parameters["quantity"]
    offset = parameters["offset"]

    items_per_page = 50
    pages = int(math.ceil(quantity/items_per_page))

    # Preparing Selenium options and enabling browser logging
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")
    options.add_argument('headless')
    d = DesiredCapabilities.CHROME
    d["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(
        executable_path=chromedriver, chrome_options=options, desired_capabilities=d
    )

    # accessing page and performing interations
    driver.get(
        "https://www.reclameaqui.com.br/empresa/"
        + shortname
        + "/lista-reclamacoes/"
    )
    assert name + " - Reclame Aqui" in driver.title
    time.sleep(3)

    # capturing data
    for i in range(pages):
        driver.execute_script(
            "$.ajax({url: 'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/"
            + str(items_per_page)
            + "/"
            + str(items_per_page * (i + offset))
            + "?company="
            + str(id)
            + "', context: document.body})"
        )
        driver.execute_script("console.log('" + str(i) + "')")
        time.sleep(1)

    # reading and mapping logs to its contained useful information
    entries = []
    for entry in driver.get_log("performance"):
        entries.append(entry)
    message_response = list(
        map(lambda i: json.loads(i["message"])["message"], entries)
    )

    # reading IDs of desired http responses
    request_ids = []
    for i in message_response:
        if (
            "params" in i
            and i["method"] == "Network.responseReceived"
            and i["params"]["response"]["url"].startswith(
                "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/"
                + str(items_per_page)
            )
        ):
            request_ids.append(i["params"]["requestId"])

    # reading data from http responses
    reclamacoes = []
    for request_id in request_ids:
        response = driver.execute_cdp_cmd(
            "Network.getResponseBody", {"requestId": request_id}
        )
        reclamacoes.extend(
            json.loads(response["body"])["complainResult"]["complains"]["data"]
        )

    # structuring valid data
    ra_json = []
    for reclamacao in reclamacoes:
        if not col_ra.find({"hash": reclamacao["id"]}).count() > 0:
            # For the lines below, a function can be written for preprocessing.
            # E.g.: to clean the eventual \t's, that can cause malfunctioning cell delimiter, or <br /> etc
            registro = {
                "title": "title",
                "hash": "id",
                "date": "created",
                "complaint": "description",
                "finalreply": "evaluation",
                "wouldbuyagain": "dealAgain",
                "score": "score"
                }
            for key, value in registro.items():
                registro[key] = reclamacao.get(value, "-")
            registro["company"] = name
            registro["city"] = "{city} - {state}".format(
                city = reclamacao["userCity"],
                state = reclamacao["userState"]
                )
            registro["date"] = datetime.strptime(registro["date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S.000Z") # Date in correct format
            # Below, the code for 'status' is based on getStatusComplain function from ReclameAqui's web client
            # Yes, it looks horrible, but the intention here is to expect PRECISELY the same behavior
            registro["status"] = "-"
            if (
                not reclamacao["evaluated"]
                and len(reclamacao["interactions"]) > 1
            ):
                registro["status"] = "Réplica"
            elif reclamacao["evaluated"]:
                registro["status"] = (
                    "Resolvido"
                    if reclamacao["solved"]
                    else "Não resolvido"
                )
            elif reclamacao["status"] == "ANSWERED":
                registro["status"] = "Respondido"
            elif reclamacao["status"] == "PENDING":
                registro["status"] = "Não respondido"
            ra_json.append(registro)
        else:
            print(reclamacao["id"] + " already saved... ")

    driver.close()
    return json.dumps(ra_json)


def name(name):
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("headless")

    # enable browser logging
    d = DesiredCapabilities.CHROME
    d["goog:loggingPrefs"] = {"performance": "ALL", "performance": "ALL"}
    driver = webdriver.Chrome(
        chromedriver, options=options, desired_capabilities=d
    )

    # access page and perform interations
    driver.get("https://www.reclameaqui.com.br/")
    assert "Reclame Aqui" in driver.title
    input_search = driver.find_elements_by_css_selector(
        "input[placeholder='Busque por uma empresa, produto ou serviço'][class='form-search input-auto-complete-search']"
    )[0]
    webdriver.ActionChains(driver).move_to_element(
        input_search
    ).click().send_keys(name).perform()
    time.sleep(3)

    entries = []
    for entry in driver.get_log("performance"):
        entries.append(entry)
    message_response = list(
        map(lambda i: json.loads(i["message"])["message"], entries)
    )
    request_id = ""
    for i in message_response:
        if (
            "params" in i
            and i["method"] == "Network.responseReceived"
            and i["params"]["response"]["url"]
            == "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/companies/search/"
            + quote(name)
        ):
            request_id = i["params"]["requestId"]
    response = driver.execute_cdp_cmd(
        "Network.getResponseBody", {"requestId": request_id}
    )

    driver.close()
    return json.loads(response["body"])["companies"]
