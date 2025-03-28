import pandas as pd
import requests
from pathlib import Path
import json
from datetime import datetime

def update_backup():
    print(f"Iniciando atualização em {datetime.now().isoformat()}")
    
    try:
        # Tenta buscar da API
        print("Conectando à API...")
        response = requests.get(
            "https://www.intuitivecare.com.br/api/getapi",
            timeout=30
        )
        response.raise_for_status()
        
        # Verifica o JSON
        data = response.json()
        if not data:
            raise ValueError("API retornou dados vazios")
            
        # Converte para DataFrame e salva
        df = pd.DataFrame(data)
        backup_path = Path("operadoras_backup.csv")
        
        # Faz backup do arquivo antigo se existir
        if backup_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            old_backup = Path(f"operadoras_backup_old_{timestamp}.csv")
            backup_path.rename(old_backup)
            print(f"Backup antigo salvo como {old_backup.name}")
        
        # Salva novo arquivo
        df.to_csv(backup_path, index=False, encoding='utf-8')
        print(f"Backup atualizado com {len(df)} registros")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON da API")
    except ValueError as ve:
        print(f"Problema nos dados: {str(ve)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
    
    return False

if __name__ == "__main__":
    update_backup()