{
    'name': 'ITC Internal Carta Porte',
    'version': '17.0.1.0.0',
    'summary': 'Habilita Carta Porte en traslados internos seleccionados',
    'category': 'Inventory/Inventory',
    'author': 'ITC',
    'license': 'LGPL-3',
    'depends': [
        'l10n_mx_edi_stock_30',
    ],
    'data': [
        'views/stock_picking_type_views.xml',
    ],
    'installable': True,
    'application': False,
}
