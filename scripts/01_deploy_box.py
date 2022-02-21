from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    network,
)
from scripts.utils import get_account, encode_function_data


def main():
    account = get_account()
    account_param = {"from": account}
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(account_param)
    proxy_admin = ProxyAdmin.deploy(account_param)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}, contract is now upgradeable.")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
