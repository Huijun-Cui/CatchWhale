from web3 import Web3
import sys
import json
import requests

if len(sys.argv) >= 2:
    contract_address = sys.argv[1]
else:
    contract_address = '0x67baFF31318638F497f4c4894Cd73918563942c8'

rpc_url = 'http://127.0.0.1:8545/'
w3 = Web3(Web3.HTTPProvider(rpc_url))

users = {
    '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266':'0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80',
    '0x70997970C51812dc3A010C7d01b50e0d17dc79C8':'0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d',
    '0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC':'0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a',
    '0x90F79bf6EB2c4f870365E785982E1f101E93b906':'0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6',
    '0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65':'0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a',
    '0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc':'0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba'
}

def buld_param(nonce,val = 0,gas = 470000,_from = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'):
    _param = {
        'gas':gas,
        'value':val,
        'from':_from,
        'nonce':nonce
    }
    return _param


eth_abi_url = 'https://api.etherscan.io/api' + \
   '?module=contract' + \
   '&action=getabi' + \
   '&address={}'.format('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2') + \
   '&apikey=ZMHGVZTA8V3JAZGHXQCBCPZZRPJFUFVMGK'
eth_abi = json.loads(json.loads(requests.get(eth_abi_url).content.decode('utf-8'))['result'])
eth_c = w3.eth.contract(address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', abi = eth_abi)
print('name',eth_c.functions.name().call())

print(w3.eth.get_balance('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266') / (10 ** 18))
print(eth_c.functions.balanceOf('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266').call() / (10 ** 18))

nonce = w3.eth.getTransactionCount('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
val = int(300 * 10 ** 18)
print(nonce)
build_tx = eth_c.functions.deposit().buildTransaction(buld_param(nonce = nonce,val = val))
signed_tx = w3.eth.account.signTransaction(build_tx, private_key = users['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'])
w3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(w3.eth.get_balance('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266') / (10 ** 18))
print(eth_c.functions.balanceOf('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266').call() / (10 ** 18))

dai_c = w3.eth.contract(address = '0x6B175474E89094C44Da98b954EedeAC495271d0F', abi = eth_abi)
print('dai balance',dai_c.functions.balanceOf('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266').call())

with open('../artifacts/contracts/v3_swap.sol/SwapExamples.json') as f:
    nonce += 1
    val = 0
    print(nonce)
    build_tx = eth_c.functions.approve(contract_address,int(2 ** 255) - 1).buildTransaction(buld_param(nonce = nonce,val = val))
    signed_tx = w3.eth.account.signTransaction(build_tx, private_key = users['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'])
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    v3_swap_c = w3.eth.contract(address = contract_address, abi = json.load(f)['abi'])
    nonce += 1
    val = 0
    print(nonce)
    build_tx = v3_swap_c.functions.swapExactInputSingle(int(10 * 10 ** 18),\
        '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',\
            '0x6B175474E89094C44Da98b954EedeAC495271d0F').buildTransaction(buld_param(nonce = nonce,val = val))
    signed_tx = w3.eth.account.signTransaction(build_tx, private_key = users['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'])
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print('dai balance',dai_c.functions.balanceOf('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266').call())
