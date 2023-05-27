from web3 import Web3
import json

ganache_url = "http://localhost:7545"  # Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

contract_file = open("contract.sol", "r")
contract_code = contract_file.read()
contract_file.close()

abi = ''
bytecode = ''

compiled_contract = web3.eth.contract(abi=json.loads(abi), bytecode=bytecode)

