#!/usr/bin/python3
from brownie import (
    BoxV2,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    network,
    Contract,
)
from scripts.utils import get_account, upgrade


def main():
    account = get_account()
    account_param = {"from": account}

    box_v2 = BoxV2.deploy(account_param)

    proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]

    upgrade_tx = upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    upgrade_tx.wait(1)

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    return proxy_box
