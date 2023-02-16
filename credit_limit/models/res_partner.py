from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    pending_to_paid = fields.Float(
        compute="_compute_pending_to_paid",
    )
    credit_limit = fields.Float()

    def _compute_pending_to_paid(self):
        for partner in self:
            invoices_pending_to_paid = self.env["account.move"].search(
                [
                    ("partner_id", "=", partner.id),
                    ("state", "=", "posted"),
                    ("payment_state", "!=", "paid"),
                ]
            )
            partner.pending_to_paid = sum(invoices_pending_to_paid.mapped("amount_residual"))
