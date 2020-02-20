#sudo apt-get install -y selenium chromium-browser flask

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def crawl(fornecedor, dataInicio, dataTermino):
    driver = webdriver.ChromeOptions()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    driver.get("https://www.consumidor.gov.br/pages/indicador/relatos/abrir")

    injected_javascript = '''

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
        nota = "Selecione"
    }) => {
            var running = false;
            var csv = "";

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
            /*console.log(b);*/
            if(running){
                if (!document.querySelector('#btn-mais-resultados').hasAttribute('disabled') && primeiroProximoIndice != '-1') {/*console.log("continuar!");*/document.querySelector("#btn-mais-resultados").click();}
                else {/*console.log("finalizar!->");*/finalizar();}
                /*console.log(primeiroProximoIndice);*/
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
            }, 10000);

        function finalizar() {
            running = false;
            /*console.log(",-finalizar!");*/
            //csv = [].slice.call(document.querySelectorAll("#resultados > div > div:nth-child(3) > p")).map(e=>e.innerText).join('\\n');
            csv=[].slice.call(document.querySelectorAll("#resultados > div.cartao-relato.conteudoEstatico")).map(e=>{
                empresa			= e.querySelector("h3[class=relatos-nome-empresa]").innerText.replace(/[\\t\\n]/g,' ').replace(/\\s\\s+/g, ' ').trim();
                [data, cidade]	= e.querySelector("span[class=relatos-data]").innerText.replace(/[\\t\\n]/g,' ').trim().split(",").map(e=>e.trim());
                relato			= e.querySelector("div:nth-child(3) > p").innerText.replace(/[\\t\\n]/g,' ').replace(/\\s\\s+/g, ' ').trim();
                resposta 		= e.querySelector("div:nth-child(4) > p").innerText.replace(/[\\t\\n]/g,' ').replace(/\\s\\s+/g, ' ').trim();
                    pre_nota		= e.querySelector("div:nth-child(5) > p:nth-child(2)").innerText.replace(/\\D/g,'').trim(); // digits only
                nota 			= pre_nota === '' ? '-' : pre_nota;
                    pre_avaliacao	= e.querySelector("div:nth-child(5) > p:nth-child(3)");
                avaliacao		= pre_avaliacao ? pre_avaliacao.innerText.replace(/[\\t\\n]/g,' ').replace(/\\s\\s+/g, ' ').trim() : '-';
                
                //return `${empresa}\\t${data}\\t${cidade}\\t${nota}\\t${relato}\\t${resposta}\\t${avaliacao}`; //`"${relato}"`;
                return `{"empresa": "${empresa.replace(/\\"/g, "\\\\\\"")}", "data": "${data.replace(/\\"/g, "\\\\\\"")}", "cidade": "${cidade.replace(/\\"/g, "\\\\\\"")}", "nota": "${nota.replace(/\\"/g, "\\\\\\"")}", "relato": "${relato.replace(/\\"/g, "\\\\\\"")}", "resposta": "${resposta.replace(/\\"/g, "\\\\\\"")}", "avaliacao": "${avaliacao.replace(/\\"/g, "\\\\\\"")}"}`;
                
            }).join(',\\n');
            //console.log("["+csv+"]");
            done("["+csv+"]");
            /*console.log(csv);*/
        }
        
        })({
        fornecedor : "'''+fornecedor+'''",
        dataInicio : "'''+dataInicio+'''",
        dataTermino : "'''+dataTermino+'''",
        });
        '''

    csv = driver.execute_async_script(injected_javascript)

    driver.quit()

    return csv