from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from arividam.siteconfig.models import SiteConfiguration
from cms.models import GlobalPagePermission, PageUser


class Command(BaseCommand):
    help = 'Creates a school Site'

    def add_arguments(self, parser):
        parser.add_argument('school_code', help='Government assigned School Code')
        parser.add_argument('school_type', help='One of: (hs|hss|vhse)-(govt|aided|unaided)')
        parser.add_argument('school_name', help='School name')
        parser.add_argument('domain', help='School site sub-domain')

    def handle(self, *args, **options):
        code = options['school_code']
        stype = options['school_type']
        name = options['school_name']
        domain = options['domain']
        if domain.find(".") > -1:
            sub_domain = domain.split(".")[0]
        else:
            sub_domain = domain

        full_domain = "{}.arividam.in".format(sub_domain)

        site, _ = Site.objects.get_or_create(name=name, domain=full_domain)
        config, _ = SiteConfiguration.objects.get_or_create(
                site=site,
                school_code=code,
                school_type=stype,
                )

        User = get_user_model()

        admin = User.objects.filter(is_superuser=True)[0]

        egroup, _ = Group.objects.get_or_create(name='Editor')
        wgroup, _ = Group.objects.get_or_create(name='Writer')

        try:
            editor = PageUser.objects.create_user(
                    username="editor@{}".format(sub_domain),
                    password='editorpass',
                    created_by=admin)
            editor.is_staff=True
            editor.save()
            egroup.user_set.add(editor)
        except IntegrityError:
            editor = PageUser.objects.get(username="editor@{}".format(sub_domain))

        try:
            writer = PageUser.objects.create_user(
                username="writer@{}".format(sub_domain),
                password='writerpass',
                created_by=admin)
            wgroup.user_set.add(writer)
        except IntegrityError:
            writer = PageUser.objects.get(username="writer@{}".format(sub_domain))

        gpe, _ = GlobalPagePermission.objects.get_or_create(
                user=editor,
                can_change=True,
                can_add=True,
                can_delete=True,
                can_change_advanced_settings=True,
                can_publish=True,
                can_change_permissions=True,
                can_move_page=True)
        gpe.sites.add(site)

        gpw, _ = GlobalPagePermission.objects.get_or_create(
                user=writer,
                can_change=True,
                can_add=True,
                can_delete=True,
                can_publish=False)
        gpw.sites.add(site)

