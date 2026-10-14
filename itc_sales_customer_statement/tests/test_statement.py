from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged, new_test_user


@tagged("post_install", "-at_install")
class TestSalesCustomerStatement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.seller = new_test_user(
            cls.env, login="statement_seller",
            groups="base.group_user,itc_sales_customer_statement.group_statement_reader",
            company_id=cls.company.id,
            company_ids=[Command.set(cls.company.ids)],
        )
        cls.other_seller = new_test_user(
            cls.env, login="statement_other_seller",
            groups="base.group_user,itc_sales_customer_statement.group_statement_reader",
            company_id=cls.company.id,
            company_ids=[Command.set(cls.company.ids)],
        )
        cls.customer = cls.env["res.partner"].create({
            "name": "Assigned customer", "is_company": True, "user_id": cls.seller.id,
        })
        cls.other_customer = cls.env["res.partner"].create({"name": "Other customer"})
        cls.child = cls.env["res.partner"].create({
            "name": "Child contact", "parent_id": cls.customer.id,
        })
        cls.receivable = cls.env["account.account"].create({
            "name": "Statement receivable", "code": "STREC17",
            "account_type": "asset_receivable", "reconcile": True,
            "company_id": cls.company.id,
        })
        cls.income = cls.env["account.account"].create({
            "name": "Statement income", "code": "STINC17",
            "account_type": "income", "company_id": cls.company.id,
        })
        cls.journal = cls.env["account.journal"].create({
            "name": "Statement test", "code": "SCT17", "type": "general",
            "company_id": cls.company.id,
        })

    def _entry(self, partner, amount, posted=True):
        date = fields.Date.today() - timedelta(days=10)
        move = self.env["account.move"].create({
            "journal_id": self.journal.id, "company_id": self.company.id,
            "date": date,
            "line_ids": [Command.create({
                "name": "Customer open item", "partner_id": partner.id,
                "account_id": self.receivable.id, "date_maturity": date,
                "debit": max(amount, 0), "credit": max(-amount, 0),
            }), Command.create({
                "name": "Counterpart", "account_id": self.income.id,
                "debit": max(-amount, 0), "credit": max(amount, 0),
            })],
        })
        if posted:
            move.action_post()
        return move.line_ids.filtered(lambda line: line.account_id == self.receivable)

    def test_no_added_accounting_access(self):
        self.assertFalse(self.seller.has_group("account.group_account_invoice"))
        self.assertFalse(self.seller.has_group("account.group_account_readonly"))
        self.assertFalse(self.env["account.move"].with_user(self.seller)
                         .check_access_rights("read", raise_exception=False))
        outsider = new_test_user(
            self.env, login="statement_without_group", groups="base.group_user",
            company_id=self.company.id, company_ids=[Command.set(self.company.ids)],
        )
        self.customer.write({"user_id": outsider.id})
        with self.assertRaises(AccessError):
            self.customer.with_user(outsider)._sales_statement_data(self.company.id)

    def test_unassigned_and_other_seller_are_denied(self):
        with self.assertRaises(AccessError):
            self.other_customer.with_user(self.seller).action_itc_sales_customer_statement()
        with self.assertRaises(AccessError):
            self.customer.with_user(self.other_seller)._sales_statement_data(self.company.id)

    def test_unauthorized_company_and_revocation(self):
        other_company = self.env["res.company"].create({"name": "Statement other company"})
        with self.assertRaises(AccessError):
            self.customer.with_user(self.seller)._sales_statement_data(other_company.id)
        self.customer.write({"user_id": False})
        with self.assertRaises(AccessError):
            self.customer.with_user(self.seller)._sales_statement_data(self.company.id)

    def test_signed_open_items_partial_payment_children_and_drafts(self):
        invoice = self._entry(self.customer, 100)
        payment = self._entry(self.customer, -40)
        (invoice + payment).reconcile()
        self._entry(self.child, -25)
        self._entry(self.other_customer, 999)
        self._entry(self.customer, 888, posted=False)
        data = self.customer.with_user(self.seller)._sales_statement_data(self.company.id)
        self.assertEqual(len(data["rows"]), 2)
        self.assertAlmostEqual(data["total"], 35)
        self.assertAlmostEqual(data["overdue"], 60)
        child_data = self.child.with_user(self.seller)._sales_statement_data(self.company.id)
        self.assertEqual(child_data["customer"], data["customer"])
        self.assertAlmostEqual(child_data["total"], data["total"])

    def test_standard_contact_access_is_also_required(self):
        rule = self.env["ir.rule"].create({
            "name": "Test blocked customer", "model_id": self.env.ref("base.model_res_partner").id,
            "domain_force": "[('id', '!=', %s)]" % self.customer.id,
        })
        with self.assertRaises(AccessError):
            self.customer.with_user(self.seller).action_itc_sales_customer_statement()

    def test_new_children_are_included_automatically(self):
        self._entry(self.customer, 100)
        new_child = self.env["res.partner"].create({
            "name": "New child", "parent_id": self.customer.id,
        })
        self._entry(new_child, -25)
        data = self.customer.with_user(self.seller)._sales_statement_data(self.company.id)
        self.assertAlmostEqual(data["total"], 75)

    def test_reassignment_takes_effect_without_manual_authorizations(self):
        self.assertTrue(self.customer.with_user(self.seller).sales_statement_available)
        self.customer.write({"user_id": self.other_seller.id})
        self.assertFalse(self.customer.with_user(self.seller).sales_statement_available)
        self.assertTrue(self.customer.with_user(self.other_seller).sales_statement_available)
        with self.assertRaises(AccessError):
            self.customer.with_user(self.seller)._sales_statement_data(self.company.id)
        data = self.customer.with_user(self.other_seller)._sales_statement_data(self.company.id)
        self.assertEqual(data["customer"], self.customer.display_name)

    def test_legacy_assignment_does_not_grant_access(self):
        self.env["sales.statement.assignment"].create({
            "user_id": self.seller.id, "partner_id": self.other_customer.id,
            "company_id": self.company.id,
        })
        with self.assertRaises(AccessError):
            self.other_customer.with_user(self.seller)._sales_statement_data(self.company.id)
