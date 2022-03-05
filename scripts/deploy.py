from ctypes import addressof
from unittest import mock
from brownie import FundMe, MockV3Aggregator, network, config
from dotenv import load_dotenv
from scripts.helpful_scripts import (get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS)

load_dotenv()

def deploy_fund_me():
    account = get_account()
    #pass the pass feed address to our fundme contract

    # if we are on a persistent network like rinkeby use associated address.
    # otherwise, deploy mocks

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        # Creating a seperate function for this and putting it in helpful_scripts

        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address



    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, publish_source=config["networks"][network.show_active()].get("verify",)
    )
    print(f"Contract deployed to {fund_me.address}")

    return fund_me

def main():
    deploy_fund_me()