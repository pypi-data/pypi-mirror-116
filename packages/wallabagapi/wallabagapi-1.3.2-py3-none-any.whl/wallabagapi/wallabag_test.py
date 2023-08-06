# coding: utf-8
"""
   Wallabag API - Test
"""

import datetime
import unittest
from unittest import IsolatedAsyncioTestCase
from core import Wallabag


class TestWallabag(IsolatedAsyncioTestCase):

    host = 'http://wallabag:81'
    client_id = ''
    client_secret = ''
    token = ''

    async def asyncSetUp(self):

        params = {"grant_type": "password",
                  "client_id": '1_3847efhvxack8gwog8scg8oowww0csogg4wwoogg0cg444g8k4',
                  "client_secret": 'i1j19n9e7mog0ook48gwo0kck88oskggwgswwg48gsw4sc8gk',
                  "username": 'wallabag',
                  "password": 'wallabag'}

        self.token = await Wallabag.get_token(host=self.host, **params)
        self.format = 'json'
        self.w = Wallabag(host=self.host,
                          token=self.token)

    async def test_get_token(self):
        params = {"grant_type": "password",
                  "client_id": '1_3847efhvxack8gwog8scg8oowww0csogg4wwoogg0cg444g8k4',
                  "client_secret": 'i1j19n9e7mog0ook48gwo0kck88oskggwgswwg48gsw4sc8gk',
                  "username": 'wallabag',
                  "password": 'wallabag'}
        data = await Wallabag.get_token(host=self.host, **params)
        self.assertTrue(isinstance(data, str), True)
        return data

    async def create_entry(self):
        self.format = 'json'

        title = 'the FooBar Title'
        url = 'https://somwhereelse.over.the.raibow.com/'
        tags = ['foo', 'bar']
        starred = 0
        archive = 0
        content = '<p>Additional content</p>'
        language = 'FR'
        published_at = datetime.datetime.now()
        authors = 'John Doe'
        public = 0
        original_url = 'http://localhost'
        data = await self.w.post_entries(url, title, tags, starred, archive,
                                         content, language, published_at, authors,
                                         public, original_url)

        return data

    async def test_get_entries(self):
        params = {'delete': 0,
                  'sort': 'created',
                  'order': 'desc',
                  'page': 1,
                  'perPage': 30,
                  'tags': []}
        data = await self.w.get_entries(**params)
        self.assertIsInstance(data, dict)

    async def test_get_entry(self):
        entry = 1
        self.assertTrue(isinstance(entry, int), True)
        data = await self.w.get_entry(entry)
        self.assertTrue(data, str)

    async def test_get_entry_tags(self):
        entry = 1
        self.assertTrue(isinstance(entry, int), True)
        data = await self.w.get_entry_tags(entry)
        self.assertIsInstance(data, list)

    async def test_get_tags(self):
        data = await self.w.get_tags()
        self.assertIsInstance(data, list)

    async def test_post_entries(self):
        data = await self.create_entry()
        self.assertTrue(data, True)

    async def test_patch_entries(self):
        entry = 1
        params = {'title': 'I change the title',
                  'archive': 0,
                  'tags': ["bimbo", "pipo"],
                  'order': 'asc',
                  'star': 0,
                  'delete': 0}
        self.assertTrue(isinstance(entry, int), True)
        self.assertTrue(isinstance(params, dict), True)
        data = await self.w.patch_entries(entry, **params)
        self.assertTrue(data, True)

    async def test_delete_entries(self):
        entry = await self.create_entry()
        self.assertTrue(isinstance(entry['id'], int), True)
        data = await self.w.delete_entries(entry['id'])
        self.assertTrue(data, True)

    async def test_post_entry_tags(self):
        entry = 1
        self.assertTrue(isinstance(entry, int), True)
        tags = ['foo', 'bar']
        self.assertTrue(isinstance(tags, list), True)
        data = await self.w.post_entry_tags(entry, tags)
        self.assertTrue(data, True)

    """
    def test_delete_entry_tag(self):
        entry = self.create_entry()
        tag = 'bar'
        self.assertTrue(isinstance(entry['id'], int), True)
        self.assertTrue(isinstance(tag, str), True)
        resp = self.w.delete_entry_tag(entry['id'], tag)
        self.assertTrue(resp, True)
    """


if __name__ == '__main__':
    unittest.main()
