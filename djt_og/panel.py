# ##############################################################################
#  This file is part of djt_og                                                #
#                                                                              #
#  Copyright (C) 2020 Matthieu Gallet <github@19pouces.net>                    #
#  All Rights Reserved                                                         #
#                                                                              #
#  You may use, distribute and modify this code under the                      #
#  terms of the (BSD-like) CeCILL-B license.                                   #
#                                                                              #
#  You should have received a copy of the CeCILL-B license with                #
#  this file. If not, please visit:                                            #
#  https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt (English)           #
#  or https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt (French)         #
#                                                                              #
# ##############################################################################
from functools import lru_cache

import pkg_resources
from debug_toolbar.panels import Panel
from django.http import HttpResponse, HttpRequest

# noinspection PyProtectedMember
from django.template import engines, TemplateSyntaxError
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from djt_og.opengraph import HTMLAnalyzer


def template_from_string(template_string):
    """
    Convert a string into a template object,
    using a given template engine or using the default backends
    from settings.TEMPLATES if no engine was specified.
    """
    # This function is based on django.template.loader.get_template,
    for engine in engines.all():
        try:
            return engine.from_string(template_string)
        except TemplateSyntaxError:
            pass
    raise TemplateSyntaxError(template_string)


class OpenGraphPanel(Panel):
    """Affiche les données OpenGraph"""

    title = "OpenGraph"
    template = "templates/debug/opengraph.html"
    has_content = True

    def generate_stats(self, request: HttpRequest, response: HttpResponse):
        content_type = response["Content-Type"]
        if content_type.startswith("text/html") and (
            response.status_code < 300 or response.status_code >= 400
        ):
            content_text = response.content
            open_graph_data = self.get_data(content_text)
            self.record_stats(open_graph_data)

    def nav_subtitle(self):
        stats = self.get_stats()
        template = (
            "<img src='%(img)s' alt='OpenGraph image' "
            "style='max-height: 2em; max-width: 3em; float: right'> %(title)s"
        )
        values = {
            "img": static("admin/img/icon-no.svg"),
            "title": _("no OpenGraph metadata"),
        }
        if stats.get("is_valid"):
            values["img"] = stats["image"] or static("admin/img/icon-yes.svg")
            values["title"] = stats["og_attrs"].get(
                "title", _("missing OpenGraph title")
            ) or _("empty OpenGraph title")
        return mark_safe(template % values)

    @staticmethod
    def get_data(content_text):
        analyzer = HTMLAnalyzer()
        analyzer.load(content_text)
        result = {
            "is_valid": analyzer.is_valid,
            "image": None,
            "comments": analyzer.comments,
            "og_attrs": analyzer.og_attrs,
            "title": analyzer.title,
            "meta_attrs": analyzer.meta_attrs,
        }
        for x, y in analyzer.og_attrs.items():
            if x == "image":
                result["image"] = y
        return result

    @property
    def content(self):
        """
        Content of the panel when it's displayed in full screen.

        By default this renders the template defined by :attr:`template`.
        Statistics stored with :meth:`record_stats` are available in the
        template's context.
        """
        template = self.get_template()
        context = self.get_stats()
        content = template.render(context)
        return content

    @lru_cache()
    def get_template(self):
        template_filename = pkg_resources.resource_filename("djt_og", self.template)
        with open(template_filename) as fd:
            template_content = fd.read()
        template = template_from_string(template_content)
        return template
