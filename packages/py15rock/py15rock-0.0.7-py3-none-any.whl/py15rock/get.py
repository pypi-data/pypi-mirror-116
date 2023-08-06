import requests    
import pandas as pd

#actual api calls
def requestReturning(ticker, endpoint, token):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}', headers={'Authorization': f'{token}'})
    df = pd.read_json(r.content)
    return df

#api calls for endpoints that require years 
def requestReturningYears(ticker, years, endpoint, token):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}/{years}', headers={'Authorization': f'{token}'})
    df = pd.read_json(r.content)
    return df



def companyCarbon(ticker, token):
    df = requestReturning(ticker, "carbon-footprint", token)
    return df

def companyIndustryAverage(ticker, token):
    df = requestReturning(ticker, "industry-average", token)
    return df

def companyNetincomeCarbon(ticker, token):
    df = requestReturning(ticker, "netincome-carbon", token)
    return df

def company15rockScore(ticker, token):
    df = requestReturning(ticker, "15rock-globalscore", token)
    return df

def companyInfo(ticker, token):
    df = requestReturning(ticker, "", token)
    return df

def companyCalculator(ticker, token):
    df = requestReturning(ticker, "equivalencies_calculator", token)
    return df

def companyIndustrySum(ticker, token):
    df = requestReturning(ticker, "industry-sum", token)
    return df

def companyEmissionsEfficiency(ticker, token):
    df = requestReturning(ticker, "EmissionsEfficiency", token)
    return df

def companyHistoricalPrices(ticker, token):
    df = requestReturning(ticker, "historicalPrices", token)
    return df


def companySumHistoricCarbon(ticker, years, token):
    df = requestReturningYears(ticker, years, "sumhistoriccarbon", token)
    return df

def companyTempConversation(ticker, years, token):
    df = requestReturningYears(ticker, years, "temperatureconversion", token)
    return df

def companyCarbonAlpha(ticker, years, token):
    df = requestReturningYears(ticker, years, "carbonAlpha", token)
    return df

def companyCarbonTransitionRisk(ticker, years, token):
    df = requestReturningYears(ticker, years, "CarbonTransitonRisk", token)
    return df





def getCompany(ticker, endpoint, token):
    r = requests.get(f'https://api.15rock.com/company/{ticker}/{endpoint}', headers={'Authorization': f'{token}'})
    df = pd.read_json(r.content)
    return df