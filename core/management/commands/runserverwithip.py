from django.core.management.base import BaseCommand, CommandError
import subprocess


class Command(BaseCommand):
    help = "Run pythonserver with system IP"

    def handle(self, *args, **options):
        IP = ''

        if subprocess.call(['ipconfig', 'getifaddr', 'en1']) is not 1:
            IP = subprocess.call(['ipconfig', 'getifaddr', 'en1'])
            self.stdout.write(IP)

        elif subprocess.call(['ipconfig', 'getifaddr', 'en0']) is not 1:
            IP = subprocess.call(['ipconfig', 'getifaddr', 'en0'])
            self.stdout.write(IP)

        else:
            self.stdout.write('No Internet Connection Available')

