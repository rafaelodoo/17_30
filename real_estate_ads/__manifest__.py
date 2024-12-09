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
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_type_tag.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',
        'data/property_type.xml',
        'data/estate.property.type.csv',
        # Nuevo archivo para el conector de API
        #'views/api_connector_views.xml',
        'views/character_wizard_views.xml',
        'views/estate.property.type.csv',
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
