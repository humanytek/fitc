from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError


class SalesStatementAssignment(models.Model):
    _name = "sales.statement.assignment"
    _description = "Cliente autorizado para consulta comercial"
    _rec_name = "partner_id"
    _order = "user_id, partner_id, company_id"
    _check_company_auto = True

    user_id = fields.Many2one(
        "res.users", string="Vendedor", required=True, ondelete="cascade",
        domain=[("share", "=", False)],
    )
    partner_id = fields.Many2one(
        "res.partner", string="Cliente (empresa principal)", required=True,
        ondelete="cascade", check_company=True,
    )
    company_id = fields.Many2one(
        "res.company", string="Empresa", required=True,
        default=lambda self: self.env.company, ondelete="cascade",
    )
    contact_ids = fields.Many2many(
        "res.partner", "sales_statement_assignment_partner_rel",
        "assignment_id", "partner_id", string="Contactos contables autorizados",
        help="Lista fija de contactos hijos incluidos. Solo un administrador puede ampliarla.",
    )

    _sql_constraints = [
        ("assignment_unique", "unique(user_id, partner_id, company_id)",
         "Este cliente ya está autorizado para este vendedor y empresa."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        # Snapshot descendant IDs rather than treating editable contact hierarchy as authority.
        for vals in vals_list:
            if "contact_ids" not in vals and vals.get("partner_id"):
                children = self.env["res.partner"].with_context(active_test=False).search([
                    ("commercial_partner_id", "=", vals["partner_id"]),
                    ("id", "!=", vals["partner_id"]),
                ])
                vals["contact_ids"] = [(6, 0, children.ids)]
        return super().create(vals_list)

    def action_refresh_contacts(self):
        if not self.env.user.has_group("itc_sales_customer_statement.group_statement_manager"):
            raise AccessError(_("Solo un administrador de cartera puede actualizar contactos."))
        self.check_access_rights("write")
        self.check_access_rule("write")
        for rec in self:
            children = self.env["res.partner"].with_context(active_test=False).search([
                ("commercial_partner_id", "=", rec.partner_id.id),
                ("id", "!=", rec.partner_id.id),
            ])
            rec.contact_ids = [(6, 0, children.ids)]
        return True

    @api.constrains("partner_id", "contact_ids", "user_id", "company_id")
    def _check_assignment(self):
        for rec in self:
            if rec.partner_id != rec.partner_id.commercial_partner_id:
                raise ValidationError(_("Selecciona la empresa principal, no un contacto hijo."))
            if rec.user_id.share or rec.company_id not in rec.user_id.company_ids:
                raise ValidationError(_("El vendedor debe ser interno y tener acceso a esta empresa."))
            if any(contact.commercial_partner_id != rec.partner_id for contact in rec.contact_ids):
                raise ValidationError(_("Los contactos autorizados deben pertenecer a este cliente."))
            if any(contact.company_id and contact.company_id != rec.company_id
                   for contact in rec.contact_ids):
                raise ValidationError(_("Los contactos autorizados deben corresponder a la empresa."))
