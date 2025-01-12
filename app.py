from fastapi import FastAPI, HTTPException, Query
from typing import Literal, Optional
import pandas as pd
import os
from Scripts.scrape import scrape_vitibrasil_data
from Scripts.clean import extract_table_from_html


app = FastAPI(title="Website Data API", description="API para raspar dados do website VitiBrasil.")

# --- API Endpoints ---
@app.get("/vitibrasil/", summary="Obtém dados do Viti Brasil", description="Raspa dados do VitiBrasil ou carrega dados localmente se a raspagem falhar.")

async def get_vitibrasil_data(
aba: Literal["Produção", "Processamento", "Comercialização", "Importação", "Exportação"] = Query(
        ..., 
        description="A aba para raspar dos dados. Opções incluem: Produção, Processamento, Comercialização, Importação, and Exportação.",
        example="Processamento"
    ),
    ano: int = Query(
        ..., 
        description="A ano para baixar os dados.",
        example=2023
    ),
    sub_aba: Optional[Literal["Viníferas", "Americanas e híbridas", "Uvas de mesa", "Sem classificação", "Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"]] = Query(
        None, 
        description=(
            "A subaba dentro da aba principal, se aplicável. Por exemplo::\n"
            "- Para 'Processamento': ['Viníferas', 'Americanas e híbridas', 'Uvas de mesa', 'Sem classificação']\n"
            "- Para 'Importação': ['Vinhos de mesa', 'Espumantes', 'Uvas frescas', 'Uvas passas', 'Suco de uva']\n"
            "- Para 'Exportação': ['Vinhos de mesa', 'Espumantes', 'Uvas frescas', 'Suco de uva']"
        ),
        example="Viníferas"
    ),
):
    """
    Recupera os dados, priorizando a extração via web scraping e, em seguida, recorrendo ao arquivo local, caso a raspagem falhe.
    """
    
    aba = aba.capitalize().strip()
    sub_aba = sub_aba.capitalize().strip() if sub_aba else None

    filename = f"vitibrasil_{aba}_{ano}{'_'+sub_aba if sub_aba else ''}.parquet" 
    filepath = os.path.join("data", filename)

    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        html_table = scrape_vitibrasil_data(aba, ano, sub_aba)
        if html_table:
            df = extract_table_from_html(html_table)
             
            if not os.path.exists(filepath):
                df.to_parquet(filepath)  # Save to parquet if scraping successful and if does not exist
            
            return df.to_dict(orient="records")
        
        else:
            raise HTTPException(status_code=500, detail="Falha ao raspar os dados e arquivo local não encontrado.")
    
    except Exception as err: # Catch other potential exceptions

        # If scraping failed or returned empty data, try to load from file
        if os.path.exists(filepath):
            df = pd.read_parquet(filepath)
            print('A raspagem falhou. Arquivo local carregado.')
            
            return df.to_dict(orient="records")
        
        else:
            print(f"Um erro inesperado ocorreu: {err}")
            raise HTTPException(status_code=500, detail=f"Erro código {err}")