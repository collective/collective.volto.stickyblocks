# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

from collective.volto.stickyblocks.testing import (  # noqa: E501
    COLLECTIVE_VOLTO_STICKYBLOCKS_INTEGRATION_TESTING,
)

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.volto.stickyblocks is properly installed."""

    layer = COLLECTIVE_VOLTO_STICKYBLOCKS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.volto.stickyblocks is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.volto.stickyblocks")
        )

    def test_browserlayer(self):
        """Test that ICollectiveVoltoStickyblocksLayer is registered."""
        from plone.browserlayer import utils

        from collective.volto.stickyblocks.interfaces import (
            ICollectiveVoltoStickyblocksLayer,
        )

        self.assertIn(ICollectiveVoltoStickyblocksLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_VOLTO_STICKYBLOCKS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.volto.stickyblocks")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.volto.stickyblocks is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.volto.stickyblocks")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveVoltoStickyblocksLayer is removed."""
        from plone.browserlayer import utils

        from collective.volto.stickyblocks.interfaces import (
            ICollectiveVoltoStickyblocksLayer,
        )

        self.assertNotIn(ICollectiveVoltoStickyblocksLayer, utils.registered_layers())
