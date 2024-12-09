# -*- coding: utf-8 -*-
{
    'name': "Real Estate Ads Udemy",
    'summary': """
        Aplicación realizada a partir de curso de Udemy Zero to Hero""",
    'description': """
        Aplicación de practica
    """,
    'author': "Ing. Rafael López Flores",
    'website': "http://www.yourcompany.com",
    'category': 'Rafael',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        # groups

    ],
    'demo': [
        'demo/property_tag.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'real_estate_ads/static/src/js/my_custom_tag.js',
            'real_estate_ads/static/src/xml/my_custom_tag.xml',
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
