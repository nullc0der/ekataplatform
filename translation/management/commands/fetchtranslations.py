import importlib
import json
import requests

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

API_KEY = settings.GOOGLE_TRANSLATE_API_KEY


class Command(BaseCommand):
    help_text = 'Fetch translation from google API'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('STARTING SCRIPT.....')
        )
        languages = settings.LANGUAGES
        for language in languages:
            if language[0] != 'en':
                self.stdout.write(
                    self.style.SUCCESS(
                        'Creating locale file for {}'.format(language[0])
                    )
                )
                call_command('makemessages',  '-l{}'.format(language[0]))
                langdict = {}
                c = 0
                t_file = open(
                    settings.BASE_DIR + '/locale/{}/LC_MESSAGES/django.po'.format(language[0]))
                for t in t_file:
                    if t.startswith('msgid'):
                        t_eng = t[6:]
                        t_oth = next(t_file)
                        if t_eng.strip() != '""':
                            langdict[t_eng.strip()] = t_oth[7:].strip()
                t_file.close()
                t_file = open(
                    settings.BASE_DIR + '/locale/{}/LC_MESSAGES/django.po'.format(language[0]), 'w+')
                t_file.write(
                    r'msgid ""'
                    '\n'
                    r'msgstr ""'
                    '\n'
                    r'"MIME-Version: 1.0\n"'
                    '\n'
                    r'"Content-Type: text/plain; charset=UTF-8\n"'
                    '\n'
                    r'"Content-Transfer-Encoding: 8bit\n"'
                    '\n'
                    r'"Plural-Forms: nplurals=2; plural=(n != 1);\n"'
                    '\n'
                )
                for key in langdict:
                    if langdict[key] == '""':
                        try:
                            res = requests.get(
                                "https://translation.googleapis.com/"
                                "language/translate/"
                                "v2?key={}&source=en&target={}&q={}"
                                .format(API_KEY, language[0], key.strip('"'))
                            )
                            c += 1
                            if res.status_code == 200:
                                data = json.loads(res.content)
                                translated_text = data['data']['translations'][0]['translatedText'].encode('utf-8')
                                print(translated_text)
                                langdict[key] = '"{}"'.format(translated_text)
                        except:
                            pass
                for key in langdict:
                    t_file.write('msgid {}\n'.format(key))
                    t_file.write('msgstr {}\n'.format(langdict[key]))
                t_file.close()
                self.stdout.write(
                    self.style.SUCCESS(
                        'Translate API called {} times for {}'.format(c, language[0])
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Compiling locale file for {}'.format(language[0])
                    )
                )
                call_command('makemessages',  '-l{}'.format(language[0]))
                call_command('compilemessages',  '-l{}'.format(language[0]))
