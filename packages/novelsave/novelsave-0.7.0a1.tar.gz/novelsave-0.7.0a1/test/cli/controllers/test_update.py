import unittest
from unittest.mock import patch

from loguru import logger

from novelsave.cli.controllers import update


@patch('novelsave.cli.controllers._update.helpers.download_pending')
@patch('novelsave.cli.controllers._update.helpers.download_thumbnail')
@patch('novelsave.cli.controllers._update.helpers.update_novel')
@patch('novelsave.cli.controllers._update.helpers.create_novel', return_value=None)
@patch('novelsave.cli.controllers._update.helpers.get_novel', return_value=None)
class TestUpdateController(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.remove()

    def test_update_not_exists(self, get_novel, create_novel, update_novel, download_thumbnail, download_pending):
        get_novel.side_effect = ValueError()
        create_novel.return_value = None

        with self.assertRaises(SystemExit):
            update('not int', 0)
        get_novel.assert_called_with('not int')
        create_novel.assert_not_called()

        with self.assertRaises(SystemExit):
            update('1', 0)
        get_novel.assert_called_with('1')
        create_novel.assert_not_called()

        update('https://my.site.org', False)
        get_novel.assert_called_with('https://my.site.org')
        create_novel.assert_called_with('https://my.site.org')

    def test_update_exists(self, get_novel, create_novel, update_novel, download_thumbnail, download_pending):
        get_novel.return_value = 'novel'

        url = 'https://novel.site'
        update(url, 1)

        get_novel.assert_called_with(url)
        update_novel.assert_called_with('novel')
        download_pending.assert_called_with('novel', 1)

    def test_update_exists_skip_chapters(self, get_novel, create_novel, update_novel, download_thumbnail,
                                         download_pending):
        get_novel.return_value = 'novel'

        url = 'https://novel.site'
        update(url, limit=0)

        get_novel.assert_called_with(url)
        update_novel.assert_called_with('novel')
        download_pending.assert_not_called()

