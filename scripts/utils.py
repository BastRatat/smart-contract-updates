from brownie import accounts, network, config
import eth_utils

LOCAL_ENV = ["development", "ganache-local", "mainnet-fork-dev", "mainnet-fork"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        accounts.load(id)
    if network.show_active() in LOCAL_ENV:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def encode_function_data(initializer=None, *args):
    if not len(args):
        args = b""

    if initializer:
        return initializer.encode_input(*args)

    return b""


def upgrade(
    account,
    proxy,
    newimplementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                newimplementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, newimplementation_address, {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                newimplementation_address, encoded_function_call, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(newimplementation_address, {"from": account})
    return transaction
