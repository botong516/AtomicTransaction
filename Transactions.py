import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk import transaction
from algosdk import mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# Write down the address, private key, and the passphrase for later usage
generate_algorand_keypair()

def transaction_example(private_key, my_address, receiver, note):
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = ""
    headers = {"X-API-Key": "9LRgIRPFaO6z80AKatXCE7YiaRZGg9vu6cjXi7ii"}
    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    # receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    receiver = receiver
    amount = 1420000
    # note = "Hello World".encode()
    note = note

    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')))
    print("Amount transfered: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# replace private_key and my_address with your private key and your address.
private_key_A = mnemonic.to_private_key("maze screen check actual wide pottery dune jaguar extra beach castle update affair dawn lonely boost sense word broom pilot royal fragile use abandon rhythm")
private_key_B = mnemonic.to_private_key("blame skill angle better borrow special feel awake pause track issue much cloth soup chest kiwi chase special sudden excite speed barrel direct absent thought")

transaction_example(private_key_A, "7XR45CDKUYQBALS7R44AX4675QLOO2KQLILYRRMHIBQIRXWCB7XRHD4CQI",
                          "4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI", "my first Algorand transaction".encode())

transaction_example(private_key_B, "OJQPUE4LFFJV6PJR7KLM6TNVDWJ7PFJDVGQHWJN3TL326WCTGY3LNCBNAA",
                          "4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI", "my second Algorand transaction".encode())