from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
from scripts.utils import get_account, encode_function_data, upgrade
import pytest


def test_upgrade():
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

    box_v2 = BoxV2.deploy(account_param)

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment(account_param)

    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    assert proxy_box.retrieve() == 0

    proxy_box.increment(account_param)
    assert proxy_box.retrieve() == 1
