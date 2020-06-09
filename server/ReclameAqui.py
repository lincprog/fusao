import urllib.request
import json
import pymongo

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
fusao = mongoclient["fusao"]
col_co = fusao["consumidor"]
col_ra = fusao["reclameaqui"]
ra_json = []


def retry_http_get(url):
    while True:
        try:
            file = urllib.request.urlopen(url)
            return file
        except Exception as e:
            print("-> " + str(e.reason))


def crawl(id, qtdPaginas, qtdItens, nome, pular):

    for i in range(qtdPaginas):  # For each page:
        # Calls the main url
        # print('### --> /'+str(qtdItens)+'/'+str(qtdItens * (i+pular))+'?company='+str(id))
        req = urllib.request.Request(
            url="https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/"
            + str(qtdItens)
            + "/"
            + str(qtdItens * (i + pular))
            + "?company="
            + str(id),  # +'&evaluated=bool:true',
            origin_req_host="https://www.reclameaqui.com.br",
            headers={
                "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                "Referer": "https://www.reclameaqui.com.br/empresa/"
                + nome
                + "/lista-reclamacoes/?pagina="
                + str(i + pular + 1),
            },
        )  # Headers for a well-formed browser request
        pagina = urllib.request.urlopen(req).read().decode("utf-8")
        pagina_json = json.loads(pagina)
        reclamacoes = pagina_json["complainResult"]["complains"][
            "data"
        ]  # here lay our treasures

        # Gets details
        for reclamacao in reclamacoes:
            if not col_ra.find({"hash": reclamacao["id"]}).count() > 0:
                # For the lines below, a function can be written for preprocessing.
                # E.g.: to clean the eventual \t's, that can cause malfunctioning cell delimiter, or <br /> etc
                title = (
                    reclamacao["title"]
                    if "title" in reclamacao.keys() and reclamacao["title"]
                    else "-"
                )
                city = (
                    reclamacao["userCity"]
                    if "userCity" in reclamacao.keys()
                    and reclamacao["userCity"]
                    else "-"
                )
                state = (
                    reclamacao["userState"]
                    if "userState" in reclamacao.keys()
                    and reclamacao["userState"]
                    else "-"
                )
                hash = (
                    reclamacao["id"]
                    if "id" in reclamacao.keys() and reclamacao["id"]
                    else "-"
                )
                dataTime = (
                    reclamacao["created"]
                    if "created" in reclamacao.keys() and reclamacao["created"]
                    else "-"
                )
                complaint = (
                    reclamacao["description"]
                    if "description" in reclamacao.keys()
                    and reclamacao["description"]
                    else "-"
                )
                finalreply = (
                    reclamacao["evaluation"]
                    if "evaluation" in reclamacao.keys()
                    and reclamacao["evaluation"]
                    else "-"
                )
                # Below, the code for 'status' is based on getStatusComplain function from ReclameAqui's web client
                # Yes, it looks horrible, but the intention here is to expect PRECISELY the same behavior
                status = "-"
                if (
                    not reclamacao["evaluated"]
                    and len(reclamacao["interactions"]) > 1
                ):
                    status = "Réplica"
                elif reclamacao["evaluated"]:
                    status = (
                        "Resolvido" if reclamacao["solved"] else "Não resolvido"
                    )
                elif reclamacao["status"] == "ANSWERED":
                    status = "Respondido"
                elif reclamacao["status"] == "PENDING":
                    status = "Não respondido"
                wouldBuyAgain = "-"
                wouldBuyAgain = (
                    reclamacao["dealAgain"]
                    if "dealAgain" in reclamacao.keys()
                    and isinstance(reclamacao["dealAgain"], bool)
                    else "-"
                )
                score = (
                    reclamacao["score"]
                    if "score" in reclamacao.keys() and reclamacao["score"]
                    else "-"
                )

                # print("-> "+'https://www.reclameaqui.com.br/x/x_'+hash) # For each one of the complains, let's get the company and user messages
                rec_req = urllib.request.Request(
                    url="https://iosite.reclameaqui.com.br/raichu-io-site-v1/complain/public/"
                    + hash,
                    origin_req_host="https://www.reclameaqui.com.br",
                    headers={
                        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                        "Referer": "https://www.reclameaqui.com.br/empresa/"
                        + nome
                        + "/lista-reclamacoes/?pagina="
                        + str(i + pular + 1),
                    },
                )  # Headers for a well-formed browser request
                rec_pagina = retry_http_get(rec_req).read().decode("utf-8")
                rec_pagina_json = json.loads(rec_pagina)
                companyreply = "-"
                userreply = "-"
                if (
                    "interactions" in rec_pagina_json.keys()
                    and len(rec_pagina_json["interactions"]) >= 1
                ):  # if there are interactions
                    interactions = list(
                        filter(
                            lambda x: not x["deleted"],
                            rec_pagina_json["interactions"],
                        )
                    )  # remove the deleted messages
                    interactions = list(
                        map(
                            lambda x: {
                                "message": x["message"],
                                "type": x["type"],
                            },
                            interactions,
                        )
                    )  # clean not-used key-value pairs
                    # now we have our filtered-and-mapped interactions
                    answers = list(
                        filter(lambda x: x["type"] == "ANSWER", interactions)
                    )  # For all the companie answers:
                    if answers:
                        companyreply = answers[0][
                            "message"
                        ]  # take the first one
                    # if "interactions" in rec_pagina_json.keys() and len(rec_pagina_json["interactions"]) >= 2 : # if there are more than one interaction
                    # the above line can be omitted
                    replys = list(
                        filter(lambda x: x["type"] == "REPLY", interactions)
                    )  # For all the user replys:
                    if replys:
                        userreply = replys[0]["message"]  # take the first one

                # Now let's write the register:
                registro = {
                    "company": nome,
                    "title": title,
                    "city": city,
                    "state": state,
                    "hash": hash,
                    "dataTime": dataTime,
                    "complaint": complaint,
                    "companyreply": companyreply,
                    "userreply": userreply,
                    "finalreply": finalreply,
                    "status": status,
                    "wouldBuyAgain": wouldBuyAgain,
                    "score": score,
                }
                ra_json.append(registro)
            else:
                print(reclamacao["id"] + " already saved... ")
    return ra_json
