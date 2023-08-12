from web3 import Web3

from app.logs import logging as logger
from app.utils.configs.config import rpcs, contracts


class Estimate:
    def __init__(self, pk):
        self.pk = pk

    def estimate_bridge(self, bridge_amount):
        web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
        logger.info(f"Successfully connected to {rpcs['eth']}")

        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ETH network: {web3.from_wei(wallet_balance, 'ether')}")

            contract = web3.eth.contract(address=Web3.to_checksum_address(contracts["ZoraBridge"]["address"]),
                                         abi=contracts["ZoraBridge"]["abi"])

            gas_estimate = contract.functions.depositTransaction(wallet_address, Web3.to_wei(bridge_amount, 'ether'),
                                                                 100000,
                                                                 False, b'').estimate_gas()

            gas_price = web3.eth.gas_price * 1.15

            total_cost_eth = Web3.from_wei(gas_estimate * gas_price, 'ether')
            #logger.info(f"Estimated Gas: {gas_estimate} Gas Price: {round(Web3.from_wei(gas_price, 'gwei'), 2)} gwei Total Cost: {total_cost_eth} ETH")
            return total_cost_eth
        except Exception as err:
            logger.error(f"Error while bridge estimating price: {err}")


    def eth_required(self, bridge_amount):
        total_amount = self.estimate_bridge(bridge_amount=bridge_amount)
        print("Eth required: ", total_amount)