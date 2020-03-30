from django.core.management.base import BaseCommand
from contents.management.commands.crawler import get_url, get_item
import mimetypes
import requests
import magic
from django.core.files.uploadedfile import SimpleUploadedFile
from contents.models import Contents, Category, Actor, Director


class Command(BaseCommand):

    def handle(self, *args, **options):
        url_list = get_url()

        for url in url_list:
            item = get_item(url)
            contents, is_create = Contents.objects.get_or_create(contents_title=item['title'])

            if is_create:
                response = requests.get(item['image_url'])
                binary_data = response.content
                mime_type = magic.from_buffer(binary_data, mime=True)
                ext = mimetypes.guess_extension(mime_type)
                file = SimpleUploadedFile(f'{item["title"]}{ext}', binary_data)

                contents.contents_summary = item['summary']
                contents.contents_title_english = item['title_english']
                contents.contents_image = file
                contents.contents_rating = item['rating']
                contents.contents_length = item['length']
                contents.contents_pub_year = item['pub_year']
                contents.save()

                for category in item['genre']:
                    c1, _ = Category.objects.get_or_create(category_name=category)

                for actor in item['actor']:
                    a1, _ = Actor.objects.get_or_create(actor_name=actor)
                    contents.actors.add(a1)

                for director in item['director']:
                    d1, _ = Director.objects.get_or_create(director_name=director)
                    contents.directors.add(d1)

        return self.stdout.write('크롤링 완료')
