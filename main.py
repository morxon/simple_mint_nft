from web3 import Web3
from eth_account import Account

from concurrent.futures import ThreadPoolExecutor


w3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))


def send_tx(private_key):
    acc = Account.from_key(private_key)

    transaction = contract.functions.mint() \
        .buildTransaction({
            'gas': 280000,
            'gasPrice': w3.eth.gas_price,
            'from': acc.address,
            'nonce': w3.eth.getTransactionCount(acc.address)
        })

    signed_txn = w3.eth.account.signTransaction(transaction,
                                                private_key=private_key)

    w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))
    print(f'Mint_tx:{tx_hash} | address:{acc.address}')


if __name__ == '__main__':
    with open('ABI', 'r', encoding='utf-8-sig') as file:
        ABI = file.read().strip().replace('\n', '').replace(' ', '')
    contract = w3.eth.contract(address=Web3.toChecksumAddress('0xBb73C18a415C1D7274461a3b96A764daB782334a'), abi=ABI)

    with open("keys.txt", 'r') as file:
        keys = [row.strip() for row in file]

    with ThreadPoolExecutor(max_workers=int(input('Threads>>>'))) as executor:
        executor.map(send_tx, keys)

