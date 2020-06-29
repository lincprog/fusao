DB = "fusao2"
PLATFORMS = [
 {"name":"consumidor","crawler":"consumidor","dateField":"data","datePattern":"%d/%m/%Y"},
 {"name":"reclameaqui","crawler":"reclame_aqui","dateField":"dataTime","datePattern":"%Y-%m-%dT%H:%M:%S"}
]
FILTERS = [
 {"name":"date","parameters":["from","until"],"available":True},
 {"name":"score","parameters":["min","max"],"available":False}
]
COLUMNS = [
 {"name":"company","consumidor":"company","reclameaqui":"company"},
 {"name":"complaint","consumidor":"relato","reclameaqui":"complaint"},
 {"name":"city","consumidor":"cidade","reclameaqui":"city"},
 {"name":"companyreply","consumidor":"resposta","reclameaqui":"companyreply"},
 {"name":"date","consumidor":"data","reclameaqui":"dataTime"},
 {"name":"evaluation","consumidor":"avaliacao","reclameaqui":"finalReply"},
 {"name":"score","consumidor":"nota","reclameaqui":"score"},
 {"name":"id","consumidor":"_id","reclameaqui":"_id"}
]
LANGUAGE = "english"