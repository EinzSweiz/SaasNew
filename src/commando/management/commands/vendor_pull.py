from typing import Any
import helpers
from django.core.management.base import BaseCommand
from django.conf import settings

# STATICFILES_VENDOR_DIRS = settings.STATICFILES_VENDOR_DIRS
STATICFILES_VENDOR_DIRS = getattr(settings, 'STATICFILES_VENDOR_DIRS')

VENDOR_STATICFILES = {
    'flowbite.min.css': 'https://cdn.jsdelivr.net/npm/flowbite@2.5.1/dist/flowbite.min.css',
    'flowbite.min.js': 'https://cdn.jsdelivr.net/npm/flowbite@2.5.1/dist/flowbite.min.js',
    'flowbite.min.js.map': "https://cdn.jsdelivr.net/npm/flowbite@2.5.1/dist/flowbite.min.js.map",
    

}

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('Downloading static files')
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            dest_path = STATICFILES_VENDOR_DIRS / name
            success = helpers.download_to_local(url, dest_path)
            if success:
                completed_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR( f'Failed to download {url}')
                    )
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully updated vendor files'
                    )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Some files were not updated'
                )
            )
 