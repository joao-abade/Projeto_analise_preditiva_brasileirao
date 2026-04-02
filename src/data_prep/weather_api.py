import requests

def buscar_clima(local, data):
    
    key = "SUA CHAVE AQUI"
    unitgroup = "metric"
    contenttype = "json"
    include = "days"
    
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{local}/{data}/{data}?unitGroup={unitgroup}&include={include}&key={key}&contentType={contenttype}"
    
    resposta = requests.get(url)
    
    dados = resposta.json()
    
    temperatura = dados["days"][0]["temp"]
    chuva = dados["days"][0]["precip"]
    condicao = dados["days"][0]["conditions"]
    
    return temperatura, chuva, condicao

    
    