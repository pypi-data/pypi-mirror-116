import requests    
import pandas as pd

def getCompany(ticker, endpoint, token):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}', headers={'Authorization': f'{token}'})
    df = pd.read_json(r.content)
    return df