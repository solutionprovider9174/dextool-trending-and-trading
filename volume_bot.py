import requests
import json
import config
import time
import sys
import web3
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

load_dotenv()
# with open("tokenabi.json") as f:
#     tokenabi_json = json.load((f.read()))
# TOKEN_ABI = tokenabi_json
# print(TOKEN_ABI)
f= open("tokenabi.json",) 
TOKEN_ABI = json.load(f)
 


a= open("routerabi.json",) 
ROUTER_ABI = json.load(a)



k= open("wtoke.json",) 
WRAP_ABI = json.load(k)
 

PRIVATE_KEY = ""

ROUTER_ADDRESS = Web3.toChecksumAddress("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D") # uniswap v3 router
PAIR_ADDRESS = Web3.toChecksumAddress("0xa8dfebeb90f8e148b6a3c611758ea63703ab02c1") # uniswap v3 router

SENDER_ADDRESS = Web3.toChecksumAddress("")
TOKEN_ADDRESS = Web3.toChecksumAddress("0x24ffe459f51ea20c5d8ad49843529fc33654e7e4")  # POMD
TARGET_ADDRESS = Web3.toChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")  # Wrapped Ether

routerABI = ROUTER_ABI
tokenABI = TOKEN_ABI
wraptoken= WRAP_ABI


ethereum = ""
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/#############################'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

print(web3.isConnected())

routerContract = web3.eth.contract(
    address=ROUTER_ADDRESS, abi=routerABI)
nonce = web3.eth.getTransactionCount(SENDER_ADDRESS)
print(nonce)
# exit()
tokenContract = web3.eth.contract(TOKEN_ADDRESS, abi=tokenABI)
WtokenContract=web3.eth.contract(TARGET_ADDRESS, abi=wraptoken)

IS_SELL = True # BAG -> ETH

while True:
  balance = web3.eth.getBalance(SENDER_ADDRESS)
  humanReadable = web3.fromWei(balance, 'ether')
  print(humanReadable)

#   if balance < web3.toWei(100, 'ether'):
#     break
  
  tokenValue = tokenContract.functions.balanceOf(SENDER_ADDRESS).call()
  am=int(tokenValue/10000)
  print(am)

  if IS_SELL == True:
    start = time.time()
    print(int(time.time()) + 1000000)

    approve = tokenContract.functions.approve(ROUTER_ADDRESS, am).buildTransaction({
        'from': SENDER_ADDRESS,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(SENDER_ADDRESS),
    })

    signed_txn = web3.eth.account.sign_transaction(
        approve, private_key=PRIVATE_KEY)
    tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    print("approved : " + web3.toHex(tx_token))

    receipt = web3.eth.waitForTransactionReceipt(
        tx_token, timeout=30000, poll_latency=0.1)

    amount = routerContract.functions.getAmountsOut(am, [TOKEN_ADDRESS, TARGET_ADDRESS]).call()
    print(amount)

    swap = routerContract.functions.swap(
        am,  # am,
        1,
        [TOKEN_ADDRESS, TARGET_ADDRESS],
        SENDER_ADDRESS,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': SENDER_ADDRESS,
        'gas': 250000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(SENDER_ADDRESS),
    })
    signed_txn = web3.eth.account.sign_transaction(
        swap, private_key=PRIVATE_KEY)
    tx_swap = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    print(web3.toHex(tx_swap))

    print("Wait...")
    time.sleep(5)
    receipt = web3.eth.waitForTransactionReceipt(
        tx_swap, timeout=30000, poll_latency=0.1)
    print("-----------------------Token successfully bought---------------------------------")
  #
  else:

    start = time.time()
    print(start)
    wtokenValue = WtokenContract.functions.balanceOf(SENDER_ADDRESS).call()
    wtokenValue=int(wtokenValue)
    amount = routerContract.functions.getAmountsOut(wtokenValue,[TARGET_ADDRESS,TOKEN_ADDRESS]).call()
    print(amount)

    approve = WtokenContract.functions.approve(ROUTER_ADDRESS, wtokenValue).buildTransaction({
        'from': SENDER_ADDRESS,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(SENDER_ADDRESS),
    })

    signed_txn = web3.eth.account.sign_transaction(
        approve, private_key=PRIVATE_KEY)
    tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    print("approved : " + web3.toHex(tx_token))

    receipt = web3.eth.waitForTransactionReceipt(
        tx_token, timeout=30000, poll_latency=0.1)

    swap = routerContract.functions.swap(
        wtokenValue,
        1,#amount[1],
        [TARGET_ADDRESS,TOKEN_ADDRESS],
        SENDER_ADDRESS,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': SENDER_ADDRESS,
        'gas': 250000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(SENDER_ADDRESS),
    })

    signed_txn = web3.eth.account.sign_transaction(
        swap, private_key=PRIVATE_KEY)
    tx_swap = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    print(web3.toHex(tx_swap))

    print("Wait...")
    time.sleep(5)
    receipt = web3.eth.waitForTransactionReceipt(
        tx_swap, timeout=30000, poll_latency=0.1)
    print("-----------------------Token successfully sold---------------------------------")
    # exit()
  IS_SELL = not IS_SELL


