# -*- coding: utf-8 -*-
{
    'name': "Real Estate Ads Udemy 2",
    'summary': """
        Esta aplicación esta desarrollada con fines del curso de Udemy 1""",
    'description': """
        Aplicación chida
    """,
    'author': "Rafapolis",
    'website': "http://www.yourcompany.com",
    'category': 'Rafael',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
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