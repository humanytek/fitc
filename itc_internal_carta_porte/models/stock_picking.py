from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends(
        'company_id',
        'picking_type_code',
        'picking_type_id.x_itc_enable_internal_carta_porte',
    )
    def _compute_l10n_mx_edi_is_delivery_guide_needed(self):
        super()._compute_l10n_mx_edi_is_delivery_guide_needed()

        for picking in self:
            if (
                picking.country_code == 'MX'
                and picking.picking_type_code == 'internal'
                and picking.picking_type_id.x_itc_enable_internal_carta_porte
            ):
                picking.l10n_mx_edi_is_delivery_guide_needed = True
