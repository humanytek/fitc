from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Marca de Producto"
    _order = "sequence, name"

    name = fields.Char(string="Marca", required=True, index=True)
    code = fields.Char(string="Código", index=True)
    active = fields.Boolean(string="Activa", default=True)
    sequence = fields.Integer(string="Secuencia", default=10)

    _sql_constraints = [
        ("product_brand_name_uniq", "unique(name)", "Ya existe una marca con ese nombre."),
        ("product_brand_code_uniq", "unique(code)", "Ya existe una marca con ese código."),
    ]

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and not record.name.strip():
                raise ValidationError("El nombre de la marca no puede estar vacío.")
