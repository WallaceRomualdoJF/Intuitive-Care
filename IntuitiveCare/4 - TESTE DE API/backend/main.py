from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import requests
from datetime import datetime
import csv
from io import StringIO
from typing import Optional
import json

app = FastAPI(title="API Operadoras de Saúde")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_operadoras_externas():
    """Busca dados das operadoras na API externa com tratamento robusto"""
    try:
        response = requests.get(
            "https://www.intuitivecare.com.br/api/getapi",
            timeout=15,
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        
        # Verificação rigorosa do JSON
        try:
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("Formato de dados inválido")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=502,
                detail=f"Dados inválidos da API externa: {str(e)}"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erro ao acessar API externa: {str(e)}"
        )

@app.get("/api/info")
async def get_api_info():
    """Endpoint de verificação de saúde da API"""
    return {
        "status": "online",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/api/operadoras")
async def get_operadoras(
    status: str = Query("Ativa", description="Filtrar por status"),
    busca: Optional[str] = Query(None, description="Termo de busca")
):
    """Endpoint principal para consulta de operadoras"""
    try:
        data = fetch_operadoras_externas()
        
        # Filtragem segura
        filtered = [
            op for op in data 
            if str(op.get("Status", "")).lower() == status.lower()
        ]
        
        if busca:
            busca = busca.lower()
            filtered = [
                op for op in filtered
                if any(
                    busca in str(valor).lower()
                    for valor in op.values()
                    if valor is not None
                )
            ]
        
        return JSONResponse(content=filtered)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@app.get("/api/operadoras/export/csv")
async def export_operadoras_csv():
    """Endpoint para exportação em CSV"""
    try:
        data = fetch_operadoras_externas()
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado disponível para exportação"
            )
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return FileResponse(
            path=None,
            content=output.getvalue().encode(),
            media_type="text/csv",
            filename=f"operadoras_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na exportação: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)