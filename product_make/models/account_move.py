# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, exceptions, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "invoice_line_ids", "invoice_line_ids.make_id", "invoice_line_ids.make_id.name"
    )
    def _compute_makes_on_invoice(self):
        for invoice in self:
            makes = ""
            for line in invoice.invoice_line_ids.filtered(lambda x: x.make_id):
                if line.make_id.name not in makes:
                    if not makes:
                        makes = line.make_id.name
                    else:
                        makes = "{}, {}".format(makes, line.make_id.name)
            invoice.makes_on_invoice = makes

    makes_on_invoice = fields.Char(
        string="Makes", compute="_compute_makes_on_invoice", store=True
    )
    team_id = fields.Many2one(
        string="Division",
        default=False,
        copy=False,
    )
    commercial_make_id = fields.Many2one(
        string="Commercial Make", comodel_name="product.make", copy=False
    )
    allowed_commercial_make_ids = fields.Many2many(
        string="Allowed Commercial Makes", comodel_name="product.make", copy=False
    )
    num_allowed_commercial_make = fields.Integer(string="Num Allowed Commercial Makes")
    relation_id = fields.Many2one(
        string="Relation",
        comodel_name="res.partner.relation",
        related="partner_id.relation_id",
        store=True,
    )
    classification_id = fields.Many2one(
        string="Classification",
        comodel_name="res.partner.classification",
        related="partner_id.classification_id",
        store=True,
    )
    market_id = fields.Many2one(
        string="Market",
        comodel_name="res.partner.market",
        compute="_compute_market_id",
        compute_sudo=True,
        store=True,
        copy=False,
        related=False,
    )
    market_sector_id = fields.Many2one(
        string="Market sector",
        comodel_name="res.partner.market.sector",
        related="partner_id.market_sector_id",
        store=True,
    )

    @api.depends(
        "partner_id",
        "partner_id.market_id",
        "partner_id.parent_id",
        "partner_id.parent_id.market_id",
    )
    def _compute_market_id(self):
        for invoice in self:
            partner = invoice.partner_id
            parent = partner.parent_id if partner else None
            market = (partner.market_id if partner and partner.market_id else None) or (
                parent.market_id if parent and parent.market_id else None
            )
            invoice.market_id = market.id if market else False

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if not self.partner_id:
            return result
        info = self.partner_id.get_partner_makes_info()
        self.commercial_make_id = info.get("commercial_make_id")
        self.allowed_commercial_make_ids = info.get("allowed_commercial_make_ids")
        self.num_allowed_commercial_make = info.get("num_allowed_commercial_make")
        return result

    def action_makes_in_lines(self):
        for invoice in self:
            lines = invoice.invoice_line_ids.filtered(lambda x: not x.make_id)
            for line in lines:
                line.put_makes_in_line()

    @api.model_create_multi
    def create(self, vals_list):
        invoices = super().create(vals_list)
        for invoice in invoices:
            if invoice.move_type in ("out_invoice", "out_refund"):
                sales = invoice.line_ids.mapped("sale_line_ids.order_id")
                for sale in sales:
                    if sale.commercial_make_id:
                        invoice.commercial_make_id = sale.commercial_make_id.id
                    if sale.num_allowed_commercial_make:
                        invoice.num_allowed_commercial_make = (
                            sale.num_allowed_commercial_make
                        )
                    if sale.allowed_commercial_make_ids:
                        invoice.allowed_commercial_make_ids = [
                            (6, 0, sale.allowed_commercial_make_ids.ids)
                        ]
            if invoice.move_type == "out_invoice":
                sales = invoice.invoice_line_ids.mapped("sale_line_ids.order_id")
                sales_with_team = sales.filtered(lambda s: s.team_id)
                if sales_with_team:
                    invoice.team_id = sales_with_team[0].team_id.id
        return invoices

    def update_division_in_invoices(self):
        for invoice in self:
            if invoice.move_type not in ("out_invoice", "out_refund"):
                invoice.team_id = False
            else:
                if invoice.invoice_line_ids:
                    missing_brand_lines = invoice.invoice_line_ids.filtered(
                        lambda x: not x.make_id and x.product_id
                    )
                    if missing_brand_lines:
                        raise exceptions.ValidationError(
                            _("Check invoice lines: some lines do not have a brand.")
                        )

                    make = invoice.invoice_line_ids.mapped("make_id")
                else:
                    make = False
                if invoice.market_id and make and len(make) == 1:
                    cond = [
                        ("market_id", "=", invoice.market_id.id),
                        ("product_make_id", "=", make.id),
                    ]
                    team = self.env["crm.team"].search(cond, limit=1)
                else:
                    team = False
                if invoice.team_id != team:
                    invoice.team_id = team.id if team else False
                invoice.review_account_in_lines()

    @api.onchange("team_id")
    def onchange_team_id(self):
        if not self.team_id:
            self.review_account_in_lines()
        else:
            self.with_context(division=self.team_id.id).review_account_in_lines()

    def review_account_in_lines(self):
        for invoice in self:
            for line in invoice.invoice_line_ids.filtered(lambda x: x.product_id):
                line_with_product = line
                if invoice.partner_id.lang:
                    line_with_product = line.with_context(lang=invoice.partner_id.lang)
                product = line_with_product.product_id
                if not invoice.team_id:
                    accounts = product.product_tmpl_id.get_product_accounts(
                        invoice.fiscal_position_id
                    )
                else:
                    accounts = product.product_tmpl_id._get_product_accounts()
                    if not invoice.fiscal_position_id:
                        fiscal_pos = self.env["account.fiscal.position"]
                    else:
                        fiscal_pos = invoice.fiscal_position_id
                    accounts = fiscal_pos.with_context(
                        division=invoice.team_id.id
                    ).map_accounts(accounts)
                accounts.update(
                    {
                        "stock_journal": product.product_tmpl_id.categ_id.property_stock_journal
                        or False
                    }
                )
                if invoice.move_type in ("out_invoice", "out_refund"):
                    line.account_id = accounts["income"].id
                else:
                    line.account_id = accounts["expense"].id
