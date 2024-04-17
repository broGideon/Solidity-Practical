import contract_info 
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_info.contract_address, abi=contract_info.abi)

balances = {}

for account in w3.eth.accounts:
    balances[account] = Web3.from_wei(w3.eth.get_balance(account), 'ether')

for key, value in balances.items():
    print(F"{key}: {value}")
