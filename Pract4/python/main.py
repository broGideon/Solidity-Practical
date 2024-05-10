import contract_info 
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_info.contract_address, abi=contract_info.abi)

def register():
    password = input("Введите пароль: ")
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
        print("Ошибка авторизации: {e}")
        return None

def send_eth(account):
    try:
        value = int(input("Введите кол-во WEI для отправки: "))
        tx_hash = contract.functions.senEth().transcat({
            'from': account,
            'value': value,
        })

        print(f"Ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")

def get_balance(account):
    try:
        balance = contract.functions.getBalance2().call({
            'from': account
        })
        print(f"Ваш баланс на смарт-контракте: {balance}")
    except Exception as e:
        print("Ошибка получения баланса: {e}")

def withdraw(account):
    try:
        value = int(input("Введите кол-во WEI для отправки: "))
        to = input("Введите адрес:")
        tx_hash = contract.functions.withdrawll(to, value).transact({
            'from' : account
        })
        print(f"ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")


def main():
    account = "";
    while True:
        if account == "" or account == None:
            choice = int(input("Долбро пожаловать в систему! Выберите: 1. Регистрация 2. Авторизация 3. Выйти"))
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
            choice = int(input("Выберите: 1. Создать недвижимость \n2. Создать объявление \n3. Сменить статус недвижимости \n4.  Сменить статус объявления \n5. Выйти"))
            match choice:
                case 1:
                    send_eth(account)
                case 2:
                    get_balance(account)
                case 3:
                    print(f"Баланс аккаунта: {w3.eth.get_balance(account)}")
                case 4:
                    withdraw(account)
                case 5:
                    account = ""
                case _:
                    print("Выберите от 1 до 5")

if __name__ == "__main__":
    main()

