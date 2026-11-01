from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    x_itc_enable_internal_carta_porte = fields.Boolean(
        string='Permitir Carta Porte en traslado interno',
        help=(
            'Permite que los traslados internos de este tipo de operación sean '
            'considerados para Carta Porte por la localización mexicana.'
        ),
    )
