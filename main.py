from fastapi import FastAPI, HTTPException
import pyarrow.parquet as pq
import uvicorn

import json
import geopandas as gpd  # Validar se vamos utilizar

app = FastAPI()

# Request de teste : {"Rua": ["AVENIDA BRIGADEIRO LUÍS ANTÔNIO","RUA SÃO BENTO"]}

parquet_file = 'C:/Users/Bruno/Downloads/df.parquet.gzip'
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

    # Se usar GeoPandas, pode-se utilizar consultas espaciais:
    # geometry = gpd.points_from_xy(df['longitude'], df['latitude'])
    # gdf = gpd.GeoDataFrame(df, geometry=geometry)
    # resultados = gdf[gdf.intersects(some_geometry)]

    if len(resultados) == 0:
        raise HTTPException(status_code=404, detail="Endereços não encontrados.")

    return resultados

# Comando de start da api
# uvicorn main:app --reload

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
