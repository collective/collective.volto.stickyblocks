# -*- coding: utf-8 -*-
"""Tests for the @sticky-blocks restapi endpoint."""
import unittest

from collective.volto.stickyblocks.restapi.sticky_blocks.get import StickyBlocks
from collective.volto.stickyblocks.testing import (  # noqa: E501
    COLLECTIVE_VOLTO_STICKYBLOCKS_NOT_INSTALLED_INTEGRATION_TESTING,
)


class TestStickyBlocksGetWhenNotInstalled(unittest.TestCase):
    """https://github.com/collective/collective.volto.stickyblocks/issues/1

    If the package is only present on the Python path but its GenericSetup
    profile was never applied to the site (e.g. it is a dependency of some
    other add-on, or just installed but not activated), the registry record
    does not exist and looking it up must not blow up with a KeyError.
    """

    layer = COLLECTIVE_VOLTO_STICKYBLOCKS_NOT_INSTALLED_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def test_get_config_does_not_raise_keyerror(self):
        sticky_blocks = StickyBlocks(self.portal, self.request)
        try:
            config = sticky_blocks.get_config()
        except KeyError:
            self.fail(
                "get_config() raised KeyError when the product is present "
                "but not installed on the site"
            )
        self.assertEqual(config, [])

    def test_get_sticky_blocks_does_not_raise_keyerror(self):
        sticky_blocks = StickyBlocks(self.portal, self.request)
        try:
            result = sticky_blocks.get_sticky_blocks()
        except KeyError:
            self.fail(
                "get_sticky_blocks() raised KeyError when the product is "
                "present but not installed on the site"
            )
        self.assertEqual(result, [])
