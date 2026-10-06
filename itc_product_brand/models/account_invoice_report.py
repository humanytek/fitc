from odoo import api, fields, models
from odoo.addons.account.report.account_invoice_report import (
    AccountInvoiceReport as BaseAccountInvoiceReport,
)


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Marca",
        readonly=True,
    )

    # Conserva las dependencias estándar de Odoo 17 y añade Marca.
    _depends = dict(BaseAccountInvoiceReport._depends)
    _depends["product.template"] = list(
        BaseAccountInvoiceReport._depends.get("product.template", [])
    ) + ["brand_id"]

    @api.model
    def _select(self):
        return super()._select() + """
                , template.brand_id                                            AS brand_id
        """
