import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Popup, Icon

load_dotenv(".env")

# Autenticação
s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)
print(res.text)  # true

linhas = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca=6073"
).json()
linhas = [l for l in linhas if l["lt"] == "6073" and l["tl"] == 10]
print(linhas)

# Mapa
m = None
for linha in linhas:
    cl = linha["cl"]

    # Paradas (pins azuis)
    paradas = s.get(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={cl}"
    ).json()

    # Onibus tempo real em pins vermelhos e paradas em pins azuis
    pos = s.get(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={cl}"
    ).json()
    onibus = pos.get("vs", [])

    print(cl, "paradas:", len(paradas), "ônibus:", len(onibus))

    if m is None:
        if paradas:
            m = Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=13)
        elif onibus:
            m = Map(location=[onibus[0]["py"], onibus[0]["px"]], zoom_start=13)
        else:
            continue

    for p in paradas:
        Marker(
            location=[p["py"], p["px"]],
            popup=Popup(p["np"], max_width=200),
            icon=Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    for v in onibus:
        Marker(
            location=[v["py"], v["px"]],
            popup=Popup(f"Ônibus {v['p']}", max_width=200),
            icon=Icon(color="red", icon="bus", prefix="fa"),
        ).add_to(m)

if m is None:
    m = Map(location=[-23.5505, -46.6333], zoom_start=12)

m.save("mapa_6073-10.html")

#acessei o mapa com o localhost http://localhost:8000/mapa_6073-10.html