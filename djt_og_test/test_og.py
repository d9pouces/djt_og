from unittest import TestCase

from djt_og.opengraph import HTMLAnalyzer

content_text = """<!doctype html>
<html lang="fr" prefix="og: http://ogp.me/ns#">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <TITLE>ExamplePage</TITLE>
    <meta name="description" content="ExamplePage"/>
    <meta name="author" content="ExamplePage"/>

    <meta property="og:title" content=""/>
    <meta property="og:type" content="website"/>
    <meta property="og:url" content="http://localhost:9000/"/>
    <meta property="og:image" content="http://localhost:9000/static/favicon/favicon-194x194.png"/>
    <meta property="og:description" content="ExamplePage"/>
    <meta property="og:locale" content="fr_FR"/>
    <meta property="og:site_name" content="ExamplePage"/>

    
      <meta name="apple-mobile-web-app-title" content="ExamplePage"/>
      <meta name="application-name" content="ExamplePage"/>
      <meta name="msapplication-TileColor" content="#423f2c"/>
      <meta name="msapplication-TileImage" content="/static/favicon/mstile-144x144.png"/>
      <meta name="theme-color" content="#423f2c"/>
    
</head>
<body>

</body>
</html>"""


class TestPanel(TestCase):
    def test_panel(self):
        analyzer = HTMLAnalyzer()
        analyzer.load(content_text)
        self.assertEqual("ExamplePage", analyzer.title)
        self.assertEqual(
            {"author": "ExamplePage", "keywords": None, "description": "ExamplePage"},
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
