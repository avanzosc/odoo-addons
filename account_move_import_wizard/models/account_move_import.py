# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import xlrd

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
from datetime import datetime

from odoo.addons.base_import_wizard.models.base_import import convert2str, check_number


class AccountMoveImport(models.Model):
    _name = "account.move.import"
    _inherit = "base.import"
    _description = "Wizard to import account moves"

    import_line_ids = fields.One2many(
        comodel_name="account.move.import.line",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.user.company_id.id,
        states={"done": [("readonly", True)]},
    )
    search_partner_by_ref = fields.Boolean(
        string="Search Partner Only By Ref",
        default=False,
        states={"done": [("readonly", True)]},
    )
    search_product_by_code = fields.Boolean(
        string="Search Product Only By Code",
        default=False,
        states={"done": [("readonly", True)]},
    )
    account_move_count = fields.Integer(
        string="# Account Moves",
        compute="_compute_account_move_count",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        states={"done": [("readonly", True)]},
    )

    def _compute_account_move_count(self):
        for record in self:
            record.account_move_count = len(
                record.mapped("import_line_ids.account_move_id")
            )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            partner_code = row_values.get("Partner Code", "")
            partner_name = row_values.get("Partner Name", "")
            account_move_ref = row_values.get("Ref", "")
            date = row_values.get("Date", "")
            if date:
                date = xlrd.xldate.xldate_as_datetime(
                    date, 0
                ).date()
            else:
                date = self.env["account.move.import"].default_date()
            period_date = row_values.get("Period Date", "")
            start = False
            stop = False
            if period_date:
                start, stop = period_date.split("-", 2)
                start = start.strip()
                start = datetime.strptime(start, '%d/%m/%Y').date()
                stop = stop.strip()
                stop = datetime.strptime(stop, '%d/%m/%Y').date()
            product_code = row_values.get("Product Code", "")
            product_name = row_values.get("Product Name", "")
            account_code = row_values.get("Account Code", "")
            account_name = row_values.get("Account Name", "")
            description = row_values.get("Description", "")
            quantity = row_values.get("Quantity", "")
            price_unit = row_values.get("Price Unit", "")
            log_info = ""
            values.update(
                {
                    "partner_code": convert2str(partner_code),
                    "partner_name": convert2str(partner_name),
                    "account_move_ref": convert2str(account_move_ref),
                    "date": date or False,
                    "start_date_period": start or False,
                    "end_date_period": stop or False,
                    "product_code": convert2str(product_code),
                    "product_name": convert2str(product_name),
                    "account_code": convert2str(account_code),
                    "account_name": convert2str(account_name),
                    "description": convert2str(description),
                    "quantity": check_number(quantity),
                    "price_unit": check_number(price_unit),
                    "log_info": log_info,
                }
            )
        return values

    def button_open_account_move(self):
        self.ensure_one()
        account_moves = self.mapped("import_line_ids.account_move_id")
        action = self.env.ref("account.action_invoice_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "=", account_moves.ids)],
                safe_eval(action.domain or "[]")
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict


class AccountMoveImportLine(models.Model):
    _name = "account.move.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import account moves"

    def default_date(self):
        default_dict = self.env["account.invoice"].default_get(["date"])
        return default_dict.get("date")

    import_id = fields.Many2one(
        comodel_name="account.move.import",
        copy=False,
    )
    action = fields.Selection(
        selection=[
            ("create", "Create"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        copy=False,
    )
    account_move_id = fields.Many2one(
        string="Account Move",
        comodel_name="account.invoice",
        copy=False,
    )
    account_move_ref = fields.Char(
        string="Account Move Ref",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_code = fields.Char(
        string="Partner Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_name = fields.Char(
        string="Partner Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=default_date,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    start_date_period = fields.Date(
        string="Start Date Period",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    end_date_period = fields.Date(
        string="End Date Period",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_code = fields.Char(
        string="Account Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_name = fields.Char(
        string="Account Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    description = fields.Text(
        string="Description",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    quantity = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    price_unit = fields.Float(
        string="Price Unit",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        product = account = False
        if self.account_move_ref:
            log_info_ref = self._check_account_move_ref()
            if log_info_ref:
                log_infos.append(log_info_ref)
        partner, log_info_partner = self._check_partner()
        if log_info_partner:
            log_infos.append(log_info_partner)
        if self.product_code or self.product_name:
            product, log_info_product = self._check_product()
            if log_info_product:
                log_infos.append(log_info_product)
        if self.account_code or self.account_name:
            account, log_info_account = self._check_account()
            if log_info_account:
                log_infos.append(log_info_account)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "account_id": account and account.id,
                "partner_id": partner and partner.id,
                "product_id": product and product.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        log_info = ""
        if self.action == "create" and self.state not in ("error", "done"):
            account_move = self.account_move_id
            if not account_move:
                account_move = self._create_account_move()
                account_move._onchange_partner_id()
                if self.account_move_ref:
                    same_ref_moves = self.import_id.import_line_ids.filtered(
                        lambda c: c.account_move_ref == self.account_move_ref
                    )
                else:
                    same_ref_moves = self.import_id.import_line_ids.filtered(
                        lambda c: c.partner_id == self.partner_id and (
                            c.date == self.date
                        )
                    )
                if same_ref_moves:
                    for line in same_ref_moves:
                        line.account_move_id = account_move.id
                    if not all(
                        [line.state == "pass" for line in same_ref_moves]
                    ):
                        log_info = _(
                            "There are lines with the same reference " +
                            "with errors."
                        )
            if self.account_move_id and not log_info:
                self._create_account_move_line()
            state = "error" if log_info else "done"
            update_values.update(
                {
                    "account_move_id": account_move and account_move.id,
                    "state": state,
                    "log_info": log_info,
                }
            )
        return update_values

    def _check_account(self):
        self.ensure_one()
        log_info = ""
        if self.account_id:
            return self.account_id, log_info
        account_obj = self.env["account.account"]
        search_domain = [("code", "=", self.account_code)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            account_obj = account_obj.with_context(force_company=self.import_id.company_id)
        accounts = account_obj.search(search_domain)
        if not accounts:
            accounts = False
            log_info = _("Error: No account found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("Error: More than one account found.")
        return accounts and accounts[:1], log_info

    def _check_account_move_ref(self):
        self.ensure_one()
        log_info = ""
        if self.account_move_ref:
            account_move_obj = self.env["account.invoice"]
            search_domain = [("name", "=", self.account_move_ref)]
            if self.import_id.company_id:
                search_domain = expression.AND(
                    [
                        [
                            "|",
                            ("company_id", "=", self.import_id.company_id.id),
                            ("company_id", "=", False),
                        ],
                        search_domain,
                    ]
                )
                account_move_obj = account_move_obj.with_context(force_company=self.import_id.company_id)
            same_ref = account_move_obj.search(search_domain)
            if same_ref:
                log_info = _(
                    "Error: There is another invoice with this reference."
                )
        return log_info

    def _check_partner(self):
        self.ensure_one()
        log_info = ""
        if self.partner_id:
            return self.partner_id, log_info
        partner_obj = self.env["res.partner"]
        search_domain = [("name", "=", self.partner_name)]
        if self.partner_code:
            search_domain = expression.AND(
                [
                    [
                        ("ref", "=", self.partner_code)
                    ],
                    search_domain
                ]
            )
            if self.import_id.search_partner_by_ref:
                search_domain = [("ref", "=", self.partner_code)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            partner_obj = partner_obj.with_context(force_company=self.import_id.company_id)
        partners = partner_obj.search(search_domain)
        if not partners:
            partners = False
            log_info = _("Error: No partner found.")
        elif len(partners) > 1:
            partners = False
            log_info = _("Error: More than one partner found.")
        return partners and partners[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        product_obj = self.env["product.product"]
        search_domain = [("name", "=ilike", self.product_name)]
        if self.product_code:
            search_domain = expression.AND(
                [
                    [
                        ("default_code", "=ilike", self.product_code)
                    ],
                    search_domain
                ]
            )
            if self.import_id.search_product_by_code:
                search_domain = [("default_code", "=ilike", self.product_code)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            product_obj = product_obj.with_context(force_company=self.import_id.company_id)
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            products = False
            log_info = _("Error: More than one product found.")
        return products and products[:1], log_info

    def _create_account_move_line(self):
        self.ensure_one()
        vals = self._account_move_line_vals()
        lines_before = self.account_move_id.invoice_line_ids
        self.account_move_id.invoice_line_ids = [(0, 0, vals)]
        lines_after = self.account_move_id.invoice_line_ids
        lines = lines_after - lines_before
        if lines:
            for line in lines:
                price = line.price_unit
                line._set_taxes()
                if price:
                    line.price_unit = price

    def _account_move_line_vals(self):
        self.ensure_one()
        account = self.account_id
        if not account:
            if self.product_id and self.product_id.property_account_income_id:
                account = self.product_id.property_account_income_id
            elif self.product_id and self.product_id.categ_id and (
                self.product_id.categ_id.property_account_income_categ_id
            ):
                account = (
                    self.product_id.categ_id.property_account_income_categ_id
                )
            else:
                account = self.import_id.journal_id.default_account_id
        quantity = self.quantity
        price_unit = self.price_unit
        if self.account_move_id and (
            self.account_move_id.type == "out_refund"
        ):
            if quantity < 0:
                quantity = -quantity
            else:
                price_unit = -price_unit
        vals = {
            "partner_id": self.partner_id and self.partner_id.id,
            "product_id": self.product_id and self.product_id.id,
            "product_uom_id": self.product_id.uom_id and (
                self.product_id.uom_id.id
            ),
            "name": self.description,
            "account_id": account and account.id,
            "quantity": quantity,
            "price_unit": price_unit,
        }
        print(vals)
        return vals

    def _account_move_vals(self):
        self.ensure_one()
        vals = {
            "partner_id": self.partner_id and self.partner_id.id,
            "type": "out_invoice",
            "name": self.account_move_ref,
            "date_invoice": self.date,
            "start_date_period": self.start_date_period,
            "end_date_period": self.end_date_period,
            "journal_id": self.import_id.journal_id and (
                self.import_id.journal_id.id
            ),
            "company_id": self.import_id.company_id and (
                self.import_id.company_id.id
            ),
        }
        return vals

    def _create_account_move(self):
        self.ensure_one()
        vals = self._account_move_vals()
        subtotal = 0
        lines = self.import_id.import_line_ids.filtered(
            lambda c: c.account_move_ref == self.account_move_ref
        )
        for line in lines:
            subtotal += line.quantity * line.price_unit
        if subtotal < 0:
            vals.update({
                "type": "out_refund",
            })
        account_move = self.env["account.invoice"].create(vals)
        return account_move
