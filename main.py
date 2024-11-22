import json

import geopandas as gpd  # Validar se vamos utilizar
import pyarrow.parquet as pq
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Importação para CORS

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens, altere para origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Request de teste : {"Rua": ["AVENIDA BRIGADEIRO LUÍS ANTÔNIO", "RUA SÃO BENTO"]}

parquet_file = './df.parquet.gzip'
df = pq.read_table(parquet_file).to_pandas()
# gdf = gpd.read_parquet(parquet_file)

@app.post("/buscar_enderecos/")
async def buscar_enderecos(data: dict):
    enderecos_pesquisa = data.get("Rua", [])

    resultados = []
    for logradouro in enderecos_pesquisa:
        ocorrencias = df[df['LOGRADOURO_normalizado'] == logradouro.upper()]
        qtd = len(ocorrencias)
        resultados.append({"Rua": logradouro, "QTD": qtd})

    if len(resultados) == 0:
        raise HTTPException(status_code=404, detail="Endereços não encontrados.")

    return resultados

# Comando de start da api
# uvicorn main:app --reload

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
