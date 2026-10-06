from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Marca",
        index=True,
        ondelete="restrict",
        help="Marca comercial del producto. Se utiliza como dimensión en análisis y dashboards.",
    )
