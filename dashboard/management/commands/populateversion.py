import subprocess

from django.core.management.base import BaseCommand
from dashboard.models import VersionInfo


class Command(BaseCommand):
    help_text = 'Fetch git tag string and populate to version model'

    def add_arguments(self, parser):
        parser.add_argument('version_name', nargs='+', type=str)
        parser.add_argument('version_color', nargs='+', type=str)

    def handle(self, *args, **options):
        git_version = subprocess.check_output(['git', 'describe']).split('-')
        print(git_version)
        git_version = git_version[0]
        print(git_version)
        self.stdout.write(
            self.style.SUCCESS(
                "Latest tag is {}".format(git_version.strip())
            )
        )
        version_color = options['version_color']
        version_name = options['version_name']
        verinfo, created = VersionInfo.objects.get_or_create(
            name=version_name[0]
        )
        verinfo.version_number = git_version
        verinfo.color = 'bg-{}'.format(version_color[0])
        verinfo.save()
        self.stdout.write(
            self.style.SUCCESS(
                "Populated VersionInfo with color: bg-{0}, name: {1}"
                " version: {2}".format(
                    version_color[0], version_name[0], git_version
                )
            )
        )
