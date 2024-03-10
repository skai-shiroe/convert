from flask import Flask, render_template, request
from statistics import mean, stdev
import requests
import numpy as np


app = Flask(__name__)

conversion_results = []
# Clé API Currency Beacon
API_KEY = "jz6nZSDvaEfSt5v15jUAF9XKG0OfBzKa"
#route principal index
@app.route('/', methods=['GET', 'POST'])

def index():
    return render_template('index.html',conversion_results=conversion_results)

#route pour la page form
@app.route('/formulaire_conversion.html', methods=['GET', 'POST'])
def conversion():
    conversion_result = None
    amount=None
    from_currency=None
    if request.method == 'POST':
        # Récupérer les données du formulaire
        from_currency = request.form['from_currency']
        amount = float(request.form['amount'])

        # Effectuer la conversion en utilisant l'API Currency Beacon
        conversion_result = convert_currency(from_currency, amount)
        
        if conversion_result is not None:
            conversion_results.append((from_currency,amount,conversion_result))

    return render_template('formulaire_conversion.html', amount= amount,from_currency=from_currency,conversion_result=conversion_result,conversion_results=conversion_results)

def convert_currency(from_currency, amount):
    
    url = f"https://api.currencybeacon.com/v1/convert?from={from_currency}&to=XOF&amount={amount}&api_key={API_KEY}"

    # Effectuer la requête à l'API Currency Beacon
    response = requests.get(url)

    if response.status_code == 200:
        # Si la requête réussit, récupérer les données JSON de la réponse
        conversion_data = response.json()
        if 'response' in conversion_data:
            converted_amount = conversion_data['response']['value']
            return converted_amount
        else:
            # Gérer le cas où la clé 'response' est absente dans la réponse
            return None
    else:
        # Gérer les erreurs de requête
        return None
    

#route pour afficher les taux d'echange
@app.route('/taux_echange.html', methods=['GET', 'POST'])
def taux():
    # Liste des devises 
    devises = ['USD', 'EUR', 'JPY', 'GBP', 'AUD']

    # Clé API 
    api_key = "jz6nZSDvaEfSt5v15jUAF9XKG0OfBzKa"  

    # Initialisation du dictionnaire pour stocker les taux de change
    exchange_rates = {}

    # URL de l'API des taux de change
    api_url = "https://api.currencybeacon.com/v1/latest"

    try:
        for devise in devises:
            # Paramètres de la requête GET
            params = {
                'base': devise,     
                'api_key': api_key  
            }

            # requête GET à l'API
            response = requests.get(api_url, params=params)
            # Obtenir les données JSON de la réponse
            data = response.json()
            # Extraire les taux de change pour chaque devise
            exchange_rates[devise] = data.get('rates', {}).get('XOF', 'N/A')

        return render_template('taux_echange.html', exchange_rates=exchange_rates)

    except Exception as e:
        # Gérer les erreurs éventuelles lors de la récupération des taux de change
        return f"Erreur lors de la récupération des taux de change : {e}", 500


#route pour afficher les taux statistiques
@app.route('/statistique_total.html', methods=['GET', 'POST'])
def stats():
    amounts = [result[2] for result in conversion_results] if conversion_results else []

    if amounts:
        average_amount = mean(amounts)
        std_dev_amount = stdev(amounts)
        min_amount = min(amounts)
        max_amount = max(amounts)
        return render_template('/statistique_total.html', average_amount=average_amount, std_dev_amount=std_dev_amount,
                               min_amount=min_amount, max_amount=max_amount)
    else:
        return render_template('/statistique_total.html')


if __name__ == '__main__':
    app.run(debug=True)
