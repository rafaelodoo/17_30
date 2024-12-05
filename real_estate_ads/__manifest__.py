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
        'security/res_groups.csv',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_type_tag.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',
        'data/property_type.xml',
        'data/estate.property.type.csv'
    ],
    'demo': [
        'demo/property_tag.xml'
    ],
    'installable':True,
    'application':True,
    'license':'LGPL-3'
}