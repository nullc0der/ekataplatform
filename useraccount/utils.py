import json
import os
import logging
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from twilio.rest import TwilioRestClient

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from useraccount.models import UserAccount, Transaction, UserDistribution,\
    AdminDistribution

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file_base = os.path.join(settings.BASE_DIR, 'logs')


def get_rpc_connect():
    rpc_connect = AuthServiceProxy(
        "http://{0}:{1}@{2}".format(
            settings.BITCOIND_RPC_USERNAME,
            settings.BITCOIND_RPC_PASSWORD,
            settings.BITCOIND_RPC_URL
        )
    )
    return rpc_connect


def setup_logger(log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger("BitcoinRPC")
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def create_ekata_units_account(user):
    rpc_connect = get_rpc_connect()
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/subscribe.log')
    try:
        account_info = {}
        account_info['wallet_account_address'] = rpc_connect.getaccountaddress(
            user.username)
        rpc_connect.move("", user.username,
                         settings.EKATA_UNITS_INITIAL_BALANCE)
        account_info['balance'] = rpc_connect.getbalance(user.username)
        account_info['message'] = 'Subscribed'
        useraccount, created = UserAccount.objects.get_or_create(user=user)
        useraccount.wallet_accont_name = user.username
        useraccount.save()
        return account_info
    except JSONRPCException:
        return False


def request_new_address(account_name):
    rpc_connect = get_rpc_connect()
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/newaddressreq.log')
    try:
        address = rpc_connect.getnewaddress(account_name)
        return address
    except JSONRPCException:
        return False


def get_ekata_units_info(account_name):
    rpc_connect = get_rpc_connect()
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


def validate_address(address):
    rpc_connect = get_rpc_connect()
    try:
        res = rpc_connect.validateaddress(address)
        return res['isvalid']
    except JSONRPCException:
        return False


def send_ekata_units(from_user, to_user, amount):
    rpc_connect = get_rpc_connect()
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/transfer.log')
    address_is_valid = validate_address(to_user)
    try:
        if address_is_valid:
            rpc_connect.sendfrom(from_user, to_user, amount)
        else:
            rpc_connect.move(from_user, to_user, amount)
        Transaction.objects.create(
            from_user=from_user,
            to_user=to_user,
            units=amount
        )
    except JSONRPCException:
        return False
    return True


def send_sms(phone_no, body):
    account_sid = settings.EKATA_TWILIO_ACCOUNT_SID
    auth_token = settings.EKATA_TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        to=phone_no,
        from_=settings.EKATA_TWILIO_PHONE_NO
    )


def send_distribute_phone_verfication(phone_no, code):
    send_sms(
        phone_no=phone_no,
        body='Use verification code to distribution: '
        + code + '\nvalid for 120 sec'
    )


def dist_ekata_units(amount):
    rpc_connect = get_rpc_connect()
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/dist.log')
    admindist = AdminDistribution()
    for account in UserAccount.objects.all():
        rpc_connect.move("", account.wallet_accont_name, amount)
    admindist.end_time = now()
    admindist.no_of_accout = UserAccount.objects.count()
    admindist.total_amount = UserAccount.objects.count() * float(amount)
    admindist.amount_per_user = float(amount)
    admindist.save()
    send_sms(
        phone_no=settings.EKATA_UNITS_VERIFY_NO,
        body='Distribution finished at: {}'.format(now())
    )
    return True
