from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends(
        "company_id",
        "picking_type_code",
        "picking_type_id.x_itc_enable_internal_carta_porte",
    )
    def _compute_l10n_mx_edi_is_delivery_guide_needed(self):
        super()._compute_l10n_mx_edi_is_delivery_guide_needed()

        for picking in self:
            if (
                picking.country_code == "MX"
                and picking.picking_type_code == "internal"
                and picking.picking_type_id.x_itc_enable_internal_carta_porte
            ):
                picking.l10n_mx_edi_is_delivery_guide_needed = True

    def _l10n_mx_edi_add_picking_cfdi_values(self, cfdi_values):
        super()._l10n_mx_edi_add_picking_cfdi_values(cfdi_values)

        if not (
            self.country_code == "MX"
            and self.picking_type_code == "internal"
            and self.picking_type_id.x_itc_enable_internal_carta_porte
        ):
            return

        origin_partner = self.picking_type_id.warehouse_id.partner_id
        destination_partner = self.partner_id

        emisor = cfdi_values["emisor"]
        receptor = cfdi_values["receptor"]

        # Origen = almacén que expide (Jacarandas)
        cfdi_values["origen"]["rfc_remitente_destinatario"] = emisor["rfc"]
        cfdi_values["origen"]["num_reg_id_trib"] = None
        cfdi_values["origen"]["residencia_fiscal"] = None
        self._l10n_mx_edi_add_domicilio_cfdi_values(
            cfdi_values["origen"],
            origin_partner,
        )

        # Destino = contacto seleccionado en el traslado (Gavilanes)
        cfdi_values["destino"]["rfc_remitente_destinatario"] = receptor["rfc"]
        cfdi_values["destino"]["num_reg_id_trib"] = None
        cfdi_values["destino"]["residencia_fiscal"] = None
        self._l10n_mx_edi_add_domicilio_cfdi_values(
            cfdi_values["destino"],
            destination_partner,
        )
