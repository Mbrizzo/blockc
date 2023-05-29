from web3 import Web3
import json

ganache_url = "http://localhost:7545"  # Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

contract_file = open("contract.sol", "r")
contract_code = contract_file.read()
contract_file.close()

# solc --abi --bin contract.sol -o build/
with open('build/Counter.json', 'r') as f:
    compiled_contract_data = json.load(f)

abi = compiled_contract_data['abi']
bytecode = compiled_contract_data['bytecode']

compiled_contract = web3.eth.contract(abi=abi, bytecode=bytecode)

account = web3.eth.accounts[0]  # endereço no Ganache

# Transação de implantação do contrato
transaction = compiled_contract.constructor().buildTransaction({
    "from": account,
    "nonce": web3.eth.getTransactionCount(account),
    "gas": 4000000,  # Substitua pelo valor adequado de gás
})

# Assinar e enviar a transação
signed_txn = web3.eth.account.signTransaction(transaction, private_key="sua_chave_privada")
transaction_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Aguardar a confirmação da transação
transaction_receipt = web3.eth.waitForTransactionReceipt(transaction_hash)

# Obter o endereço do contrato implantado
contract_address = transaction_receipt["contractAddress"]
