from unittest import TestCase

import pkg_resources

from djt_og.opengraph import HTMLAnalyzer


class TestPanel(TestCase):
    def test_panel(self):
        filename = pkg_resources.resource_filename("djt_og_test", "sample.html")
        with open(filename) as fd:
            content_text = fd.read()
        analyzer = HTMLAnalyzer()
        analyzer.load(content_text)
        self.assertEqual("ExamplePage", analyzer.title)
        self.assertEqual(
            {"author": "ExamplePage", "keywords": None, "description": "ExamplePage",},
            analyzer.meta_attrs,
        )
        self.assertEqual(
            {
                "description": "ExamplePage",
                "image": "http://localhost:9000/static/favicon/favicon-194x194.png",
                "locale": "fr_FR",
                "site_name": "ExamplePage",
                "title": "",
                "type": "website",
                "url": "http://localhost:9000/",
            },
            analyzer.og_attrs,
        )
        self.assertTrue(analyzer.is_valid)
