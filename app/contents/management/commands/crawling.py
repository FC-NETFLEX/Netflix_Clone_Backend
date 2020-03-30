from django.core.management.base import BaseCommand

from contents.management.commands.crawler import get_url, get_item


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for movie_url in get_url():
            get_item(movie_url)

        return self.stdout.write('크롤링 완료')
