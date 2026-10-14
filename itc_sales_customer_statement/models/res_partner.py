from urllib.parse import urlencode

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


READER_GROUP = "itc_sales_customer_statement.group_statement_reader"


class ResPartner(models.Model):
    _inherit = "res.partner"

    sales_statement_available = fields.Boolean(
        compute="_compute_sales_statement_available", compute_sudo=False,
        string="Puede consultar estado de cuenta",
    )

    @api.depends("commercial_partner_id", "commercial_partner_id.user_id", "commercial_partner_id.company_id")
    @api.depends_context("uid", "company")
    def _compute_sales_statement_available(self):
        reader = self.env.user.has_group(READER_GROUP)
        for partner in self:
            commercial = partner.commercial_partner_id
            partner.sales_statement_available = bool(
                reader and commercial.user_id.id == self.env.uid
                and (not commercial.company_id or commercial.company_id == self.env.company)
            )

    def _sales_statement_authorize(self, company_id):
        self.ensure_one()
        if not self.env.user.has_group(READER_GROUP):
            raise AccessError(_("No tienes permiso para consultar estados de cuenta."))
        self.check_access_rights("read")
        self.check_access_rule("read")
        partner = self.commercial_partner_id
        partner.check_access_rights("read")
        partner.check_access_rule("read")
        company = self.env["res.company"].browse(company_id).exists()
        if not company or company not in self.env.user.company_ids:
            raise AccessError(_("Empresa no autorizada."))
        if partner.company_id and partner.company_id != company:
            raise AccessError(_("El cliente pertenece a otra empresa."))
        if partner.user_id.id != self.env.uid:
            raise AccessError(_("Este cliente no está asignado a tu usuario como vendedor."))
        return partner, company

    def action_itc_sales_customer_statement(self):
        self.ensure_one()
        partner, company = self._sales_statement_authorize(self.env.company.id)
        return {
            "type": "ir.actions.act_url",
            "url": "/itc-sales-customer-statement/%s?%s" % (
                partner.id, urlencode({"company_id": company.id})),
            "target": "new",
        }

    def _sales_statement_data(self, company_id):
        """Private method: return only approved scalar data, never account records."""
        partner, company = self._sales_statement_authorize(company_id)
        today = fields.Date.context_today(self)
        # Narrow sudo is necessary because no accounting ACL is granted to readers.
        # The authorization above runs as the real user before this query.
        lines = self.env["account.move.line"].sudo().search([
            ("company_id", "=", company.id),
            ("partner_id.commercial_partner_id", "=", partner.id),
            ("account_id.account_type", "=", "asset_receivable"),
            ("parent_state", "=", "posted"),
            ("reconciled", "=", False),
        ], order="date_maturity, date, id")
        rows = []
        total = overdue = 0.0
        for line in lines:
            currency = line.currency_id or company.currency_id
            if (company.currency_id.is_zero(line.amount_residual)
                    and currency.is_zero(line.amount_residual_currency)):
                continue
            due = line.date_maturity or line.date
            late = line.amount_residual > 0 and due < today
            kind = {
                "out_invoice": _("Factura"),
                "out_refund": _("Nota de crédito"),
            }.get(line.move_id.move_type, _("Otro movimiento de cartera"))
            if line.payment_id or line.statement_line_id:
                kind = _("Pago / anticipo")
            rows.append({
                "date": line.invoice_date or line.date,
                "reference": line.move_name,
                "kind": kind,
                "origin": line.move_id.invoice_origin if line.move_id.is_invoice() else "",
                "due": due,
                "days": (today - due).days if late else 0,
                "currency": currency.name,
                "original": line.balance,
                "residual": line.amount_residual,
                "residual_document": line.amount_residual_currency,
                "currency_id": currency.id,
                "overdue": late,
            })
            total += line.amount_residual
            if late:
                overdue += line.amount_residual
        return {
            "customer": partner.display_name,
            "company": company.name,
            "company_currency_id": company.currency_id.id,
            "company_currency": company.currency_id.name,
            "today": today,
            "rows": rows,
            "total": total,
            "overdue": overdue,
        }
