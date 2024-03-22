import json

from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface, implementer

from collective.volto.stickyblocks.interfaces import IStickyBlocks


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class StickyBlocksGet(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "sticky-blocks": {
                "@id": "{}/@sticky-blocks".format(self.context.absolute_url())
            }
        }

        if not expand:
            return result

        result["sticky-blocks"] = self.get_sticky_blocks()

        return json_compatible(result)

    def get_sticky_blocks(self):
        """Get sticky blocks for the current context"""

        context_path = "/".join(self.context.getPhysicalPath())

        for item in self.get_config():
            if item["rootPath"] == context_path:
                return item

    def get_config(self):
        return json.loads(
            api.portal.get_registry_record(
                interface=IStickyBlocks,
                name="sticky_blocks_configuration",
                default="[]",
            )
        )


class ExternalLinksGet(Service):
    def reply(self):
        sticky_blocks = ExternalLinks(self.context, self.request)

        return sticky_blocks(expand=True)
