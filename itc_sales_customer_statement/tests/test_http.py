from odoo import Command
from odoo.tests import HttpCase, tagged, new_test_user


@tagged("post_install", "-at_install")
class TestSalesStatementHttp(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.viewer = new_test_user(
            cls.env, login="statement_http_viewer", password="statement-test-password",
            groups="base.group_user,itc_sales_customer_statement.group_statement_reader",
            company_id=cls.env.company.id,
            company_ids=[Command.set(cls.env.company.ids)],
        )
        cls.customer = cls.env["res.partner"].create({
            "name": "Statement <script>unsafe</script>", "user_id": cls.viewer.id,
        })
        cls.other = cls.env["res.partner"].create({"name": "HTTP forbidden customer"})

    def test_http_authorization_rendering_and_revocation(self):
        self.authenticate(self.viewer.login, "statement-test-password")
        path = "/itc-sales-customer-statement/%s?company_id=%s"
        response = self.url_open(path % (self.customer.id, self.env.company.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn("No hay partidas pendientes", response.text)
        self.assertIn("&lt;script&gt;unsafe&lt;/script&gt;", response.text)
        self.assertNotIn("<script>unsafe</script>", response.text)
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))
        response = self.url_open(path % (self.other.id, self.env.company.id))
        self.assertEqual(response.status_code, 403)
        response = self.url_open("/itc-sales-customer-statement/%s?company_id=invalid" % self.customer.id)
        self.assertEqual(response.status_code, 403)
        self.customer.write({"user_id": False})
        response = self.url_open(path % (self.customer.id, self.env.company.id))
        self.assertEqual(response.status_code, 403)
