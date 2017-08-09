from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from django.conf import settings

from autosignup.models import CommunitySignup
from autosignup.utils import calculate_referral_and_referrers
from useraccount.utils import get_distribution_rpc_connect,\
    split_distribution, calculate_dist_amount


class Command(BaseCommand):
    help_text = 'This script is for calculating missing bonus and send out'

    def add_arguments(self, parser):
        parser.add_argument('amount', nargs='+', type=float)
        parser.add_argument(
            '--calcamount',
            action='store_true',
            dest='calcamount',
            default=False,
            help='Calc amount needed in main account',
        )
        parser.add_argument(
            '--sendbonus',
            action='store_true',
            dest='sendbonus',
            default=False,
            help='Send bonus from main account',
        )

    def handle(self, *args, **options):
        amount = float(options['amount'][0])
        if options['calcamount']:
            self.calculate_total_amount_needed(amount)
        if options['sendbonus']:
            self.send_bonus(amount)

    def calculate_total_amount_needed(self, amount):
        dist_ammount = calculate_dist_amount(amount)
        bonus_given = 0
        batches = split_distribution()
        total_account = CommunitySignup.objects.filter(
            is_on_distribution=True,
            status='approved'
        ).count()
        for batch in batches:
            no_of_accout = len(batch)
            total_amount = amount * no_of_accout
            referrers, referrals = calculate_referral_and_referrers()
            for account in batch:
                if account.user in referrals:
                    referral_bonus_amount = 0.5 * (total_amount/total_account)
                    bonus_given += referral_bonus_amount
                if account.user in referrers:
                    referrer_bonus_amount = referrers[account.user] * (total_amount/total_account)
                    bonus_given += referrer_bonus_amount
        amount_needed = dist_ammount['total_bonus'] - bonus_given
        self.stdout.write(self.style.SUCCESS(
            'Amount needs: %s' % amount_needed
        ))
        self.stdout.write(self.style.SUCCESS(
            'Original bonus: %s' % dist_ammount['total_bonus']
        ))
        self.stdout.write(self.style.SUCCESS(
            'Bonus given: %s' % bonus_given
        ))
        return amount_needed

    def send_bonus(self, amount):
        total_account = CommunitySignup.objects.filter(
            is_on_distribution=True,
            status='approved'
        ).count()
        amount = float(amount)
        batch_number = 0
        batches = split_distribution()
        for batch in batches:
            batch_number += 1
            send_amount_and_addresses = {}
            log_name = now().strftime("%Y-%m-%d-%H-%I") + '-batch' + str(batch_number) + '.log'
            f = open(
                settings.BASE_DIR + '/media/gc_dist/' + log_name, 'w+'
            )
            no_of_accout = len(batch)
            total_amount = amount * no_of_accout
            f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + ' Total Account: ' + str(no_of_accout))
            referrers, referrals = calculate_referral_and_referrers()
            for account in batch:
                send_amount = 0
                if account.user in referrals:
                    already_sent = 0.5 * (total_amount/total_account)
                    actual_bonus = 0.5 * amount
                    referral_bonus_amount = actual_bonus - already_sent
                    send_amount += referral_bonus_amount
                    f.write(
                        '\n{}: Actual Referral Bonus for {} was {:.6f}'.format(
                            now().strftime("%Y-%m-%d %H:%I"),
                            account.user.username.encode('utf-8'),
                            actual_bonus
                        )
                    )
                    f.write(
                        '\n{}: Sent Referral Bonus for {} was {:.6f}'.format(
                            now().strftime("%Y-%m-%d %H:%I"),
                            account.user.username.encode('utf-8'),
                            already_sent
                        )
                    )
                    f.write(
                        '\n{}: Added {:.6f} Referral Bonus to {}'.format(
                            now().strftime("%Y-%m-%d %H:%I"),
                            referral_bonus_amount,
                            account.user.username.encode('utf-8')
                        )
                    )
                if account.user in referrers:
                    already_sent = referrers[account.user] * (total_amount/total_account)
                    actual_bonus = referrers[account.user] * amount
                    referrer_bonus_amount = actual_bonus - already_sent
                    send_amount += referrer_bonus_amount
                    f.write(
                        '\n{}: Actual Referrer Bonus for {} was {:.6f}'.format(
                            now().strftime("%Y-%m-%d %H:%I"),
                            account.user.username.encode('utf-8'),
                            actual_bonus
                        )
                    )
                    f.write(
                        '\n{}: Sent Referrer Bonus for {} was {:.6f}'.format(
                            now().strftime("%Y-%m-%d %H:%I"),
                            account.user.username.encode('utf-8'),
                            already_sent
                        )
                    )
                    f.write(
                        '\n{}: Added {:.6f} Referrer Bonus to {}'.format(
                            now().strftime("%Y-%m-%d %H:%I"),
                            referrer_bonus_amount,
                            account.user.username.encode('utf-8')
                        )
                    )
                if send_amount > 0.01:
                    if account.wallet_address:
                        send_amount_and_addresses[account.wallet_address] = send_amount
                        f.write('\n{}: {:.6f} Added to distribute for Ekata ID {} Username {}'.format(
                            now().strftime("%Y-%m-%d %H:%I"), send_amount, account.user.profile.ekata_id, account.user.username.encode('utf-8')
                        ))
                    else:
                        f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + account.user.username.encode('utf-8') + "Doesn't have wallet address")
                else:
                    f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + " Dropped distribution for " + account.user.username.encode('utf-8') + " Reason: Total amount is lower than 0.01")
            distribution_rpc_connect = get_distribution_rpc_connect()
            try:
                distribution_rpc_connect.sendmany("", send_amount_and_addresses)
            except JSONRPCException as e:
                failedbatch = FailedDistributionBatch()
                failedbatch.batch_number = batch_number
                failedbatch.save()
                for account in batch:
                    failedbatch.signups.add(account)
                f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + ' Failed Distribution for batch #' + str(batch_number))
                f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ":" + ' Original error message:' + e.message)
            f.write('\n' + now().strftime("%Y-%m-%d %H:%I") + ':' + ' Finished  Distribution Task for batch #' + str(batch_number))
            f.close()
            self.stdout.write(self.style.SUCCESS('Finished one batch'))
