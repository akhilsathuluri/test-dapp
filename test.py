import json
from web3 import Web3, HTTPProvider

# Create a connection to the local node
w3 = Web3(HTTPProvider("http://localhost:7545"))
print(w3.isConnected())

# Initialise local account object
local_account = w3.eth.accounts[0]

# Compile the contract
truffleFile = json.load(open('./build/contracts/SimpleAuction.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# Initialise the contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build the transaction
txn = contract.constructor().buildTransaction({
    'from': local_account.address,
    'nonce': w3.eth.getTransactionCount(local_account.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})

# Sign the transaction
signed = w3.eth.account.signTransaction(txn, local_account.key)

# Broadcast the transaction
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())

# Collect the transaction receipt
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Address: ", receipt.contractAddress)
contract_address = receipt.contractAddress

# Get the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=abi)
