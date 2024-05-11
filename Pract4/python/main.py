import contract_info 
from web3 import Web3
from web3.middleware import geth_poa_middleware
import string

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_info.contract_address, abi=contract_info.abi)

def input_int(info):
    try:
        data = int(input(info))
        return data
    except:
        print("Неверный тип данных")
        return False
    
def secure(password):
    if password.count < 12:
        print("Пароль должен быть больше 12 символов")
        return False

    if not any(item.islower() for item in password):
        print("Пароль должен содержать прописные буквы")
        return False
    
    if not any(item.isupper() for item in password):
        print("Пароль должен содержать строчные буквы")
        return False
    
    if not any(item.isdigit() for item in password):
        print("Пароль должен содержать числа")
        return False
    
    if not any(item in string.punctuation for item in password):
        print("Пароль должен содержать спец символы")
        return False

    return True

def register():
    is_secure = False
    while(not is_secure):
        password = input("Введите пароль: ")

        is_secure = secure(password)


    account = w3.geth.personal.new_account(password)
    print(f"Ваш публичный ключ: {account}")

def login():
    public_key = input("Введите ваш публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(public_key, password)
        print("Авторизация прошла успешно!")
        return public_key
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None

def create_estate(account):
    try:
        
        razmer = int(input("Введите размер недвижимости: "))
        address = input("Введите адрес недвижимости: ")
        type = int(input("1. House \n2. Flat\n3. Loft \nВыберите тип недвижимости: "))

        if type < 1 or type > 3:
            print("Неверный тип")
            return


        tx_hash = contract.functions.createEstate(razmer, address, type-1).transact({
            'from': account,
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def create_ad(account):
    try:
        prise = int(input("Введите цену: "))
        get_estate(account)
        id_estate = int(input("Введите ID: "))
        ad_status = int(input("1. Open \n2. Close\nВыберите активность объявления: "))

        if ad_status < 1 or ad_status > 2:
            print("Недопустимое значение")
            return

        tx_hash = contract.functions.createAd(prise, id_estate, ad_status-1).transact({
            'from': account,
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def change_status_estate(account):
    try:
        get_estate(account)
        id_estate = int(input("Введите ID: "))

        tx_hash = contract.functions.changeStatusEstate(id_estate).transact({
            'from': account 
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка смены статуса: {e}")

def change_status_ad(account):
    try:
        get_ads(account)
        id_ad = int(input("Введите ID: "))

        tx_hash = contract.functions.changeStatusAd(id_ad).transact({
            'from': account 
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка смены статуса: {e}")

def get_balance(account):
    try:
        balance = contract.functions.getBalance().call({
            'from': account
        })
        print(f"Ваш баланс на смарт-контракте: {balance}")
    except Exception as e:
        print("Ошибка получения баланса: {e}")

def buy_estate(account):
    try:
        get_ads(account)
        id_ad = int(input("Введите ID: "))
        to = input("Введите адрес:")
        tx_hash = contract.functions.buyEstate(id_ad).transact({
            'from' : account
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка транзакции: {e}")

def withdraw(account):
    try:
        value = int(input("Введите кол-во WEI для вывода: "))
        tx_hash = contract.functions.withDraw(value).transact({
            'from' : account
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка транзакции: {e}")

def get_estate(account):
    try:
        estates = contract.functions.getEstates().call({
            'from': account
        })
        
        for item in estates:
            print(item)
    except Exception as e:
        print("Ошибка получения недвижимости: {e}")

def get_ads(account):
    try:
        ads = contract.functions.getAds().call({
            'from': account
        })

        for item in ads:
            print(item)
    except Exception as e:
        print("Ошибка получения объявлений: {e}")

def pay(account):
    try:
        value = int(input("Введите кол-во WEI для пополнения: "))
        if value <= 0:
            print("Значение должно быть больше нуля") 
            return
        tx_hash = contract.functions.pay().transact({
            'from' : account,
            'value': value
        })

        print(f"Операция успешно выполнена. Хэш операции: {tx_hash}")
    except Exception as e:
        print(f"Ошибка пополнения: {e}")


def main():
    account = "";
    while True:
        if account == "" or account == None:
            choice = int(input("Долбро пожаловать в систему! Выберите: 1. Регистрация 2. Авторизация 3. Выйти \n"))
            match choice:
                case 1:
                    register()
                case 2:
                    account = login()
                case 3:
                    exit(0)
                case _:
                    print("Выберите 1 или 2!")
        else:
            choice = int(input("Выберите: \n1. Создать недвижимость \n2. Создать объявление \n3. Сменить статус недвижимости \n4.  Сменить статус объявления \n5. Покупка недвжимости \n6. Вывод средств \n7. Доступная недвижимость \n8. Доступные объявления \n9. Баланс на смарт контракте \n10. Баланс на аккаунте \n11. Пополнить баланс смарт контракта \n12. Выход \n"))
            match choice:
                case 1:
                    create_estate(account)
                case 2:
                    create_ad(account)
                case 3:
                    change_status_estate(account)
                case 4:
                    change_status_ad(account)
                case 5:
                    buy_estate(account)
                case 6:
                    withdraw(account)
                case 7:
                    get_estate(account)
                case 8:
                    get_ads(account)
                case 9:
                    get_balance(account)
                case 10:
                    print(f"Баланс аккаунта: {w3.eth.get_balance(account)}")
                case 11:
                    pay(account)
                case 12:
                    account = ""
                case _:
                    print("Выберите от 1 до 11")

if __name__ == "__main__":
    main()

