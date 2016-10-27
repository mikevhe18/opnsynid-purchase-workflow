# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Request Type To RFQ',
    'version': '8.0.1.0.0',
    'summary': 'Insert purchase request type from purchase request lines',
    'author': 'OpenSynergy Indonesia,Odoo Community Association (OCA)',
    'website': 'https://opensynergy-indonesia.com',
    'category': 'Purchase Management',
    'depends': [
        'purchase_request_type',
        'purchase_request_to_rfq'
    ],
    'data': [
        'views/purchase_request_line_make_purchase_order_view.xml'
    ],
    'installable': True,
    'license': 'AGPL-3',
}
