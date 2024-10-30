from .utils import ApiResourceTestCase
from perma.models import LinkUser


class CurrentUserResourceTestCase(ApiResourceTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.registrar_user = LinkUser.objects.get(pk=2)
        cls.org_user = LinkUser.objects.get(pk=3)
        cls.regular_user = LinkUser.objects.get(pk=4)
        cls.sponsored_user = LinkUser.objects.get(pk=20)
        cls.detail_url = cls.url_base+'/user/'
        cls.fields = [
            'id',
            'first_name',
            'last_name',
            'short_name',
            'full_name',
            'top_level_folders',
        ]

    def test_get_self_detail_json(self):
        cases = [
            (self.regular_user, [
                {'id': 25, 'name': 'Personal Links', 'parent': None, 'organization': None, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': True, 'path': '25'},
            ]),
            (self.org_user, [
                {'id': 24, 'name': 'Personal Links', 'parent': None, 'organization': None, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': False, 'path': '24'},
                {'id': 27, 'name': 'Test Journal', 'parent': None, 'organization': 1, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': True, 'path': '27'}
            ]),
            (self.registrar_user, [
                {'id': 23, 'name': 'Personal Links', 'parent': None, 'organization': None, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': False, 'path': '23'},
                {'id': 28, 'name': 'Another Journal', 'parent': None, 'organization': 2, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': True, 'path': '28'},
                {'id': 31, 'name': 'A Third Journal', 'parent': None, 'organization': 3, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': True, 'path': '31'},
                {'id': 27, 'name': 'Test Journal', 'parent': None, 'organization': 1, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': True, 'path': '27'},
            ]),
            (self.sponsored_user, [
                {'id': 55, 'name': 'Personal Links', 'parent': None, 'organization': None, 'sponsored_by': None, 'is_sponsored_root_folder': False, 'read_only': False, 'has_children': False, 'path': '55'},
                {'id': 59, 'name': 'Sponsored Links', 'parent': None, 'organization': None, 'sponsored_by': None, 'is_sponsored_root_folder': True, 'read_only': False, 'has_children': True, 'path': '59'},
            ]),
        ]
        for user, top_level_folders in cases:
            data = self.successful_get(self.detail_url, user=user, fields=self.fields)
            self.assertEqual(data['top_level_folders'], top_level_folders)

    def test_get_archives_json(self):
        self.successful_get(self.detail_url + 'archives/', user=self.org_user, count=17)
        self.successful_get(self.detail_url + 'archives/', user=self.regular_user, count=17)

    def test_get_folders_json(self):
        self.successful_get(self.detail_url + 'folders/', user=self.org_user, count=2)

    def test_get_orgs_json(self):
        self.successful_get(self.detail_url + 'organizations/', user=self.org_user, count=1)
