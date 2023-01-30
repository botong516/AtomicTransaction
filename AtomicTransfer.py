import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk import transaction
from algosdk import mnemonic
import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation

# This atomic transfer example code requires three (3) acounts:
#  - account_1 requires a user-defined mnemonic and be funded with 1001000 microAlgos
#  - account_2 requires a user-defined mnemonic and be funded with 2001000 microAlgos
#  - account_3 auto-generated within the code, 1000000 microAlgos will be transfered here
# For account_1 and account_2, replcace the string "Your 25-word mnemonic goes here" in the code below.
# For account_3, ensure you note the mnemonic generated for future.
# Faucents available for funding accounts:
#  - TestNet: https://developer.algorand.org/docs/reference/algorand-networks/testnet/#faucet
#  - BetaNet: https://developer.algorand.org/docs/reference/algorand-networks/betanet/#faucet
# Replace the algod_address and algod_token parameters below to connect to your API host.

# never use mnemonics in code, for demo purposes only
# user declared account mnemonics for account1 and account2
mnemonic_1 = "maze screen check actual wide pottery dune jaguar extra beach castle update affair dawn lonely boost sense word broom pilot royal fragile use abandon rhythm"
mnemonic_2 = "blame skill angle better borrow special feel awake pause track issue much cloth soup chest kiwi chase special sudden excite speed barrel direct absent thought"

accounts = {}
counter = 1
for m in [mnemonic_1, mnemonic_2]:
    accounts[counter] = {}
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    accounts[counter]['pk'] = account.address_from_private_key(accounts[counter]['sk'])
    counter += 1

# user declared algod connection parameters
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = ""
headers = {"X-API-Key": "9LRgIRPFaO6z80AKatXCE7YiaRZGg9vu6cjXi7ii"}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

address_A = "7XR45CDKUYQBALS7R44AX4675QLOO2KQLILYRRMHIBQIRXWCB7XRHD4CQI"
address_B = "OJQPUE4LFFJV6PJR7KLM6TNVDWJ7PFJDVGQHWJN3TL326WCTGY3LNCBNAA"

# print("My address: {}".format(my_address))
# account_info = algod_client.account_info(my_address)
# print("Account balance: {} microAlgos".format(account_info.get('amount')))


## TRANSFER ALGO

# build transaction
params = algod_client.suggested_params()
# comment out the next two (2) lines to use suggested fees
params.flat_fee = constants.MIN_TXN_FEE
params.fee = 1000
# receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
receiver = address_A
amount = 1200000
# note = "Hello World".encode()
note = "payment transaction of 1.2 Algos from B to A".encode()

unsigned_txn_1 = transaction.PaymentTxn(address_B, params, receiver, amount, None, note)



## TRANSFER ASSET

# transfer asset of 1 from account A to account B
# params_2 = algod_client.suggested_params()
# # comment these two lines if you want to use suggested params
# params_2.fee = 1000
# params_2.flat_fee = True
unsigned_txn_2 = AssetTransferTxn(
    sender=accounts[1]['pk'],
    sp=params,
    receiver=accounts[2]["pk"],
    amt=1,
    index=155696286)



## GROUP TRANSACTIONS
# get group id and assign it to transactions
gid = transaction.calculate_group_id([unsigned_txn_1, unsigned_txn_2])
unsigned_txn_1.group = gid
unsigned_txn_2.group = gid


## sign transactions
stxn_1 = unsigned_txn_1.sign(accounts[2]['sk'])
stxn_2 = unsigned_txn_2.sign(accounts[1]['sk'])


## assemble transaction group
signed_group = [stxn_1, stxn_2]


tx_id = algod_client.send_transactions(signed_group)

## wait for confirmation
confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
print("txID: {}".format(tx_id), " confirmed in round: {}".format(
confirmed_txn.get("confirmed-round", 0)))


# # utility function to get address string
#
#
# def get_address(mn):
#     pk_account_a = mnemonic.to_private_key(mn)
#     address = account.address_from_private_key(pk_account_a)
#     print("Address :", address)
#     return address
#
# # utility function to generate new account
#
#
# def generate_new_account():
#     private_key, address = account.generate_account()
#     print("Created new account: ", address)
#     print("Generated mnemonic: \"{}\"".format(
#         mnemonic.from_private_key(private_key)))
#     return address
#
# # utility function to display account balance
#
#
# def display_account_algo_balance(client, address):
#     account_info = client.account_info(address)
#     print("{}: {} microAlgos".format(address, account_info["amount"]))
#
#
# def group_transactions():
#     # Initialize an algodClient
#     algod_client = algod.AlgodClient(algod_token, algod_address)
#
# # declared account1 and account2 based on user supplied mnemonics
#     print("Loading two existing accounts TO SIGN, and account_3 to recieve")
#     account_1 = get_address(mnemonic_1)
#     account_2 = get_address(mnemonic_2)
#     account_3 = generate_new_account()
#     print("!! NOTICE !! Please retain the above generated \"25-word mnemonic passphrase\" for future use.")
#
# # convert mnemonic1 and mnemonic2 using the mnemonic.ToPrivateKey() helper function
#     sk_1 = mnemonic.to_private_key(mnemonic_1)
#     sk_2 = mnemonic.to_private_key(mnemonic_2)
#
# # # generate account3, display mnemonic, wait
# # # print("Generating new account...")
# #     account_3 = generate_new_account()
# #     print("!! NOTICE !! Please retain the above generated \"25-word mnemonic passphrase\" for future use.")
#
# # display account balances
#     print("Initial balances:")
#     display_account_algo_balance(algod_client, account_1)
#     display_account_algo_balance(algod_client, account_2)
#     display_account_algo_balance(algod_client, account_3)
#
# # get node suggested parameters
#     params = algod_client.suggested_params()
#     # comment out the next two (2) lines to use suggested fees
#     # params.flat_fee = True
#     # params.fee = 1000
#
# # create transactions
#     print("Creating transactions...")
# # from account 1 to account 3
#     sender = account_1
#     receiver = account_3
#     amount = 100000
#     txn_1 = PaymentTxn(sender, params, receiver, amount)
#     print("...txn_1: from {} to {} for {} microAlgos".format(
#         sender, receiver, amount))
#     print("...created txn_1: ", txn_1.get_txid())
#
# # from account 2 to account 1
#     sender = account_2
#     receiver = account_1
#     amount = 200000
#     txn_2 = PaymentTxn(sender, params, receiver, amount)
#     print("...txn_2: from {} to {} for {} microAlgos".format(
#         sender, receiver, amount))
#     print("...created txn_2: ", txn_2.get_txid())
#
# # combine transactions
#     print("Combining transactions...")
# # the SDK does this implicitly within grouping below
#
#     print("Grouping transactions...")
# # compute group id and put it into each transaction
#     group_id = transaction.calculate_group_id([txn_1, txn_2])
#     print("...computed groupId: ", group_id)
#     txn_1.group = group_id
#     txn_2.group = group_id
#
# # split transaction group
#     print("Splitting unsigned transaction group...")
#     # this example does not use files on disk, so splitting is implicit above
#
# # sign transactions
#     print("Signing transactions...")
#     stxn_1 = txn_1.sign(sk_1)
#     print("...account1 signed txn_1: ", stxn_1.get_txid())
#     stxn_2 = txn_2.sign(sk_2)
#     print("...account2 signed txn_2: ", stxn_2.get_txid())
#
# # assemble transaction group
#     print("Assembling transaction group...")
#     signedGroup = []
#     signedGroup.append(stxn_1)
#     signedGroup.append(stxn_2)
#
# # send transactions
#     print("Sending transaction group...")
#     tx_id = algod_client.send_transactions(signedGroup)
#
#     # wait for confirmation
#
#     confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
#     print("txID: {}".format(tx_id), " confirmed in round: {}".format(
#     confirmed_txn.get("confirmed-round", 0)))
# # display account balances
#     print("Final balances:")
#     display_account_algo_balance(algod_client, account_1)
#     display_account_algo_balance(algod_client, account_2)
#     display_account_algo_balance(algod_client, account_3)
#
# # display confirmed transaction group
# # tx1
#     confirmed_txn = algod_client.pending_transaction_info(txn_1.get_txid())
#     print("Transaction information: {}".format(
#         json.dumps(confirmed_txn, indent=4)))
#
# # tx2
#     confirmed_txn = algod_client.pending_transaction_info(txn_2.get_txid())
#     print("Transaction information: {}".format(
#         json.dumps(confirmed_txn, indent=4)))
#
#
# group_transactions()