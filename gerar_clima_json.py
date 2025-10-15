import requests
import json
from datetime import datetime

API_KEY = "0d58ccefba2ae9d5e16aca126eed7f83"  # Substitua pela sua chave da OpenWeather
CIDADES = [
    {"nome": "Maceió", "query": "Maceio,BR"},
    {"nome": "Arapiraca", "query": "Arapiraca,BR"},
    {"nome": "Delmiro Gouveia", "query": "Delmiro Gouveia,BR"},
    {"nome": "Penedo", "query": "Penedo,BR"}
]
ARQUIVO_SAIDA = "clima_alagoas.json"

def pegar_clima(cidade_query):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade_query}&units=metric&lang=pt_br&appid={API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        dados = resp.json()
        return {
            "temp": round(dados["main"]["temp"], 1),
            "icone": dados["weather"][0]["icon"],
            "descricao": dados["weather"][0]["description"].capitalize()
        }
    except Exception as e:
        print(f"Erro ao buscar {cidade_query}: {e}")
        return {"temp": None, "icone": "00n", "descricao": "Erro"}

def gerar_json():
    resultado = {"cidades": [], "atualizado_em": datetime.utcnow().isoformat() + "Z"}
    for c in CIDADES:
        clima = pegar_clima(c["query"])
        resultado["cidades"].append({
            "nome": c["nome"],
            "temp": clima["temp"],
            "icone": clima["icone"],
            "descricao": clima["descricao"]
        })

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo '{ARQUIVO_SAIDA}' atualizado com sucesso às {resultado['atualizado_em']}.")

if __name__ == "__main__":
    gerar_json()
