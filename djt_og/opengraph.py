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


# noinspection PyProtectedMember
from bs4 import BeautifulSoup, Tag


class HTMLAnalyzer:
    required_og_attrs = {"title", "type", "image", "url"}
    used_meta_attrs = {"author", "description", "keywords"}

    def __init__(self):
        self.og_attrs = {}
        self.meta_attrs = {x: None for x in self.used_meta_attrs}
        self.title = None
        self.bs_doc = None
        self.comments = []
        self.is_valid = False

    def load(self, html: str):
        try:
            self.bs_doc = BeautifulSoup(html, features="html.parser")
        except Exception as e:
            self.comments.append("Unable to parse the HTML content (%(e)s)" % {"e": e})
            return
        if not self.bs_doc.html:
            self.comments.append("Unable to find the root html tag.")
            return
        if not self.bs_doc.html.head:
            self.comments.append("Unable to find the HTML head tag.")
            return
        head = self.bs_doc.html.head  # type: Tag
        og_attrs = {}
        for child in head.find_all():  # type: Tag
            if child.name == "title":
                self.title = "\n".join(child.contents)
            elif child.name == "meta" and child.attrs.get("property", "").startswith(
                "og:"
            ):
                og_attrs[child["property"][3:]] = child.attrs.get("content", "")
            elif (
                child.name == "meta"
                and child.attrs.get("name", "") in self.used_meta_attrs
            ):
                self.meta_attrs[child["name"]] = child.attrs.get("content", None)
        self.og_attrs = {x: y for (x, y) in sorted(og_attrs.items())}
        self.is_valid = all(
            self.og_attrs.get(x) is not None for x in self.required_og_attrs
        )
