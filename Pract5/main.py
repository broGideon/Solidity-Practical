from flask import Flask, render_template, request, redirect, url_for, flash
import contract_info
from web3 import Web3
from web3.middleware import geth_poa_middleware
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_info.contract_address, abi=contract_info.abi)


def secure(password):
    if len(password) < 12:
        return "Пароль должен быть больше 12 символов"

    if not any(item.islower() for item in password):
        return "Пароль должен содержать прописные буквы"

    if not any(item.isupper() for item in password):
        return "Пароль должен содержать строчные буквы"

    if not any(item.isdigit() for item in password):
        return "Пароль должен содержать числа"

    if not any(item in string.punctuation for item in password):
        return "Пароль должен содержать спец символы"

    return True


def create_estate(razmer, address, type_value, account):
    try:
        tx_hash = contract.functions.createEstate(razmer, address, type_value).transact({
            'from': account,
        })
        flash('Недвижимость успешно создана', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def create_ad(prise, id_estate, ad_status, account):
    try:
        tx_hash = contract.functions.createAd(prise, id_estate, ad_status).transact({
            'from': account,
        })
        flash('Объявление успешно создано', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def change_status_estate(id_estate, account):
    try:
        tx_hash = contract.functions.changeStatusEstate(id_estate).transact({
            'from': account
        })
        flash('Статус успешно обновлен', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def change_status_ad(id_ad, account):
    try:
        tx_hash = contract.functions.changeStatusAd(id_ad).transact({
            'from': account
        })
        flash('Статус успешно обновлен', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def get_balance(account):
    try:
        balance = contract.functions.getBalance().call({
            'from': account
        })
        return balance
    except Exception as e:
        return 0


def buy_estate(id_ad, account):
    try:
        tx_hash = contract.functions.buyEstate(id_ad).transact({
            'from': account
        })
        flash('Операция успешно выполнена', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def withdraw(value, account):
    try:
        tx_hash = contract.functions.withDraw(value).transact({
            'from': account
        })
        flash('Операция успешно выполнена', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def pay(value, account):
    try:
        tx_hash = contract.functions.pay().transact({
            'from': account,
            'value': value
        })
        flash('Операция успешно выполнена', 'successful')
    except Exception as e:
        flash(str(e).split(',')[0].replace("(", "").replace("'", ""), 'error')


def login(public_key, password):
    try:
        w3.geth.personal.unlock_account(public_key, password)
        return True
    except:
        return False


def get_estate(account):
    try:
        estates = contract.functions.getEstates().call({
            'from': account
        })
        return estates
    except Exception as e:
        return 'error'


def get_ads(account):
    try:
        ads = contract.functions.getAds().call({
            'from': account
        })
        return ads
    except Exception as e:
        return 'error'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        password = request.form.get('password')
        valid = secure(password)
        if valid == True:
            login = w3.geth.personal.new_account(password)
            return render_template("reg.html", login=login)
        else:
            return render_template("reg.html", error=valid)
    else:
        return render_template("reg.html")


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        if login(username, password):
            return redirect(url_for('about', name=username))
        else:
            return render_template("auth.html", error="Неверный логин или пароль")
    else:
        return render_template("auth.html")


@app.route('/about/<name>', methods=["GET", "POST"])
def about(name):
    ads = get_ads(name)
    estates = get_estate(name)
    type_estate = {0: "House", 1: "Flat", 2: "Loft"}
    balance = get_balance(name)
    balance_account = w3.eth.get_balance(name)
    if request.method == 'POST':
        type_form = request.form.get('type_form')
        if type_form == 'createEstate':
            razmer = int(request.form.get('razmer'))
            address = request.form.get('address')
            type_value = int(request.form.get('type'))
            create_estate(razmer, address, type_value, name)
        elif type_form == 'createAd':
            price = int(request.form.get('price'))
            id_estate = int(request.form.get('id_estate'))
            is_active = int(request.form.get('is_open'))
            create_ad(price, id_estate, is_active, name)
        elif type_form == 'changeStatusEstate':
            id_estate = int(request.form.get('id_estate'))
            change_status_estate(id_estate, name)
        elif type_form == 'changeStatusAd':
            id_ad = int(request.form.get('id_ad'))
            change_status_ad(id_ad, name)
        elif type_form == 'buy_estate':
            id_ad = int(request.form.get('id_ad'))
            buy_estate(id_ad, name)
        elif type_form == 'withdraw':
            value = int(request.form.get('money'))
            withdraw(value, name)
        elif type_form == 'pay':
            value = int(request.form.get('money'))
            pay(value, name)
        return redirect(url_for('about', name=name))
    else:
        return render_template("home.html", name=name, ads=ads, estates=estates, type_estate=type_estate, balance=balance, balance_account=balance_account)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)