from django.core.management.base import BaseCommand
from cms.models import Title

class Command(BaseCommand):
    help = 'Fix CMS pages (publisher_public_id foreign key)'

    def handle(self, *args, **options):
        ts = Title.objects.filter(
            publisher_is_draft=False,
            page_id__isnull=False,
            publisher_public_id__isnull=False
        )

        fixed_count = 0

        # for each of the (non-draft, draft) title pairs, fix the equivalent (non-draft, draft) page pairs
        for t in ts:
            fixed = False

            if t.publisher_public.page.publisher_public is None:
                self.stdout.write('Draft page id {} has a null publisher_public_id (it should be {})'.format(
                    t.publisher_public.page_id,
                    t.page_id
                ))
                t.publisher_public.page.publisher_public = t.page
                t.publisher_public.page.save()
                fixed = True

            if t.page.publisher_public is None:
                self.stdout.write('Non-draft page id {} has a null publisher_public_id (it should be {})'.format(
                    t.page_id,
                    t.publisher_public.page_id
                ))
                t.page.publisher_public = t.publisher_public.page
                t.page.save()
                fixed = True

            if fixed:
                fixed_count += 1

        self.stdout.write('Fixed {} pairs of pages.'.format(fixed_count))
