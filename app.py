from flask import Flask, render_template, request
import requests
import numpy as np

app = Flask(__name__)

# Clé API Currency Beacon
API_KEY = "jz6nZSDvaEfSt5v15jUAF9XKG0OfBzKa"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        # Effectuer la conversion en utilisant l'API Currency Beacon
        conversion_result = convert_currency(from_currency, to_currency, amount)

        # Afficher le résultat de la conversion
        return render_template('result.html', conversion_result=conversion_result)

    # Si la méthode est GET ou si aucune soumission de formulaire n'a été effectuée, afficher le formulaire
    return render_template('index.html')

def convert_currency(from_currency, to_currency, amount):
    # Construire l'URL de requête avec les données du formulaire et la clé API
    url = f"https://api.currencybeacon.com/v1/convert?from={from_currency}&to={to_currency}&amount={amount}&api_key={API_KEY}"

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



if __name__ == '__main__':
    app.run(debug=True)
