import json
import os
import logging
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from twilio.rest import TwilioRestClient

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from useraccount.models import UserAccount, Transaction, UserDistribution,\
    AdminDistribution, DistributionPhone
from autosignup.utils import calculate_referral_and_referrers
from notification.utils import create_notification
from usertimeline.models import UserTimeline
from autosignup.models import CommunitySignup

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
        # rpc_connect.move("", user.username,
        #                  settings.EKATA_UNITS_INITIAL_BALANCE)
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
    amount = float(amount)
    try:
        d_phone = DistributionPhone.objects.latest()
    except:
        d_phone = None
    rpc_connect = get_rpc_connect()
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/dist.log')
    dist_accounts = CommunitySignup.objects.filter(
        is_on_distribution=True,
        status='approved'
    )
    log_name = now().strftime("%Y-%m-%d-%H:%I") + '.log'
    f = open(
        settings.BASE_DIR + '/media/gc_dist/' + log_name, 'w+'
    )
    f.write(now().strftime("%Y-%m-%d %H:%I") + ':' + ' Distribution started')
    admindist = AdminDistribution()
    admindist.amount_per_user = amount
    no_of_accout = dist_accounts.count()
    total_amount = amount * no_of_accout
    total_amount_with_bonus = 0
    f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + ' Total Account: ' + str(no_of_accout))
    referrers, referrals = calculate_referral_and_referrers()
    for account in dist_accounts:
        send_amount = amount
        if account.user in referrals:
            referral_bonus_amount = 0.5 * (total_amount/no_of_accout)
            send_amount += referral_bonus_amount
            f.write(
                '\n{}: Added {:.6f} Referral Bonus to {}'.format(
                    now().strftime("%Y-%m-%d %H:%I"), referral_bonus_amount, account.user.username
                )
            )
        if account.user in referrers:
            referrer_bonus_amount = referrers[account.user] * (total_amount/no_of_accout)
            send_amount += referrer_bonus_amount
            f.write(
                '\n{}: Added {:.6f} Referrer Bonus to {}'.format(
                    now().strftime("%Y-%m-%d %H:%I"), referrer_bonus_amount, account.user.username
                )
            )
        if send_amount > 0.01:
            if account.wallet_address:
                try:
                    rpc_connect.sendfrom("", account.wallet_address, send_amount)
                    # rpc_connect.move("", account.user.username, send_amount)
                    f.write('\n{}: Distributed {:.6f} to Ekata ID {} Username {}'.format(
                        now().strftime("%Y-%m-%d %H:%I"), send_amount, account.user.profile.ekata_id, account.user.username
                    ))
                    total_amount_with_bonus += send_amount
                    usertimeline = UserTimeline(
                        user=account.user,
                        timeline_type=7,
                        amount=send_amount
                    )
                    usertimeline.save()
                    create_notification(
                        user=account.user,
                        ntype=14,
                        amount=send_amount,
                        timeline_id=usertimeline.id
                    )
                except JSONRPCException as e:
                    f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + ' Failed Distribution for ' + account.user.username)
                    f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ":" + ' Original error message:' + e.message)
            else:
                f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + account.user.username + "Doesn't have wallet address")
        else:
            f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + " Dropped distribution for " + account.user.username + " Reason: Total amount is lower than 0.01")
    f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + ' Finished  Distribution')
    f.write('\n{}: Total Amount Distributed With Bonus: {:.6f}'.format(now().strftime("%Y-%m-%d %H:%I"), total_amount_with_bonus))
    f.close()
    admindist.end_time = now()
    admindist.no_of_accout = no_of_accout
    admindist.total_amount = total_amount_with_bonus
    admindist.log_file_path = log_name
    admindist.save()
    send_sms(
        phone_no=d_phone.phone_number,
        body='Distribution finished at: {}'.format(now())
    )
    return True


def single_dist(to_user, amount):
    rpc_connect = get_rpc_connect()
    setup_logger(
        os.path.join(log_file_base, 'ekata_units_logs') + '/transfer.log')
    address_is_valid = validate_address(to_user)
    try:
        if address_is_valid:
            rpc_connect.sendfrom("", to_user, amount)
        else:
            rpc_connect.move("", to_user, amount)
    except JSONRPCException:
        return False
    return True


def calculate_dist_amount(amount):
    total_amount = {}
    referrers, referrals = calculate_referral_and_referrers()
    dist_accounts = CommunitySignup.objects.filter(
        is_on_distribution=True,
        status='approved'
    )
    rpc_connect = get_rpc_connect()
    info = rpc_connect.getinfo()
    total_amount['coin_fees'] = dist_accounts.count() * info['paytxfee']
    total_amount['basic_income'] = dist_accounts.count() * amount
    total_bonus = 0
    for account in dist_accounts:
        if account.user in referrals:
            referral_bonus_amount = 0.5 * (amount * dist_accounts.count()/dist_accounts.count())
            total_bonus += referral_bonus_amount
        if account.user in referrers:
            referrer_bonus_amount =\
                referrers[account.user] * (amount * dist_accounts.count()/dist_accounts.count())
            total_bonus += referrer_bonus_amount
    total_amount['total_bonus'] = total_bonus
    total_amount['total'] = float(total_amount['coin_fees']) +\
        float(total_amount['basic_income']) + float(total_amount['total_bonus'])
    return total_amount


def get_connection_data():
    rpc_connect = get_rpc_connect()
    info = rpc_connect.getinfo()
    return info['connections']