import requests
import json
from bs4 import BeautifulSoup as bs
import platform
import math
import os
import pathlib
from io import StringIO
import hashlib
from selenium import webdriver

chromedriver = (
    os.path.join(
            pathlib.Path(__file__).parent.absolute(),
            (
                    "chromedriver_83"
                    if platform.system() == "Linux"
                    else "chromedriver_83.exe"
            )
    )
)

def crawl(parameters):
    fornecedor = parameters["nome"]
    dataInicio = parameters.get("dataInicio", "")
    dataTermino = parameters.get("dataTermino", "")
    quantity = parameters.get("quantity", None)
    clicks = (
        int(math.ceil(quantity/10))
        if quantity
        else None
    )

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    driver = webdriver.Chrome(
        executable_path=chromedriver, chrome_options=options
    )

    driver.get("https://www.consumidor.gov.br/pages/indicador/relatos/abrir")

    js_parameters = StringIO()
    py_parameters = {"fornecedor": fornecedor, "dataInicio": dataInicio, "dataTermino": dataTermino, "clicks": clicks}
    json.dump(py_parameters, js_parameters)

    injected_javascript = (
        '''
    done = arguments[0];
    (({
        palavrasChave = "",
        segmentoMercado = "Selecione",
        fornecedor = "Selecione",
        area = "Selecione",
        assunto = "Selecione",
        problema = "Selecione",
        regiao = "Selecione",
        uf = "Selecione",
        cidade = "Selecione",
        dataInicio = "",
        dataTermino = "",
        avaliacao = "Selecione",
        nota = "Selecione",
        clicks = null
    }) => {
            var running = false;
            var csv = "";
            var adjust = _=>_.innerText.replace(/[\\t\\n]/g,' ').replace(/[\\\\]/g,'\\\\\\\\').replace(/\\s\\s+/g, ' ').trim()
        window["applicaRelatos"] = (b,a) => {
            if (b) {
                $("#resultados").html(a);
                scrollToAnchor($(".dropdown-toggle"));
                $('[data-toggle="dropdown"]').parent().removeClass("open")
            } else {
                $("#resultados").append(a)
            }
            if (primeiroProximoIndice < 0) {
                $("#btn-mais-resultados").attr("disabled", "disabled");
                if (b) {
                    $("#btn-mais-resultados").addClass("hidden");
                    geraContador()
                }
            } else {
                $("#btn-mais-resultados").removeAttr("disabled");
                $("#btn-mais-resultados").removeClass("hidden");
                geraContador()
            }
            realcaBusca()
            //FUN PART!
            if(running){
                if (!document.querySelector('#btn-mais-resultados').hasAttribute('disabled') && primeiroProximoIndice != '-1') {
                    if (clicks === null) document.querySelector("#btn-mais-resultados").click();
                    else if (--clicks>0) document.querySelector("#btn-mais-resultados").click();
                    else finalizar();
                    }
                else finalizar();
            }
        }
            window["setDropdown"] = (selector, value) => {
                const valueIndex = csv=[].slice.call(document.querySelectorAll(`${selector} option`)).filter(e=>e.innerHTML===value)[0].index;
                document.querySelector(`${selector}`).selectedIndex = valueIndex;
            }
            
            window["setInput"] = (selector, value) => {
                document.querySelector(`${selector}`).value = value;
            }
            dropdownForm = {
                "#segmentoMercado" : segmentoMercado,
                "#fornecedor" : fornecedor,
                "#area" : area,
                "#assunto" : assunto,
                "#problema" : problema,
                "#regiao" : regiao,
                "#uf" : uf,
                "#cidade" : cidade,
                "#avaliacao" : avaliacao,
                "#nota" : nota
            };
            
            inputForm = {
                "#palavrasChave" : palavrasChave,
            "#dataInicio" : dataInicio,
            "#dataTermino" : dataTermino
            };
            
            for (key in dropdownForm) setDropdown(key, dropdownForm[key]);
            for (key in inputForm) setInput(key, inputForm[key]);
        
            window.setTimeout(()=>{
            document.querySelector('#btn-pesquisar').click();
            running = true;
            }, 5000);
        function finalizar() {
            running = false;
            csv=[].slice.call(document.querySelectorAll("#resultados > div.cartao-relato.conteudoEstatico")).map(e=>{
                empresa			= adjust(e.querySelector("h3[class=relatos-nome-empresa]"));
                [predate, cidade]	= adjust(e.querySelector("span[class=relatos-data]")).split(",").map(e=>e.trim());
                predate = predate.split("/");
                date = `${predate[2]}-${predate[1]}-${predate[0]}T00:00:00.000+00:00`;
                relato			= adjust(e.querySelector("div:nth-child(3) > p"));
                resposta 		= adjust(e.querySelector("div:nth-child(4) > p"));
                    pre_nota		= e.querySelector("div:nth-child(5) > p:nth-child(2)").innerText.replace(/\\D/g,'').trim(); // digits only
                nota 			= pre_nota === '' ? '-' : pre_nota;
                    pre_avaliacao	= e.querySelector("div:nth-child(5) > p:nth-child(3)");
                avaliacao		= pre_avaliacao ? adjust(pre_avaliacao) : '-';
                
                return `{"company": "${empresa.replace(/\\"/g, "\\\\\\"")}", "date": "${date.replace(/\\"/g, "\\\\\\"")}", "city": "${cidade.replace(/\\"/g, "\\\\\\"")}", "nota": "${nota.replace(/\\"/g, "\\\\\\"")}", "relato": "${relato.replace(/\\"/g, "\\\\\\"")}", "resposta": "${resposta.replace(/\\"/g, "\\\\\\"")}", "avaliacao": "${avaliacao.replace(/\\"/g, "\\\\\\"")}"}`;
                
            }).join(',\\n');
            done("["+csv+"]");
        }
        
        })'''
        + (
            '''({entry});
        '''.format(
            entry = js_parameters.getvalue()
            )
        )
    )

    csv = driver.execute_async_script(injected_javascript)

    driver.quit()

    # insert hash
    json_csv = json.loads(csv)
    for j in json_csv:
        h = hashlib.md5()
        h_string = j["company"] + j["date"] + j["city"] + j["relato"]
        h.update(h_string.encode('utf-8'))
        j["hash"] = h.hexdigest()
    string_csv = StringIO()
    json.dump(json_csv, string_csv)

    return string_csv.getvalue()

def name(name):
    s = requests.Session()
    co_json = s.post(
        "https://www.consumidor.gov.br/pages/empresa/listarPorNome.json",
        data={"query": name},
    )
    co_results = json.loads(co_json.text)
    for i in co_results:
        if i["value"] == "-1":
            co_results.remove(i)
    for i in co_results:
        co_html = s.get(
            "https://www.consumidor.gov.br/pages/empresa/" + i["value"] + "/"
        )
        soup = bs(co_html.text, "html.parser")
        co_name = soup.find("div", {"class": "tit-nome"}).text
        i["name"] = co_name
        i["url"] = co_html.url
    co_names = list(
        map(lambda x: {"title": x["name"], "url": x["url"]}, co_results)
    )
    s.close()
    return co_names
