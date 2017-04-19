import json
import os
import logging
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from django.conf import settings
from django.contrib.auth.models import User
from useraccount.models import UserAccount, Transaction


rpc_connect = AuthServiceProxy(
    "http://{0}:{1}@{2}".format(
        settings.BITCOIND_RPC_USERNAME,
        settings.BITCOIND_RPC_PASSWORD,
        settings.BITCOIND_RPC_URL
    )
)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file_base = os.path.join(settings.BASE_DIR, 'logs')


def setup_logger(log_file, level=logging.DEBUG):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger("BitcoinRPC")
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def create_ekata_units_account(user):
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/subscribe.log')
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


def get_ekata_units_info(account_name):
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/getinfo.log')
    try:
        account_info = {}
        account_info['addresses'] =\
            rpc_connect.getaddressesbyaccount(account_name)
        account_info['balance'] = rpc_connect.getbalance(account_name)
        return account_info
    except JSONRPCException:
        return False


def send_ekata_units(from_user, to_user, amount, instruction):
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/transfer.log')
    try:
        rpc_connect.move(from_user, to_user, amount)
        from_u = User.objects.get(username=from_user)
        to_u = User.objects.get(username=to_user)
        Transaction.objects.create(
            from_user=from_u,
            to_user=to_u,
            units=amount,
            instruction=instruction
        )
        return False
    except JSONRPCException:
        return False


def dist_ekata_units(amount):
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/dist.log')
    for account in UserAccount.objects.all():
        rpc_connect.move("", account.wallet_accont_name, amount)
    return True
