import json
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from django.conf import settings
from useraccount.models import UserAccount


def create_ekata_units_account(user):
    rpc_connect = AuthServiceProxy(
        "http://{0}:{1}@{2}".format(
            settings.BITCOIND_RPC_USERNAME,
            settings.BITCOIND_RPC_PASSWORD,
            settings.BITCOIND_RPC_URL
        )
    )
    try:
        account_info = {}
        account_info['wallet_account_address'] = rpc_connect.getaccountaddress(
            user.username)
        account_info['balance'] = rpc_connect.getbalance(user.username)
        account_info['message'] = 'Subscribed'
        useraccount, created = UserAccount.objects.get_or_create(user=user)
        useraccount.wallet_accont_name = user.username
        useraccount.save()
        return account_info
    except JSONRPCException:
        return False


def get_ekata_units_info(user):
    rpc_connect = AuthServiceProxy(
        "http://{0}:{1}@{2}".format(
            settings.BITCOIND_RPC_USERNAME,
            settings.BITCOIND_RPC_PASSWORD,
            settings.BITCOIND_RPC_URL
        )
    )
    try:
        account_info = {}
        account_info['addresses'] =\
            rpc_connect.getaddressesbyaccount(user.username)
        account_info['balance'] = rpc_connect.getbalance(user.username)
        return account_info
    except JSONRPCException:
        return False
