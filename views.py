from app import app
from flask import render_template, request, jsonify
from queryes import addmoney, getmoney
from config import *

@app.route('/')
def index():
    return render_template('index.html')


def nopost():
    return jsonify({"success": False, "errormsg": 'Неправильный метод HTTP запроса'})

def moneyaddvalidation(currency, value):
    
    if currency == 'RUB' and value in valuerub:
        return True
    if currency == 'USD' and value in valueusd:
        return True
    if currency == 'EUR' and value in valueeur:
        return True
    
    return False

def moneygetvalidation(currency, amount):
    if currency == 'RUB' and amount >= valuerub[0]:
        return True
    if currency == 'USD' and amount >= valueusd[0]:
        return True
    if currency == 'EUR' and amount >= valueeur[0]:
        return True
    
    return False

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        currency = str(request.form['currency'])
        value = int(request.form['value'])
        total = int(request.form['quantity'])
        if not moneyaddvalidation(currency, value):
            return jsonify({'success': False, "errormsg": 'Валюта или номинал не поддерживается'})
        if addmoney(currency, value, total):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, "errormsg": 'Ошибка записи в базу данных'})
    else:
        return nopost()

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        currency = str(request.form['currency'])
        amount = int(request.form['amount'])
        if not moneygetvalidation(currency, amount):
            return jsonify({'success': False, "errormsg": 'Валюта или номинал не поддерживается'})
        return jsonify(getmoney(currency, amount))
    else:
        return nopost()

@app.route('/test')
def test():
    return render_template('test.html')

