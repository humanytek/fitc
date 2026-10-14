from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools.misc import format_date, formatLang


class SalesCustomerStatementController(http.Controller):
    @http.route(
        "/itc-sales-customer-statement/<int:partner_id>", type="http",
        auth="user", methods=["GET"], website=False, sitemap=False,
    )
    def statement(self, partner_id, company_id=None, **kwargs):
        headers = [
            ("Cache-Control", "private, no-store, max-age=0"),
            ("Pragma", "no-cache"),
            ("X-Content-Type-Options", "nosniff"),
            ("X-Frame-Options", "SAMEORIGIN"),
        ]
        try:
            company_id = int(company_id or request.env.company.id)
            partner = request.env["res.partner"].browse(partner_id)
            if not partner.exists():
                raise AccessError("Cliente no autorizado.")
            data = partner._sales_statement_data(company_id)
        except (AccessError, MissingError, ValueError, TypeError):
            return request.make_response(
                "No tienes acceso a este estado de cuenta.",
                headers=headers + [("Content-Type", "text/plain; charset=utf-8")],
                status=403,
            )

        def money(amount, currency_id=None):
            currency = request.env["res.currency"].browse(
                currency_id or data["company_currency_id"])
            return formatLang(request.env, amount, currency_obj=currency)

        return request.render(
            "itc_sales_customer_statement.statement_page",
            {"data": data, "money": money,
             "date_text": lambda value: format_date(request.env, value)},
            headers=headers,
        )
