import json

"""
    Created by B20DCCN728
    Read ethereum wallets from a JSON file
"""


def read(file_path: str) -> list[dict[str, str, str]]:
    with open(file_path, "r") as file:
        wallets = json.load(file)

    return wallets


if __name__ == '__main__':
    wallet_list = read("eth.json")
    for wallet in wallet_list:
        for key in wallet["mnemonic"].split(" "):
            print(key)


