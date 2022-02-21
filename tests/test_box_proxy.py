from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract
from scripts.utils import get_account, encode_function_data


def test_proxy_delegates_calls():
    account = get_account()
    account_param = {"from": account}
    box = Box.deploy(account_param)
    proxy_admin = ProxyAdmin.deploy(account_param)
    box_encoded_initializer = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer,
        {"from": account, "gasLimit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, account_param)
    assert proxy_box.retrieve() == 1
