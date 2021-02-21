import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template

app2 = Flask(__name__)

@app2.route('/')
def home():
    return render_template("home.html")

@app2.route('/conversion', methods=['POST','GET'])
def ExchangeRateUSD_byUI():
    currency_code = request.form['code']
    currency_code = currency_code.upper()
    codeV = {'CurrencyCode': currency_code.split(',')}
    codeV = pd.DataFrame(codeV)
    codeV['CurrencyCode'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    CurrName = []
    CurrUSDrate = []
    page = requests.get('https://www.x-rates.com/table/?from=USD&amount=1')
    soup = BeautifulSoup(page.content, "html.parser")
    Ex_rate = soup.find_all(class_='tablesorter ratesTable')
    Ex_rate_value = Ex_rate[0].text.replace('\n\n', '@')
    Ex_rate_value = Ex_rate_value.replace('\n', '@')
    Ex_rate_value = Ex_rate_value.replace('@@', '@')
    Ex_rate_value = Ex_rate_value.split('@')
    I_rng = 5
    while I_rng <= len(Ex_rate_value) - 3:
        CurrName.append(Ex_rate_value[I_rng])
        I_rng = I_rng + 3

    I_rng = 7
    while I_rng <= len(Ex_rate_value):
        CurrUSDrate.append(Ex_rate_value[I_rng])
        I_rng = I_rng + 3
    CurrDf = {'CurrencyName': CurrName, 'ExRateUSD': CurrUSDrate}
    CurrDf = pd.DataFrame(CurrDf)
    CurrDf = CurrDf.append({'CurrencyName': 'US DOLLAR', 'ExRateUSD': '1'}, ignore_index=True)
    CurrDf['CurrencyName'] = CurrDf['CurrencyName'].str.upper()
    CurrDf['CurrencyName'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    CurrDf['ExRateUSD'] = CurrDf['ExRateUSD'].astype(dtype=np.float64)

    CurrCode = pd.read_excel("refFiles/CurrencyCode.xlsx")
    CurrCode['CurrencyName'] = CurrCode['CurrencyName'].str.upper()
    CurrCode['CurrencyCode'] = CurrCode['CurrencyCode'].str.upper()
    CurrCode['CurrencyName'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    CurrCode['CurrencyCode'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)

    CurrDf = CurrDf.merge(CurrCode, on='CurrencyName', how='left')
    CurrDf = CurrDf.drop_duplicates(subset='CurrencyCode', keep="last")
    CurrDf = CurrDf[['CurrencyCode', 'ExRateUSD']]
    codeV = codeV.merge(CurrDf, on='CurrencyCode', how='left')
    res = []
    for rate in codeV.ExRateUSD:
        res.append(rate)
    result = {
        "Currency_code": currency_code.split(','),
        "Ex-rateUSD": res
    }
    return jsonify(result)
# for passing vector throw codes
@app2.route('/conversions/<string:currency_code>')
def ExchangeRateUSD_byUrl(currency_code):
    currency_code = currency_code.upper()
    codeV = {'CurrencyCode': currency_code.split(',')}
    codeV = pd.DataFrame(codeV)
    codeV['CurrencyCode'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    CurrName = []
    CurrUSDrate = []
    page = requests.get('https://www.x-rates.com/table/?from=USD&amount=1')
    soup = BeautifulSoup(page.content, "html.parser")
    Ex_rate = soup.find_all(class_='tablesorter ratesTable')
    Ex_rate_value = Ex_rate[0].text.replace('\n\n', '@')
    Ex_rate_value = Ex_rate_value.replace('\n', '@')
    Ex_rate_value = Ex_rate_value.replace('@@', '@')
    Ex_rate_value = Ex_rate_value.split('@')
    I_rng = 5
    while I_rng <= len(Ex_rate_value) - 3:
        CurrName.append(Ex_rate_value[I_rng])
        I_rng = I_rng + 3

    I_rng = 7
    while I_rng <= len(Ex_rate_value):
        CurrUSDrate.append(Ex_rate_value[I_rng])
        I_rng = I_rng + 3
    CurrDf = {'CurrencyName': CurrName, 'ExRateUSD': CurrUSDrate}
    CurrDf = pd.DataFrame(CurrDf)
    CurrDf = CurrDf.append({'CurrencyName': 'US DOLLAR', 'ExRateUSD': '1'}, ignore_index=True)
    CurrDf['CurrencyName'] = CurrDf['CurrencyName'].str.upper()
    CurrDf['CurrencyName'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    CurrDf['ExRateUSD'] = CurrDf['ExRateUSD'].astype(dtype=np.float64)

    CurrCode = pd.read_excel("refFiles/CurrencyCode.xlsx")
    CurrCode['CurrencyName'] = CurrCode['CurrencyName'].str.upper()
    CurrCode['CurrencyCode'] = CurrCode['CurrencyCode'].str.upper()
    CurrCode['CurrencyName'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    CurrCode['CurrencyCode'].replace('(^\s+|\s+$)', '', regex=True, inplace=True)

    CurrDf = CurrDf.merge(CurrCode, on='CurrencyName', how='left')
    CurrDf = CurrDf.drop_duplicates(subset='CurrencyCode', keep="last")
    CurrDf = CurrDf[['CurrencyCode', 'ExRateUSD']]
    codeV = codeV.merge(CurrDf, on='CurrencyCode', how='left')
    res = []
    for rate in codeV.ExRateUSD:
        res.append(rate)
    result = {
        "Currency_code": currency_code.split(','),
        "Ex-rateUSD": res
    }
    return jsonify(result)

if __name__ == "__main__":
    app2.run(debug=True)