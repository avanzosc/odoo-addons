# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, exceptions, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_logo_to_print(self):
        make_obj = self.env["product.make"]
        for invoice in self:
            makes = invoice.invoice_line_ids.filtered("make_id").mapped("make_id")
            if len(makes) == 1:
                make = makes[0]
                if make.logo:
                    invoice.logo_to_print = make.logo
                    invoice.three_address_in_invoice_report = (
                        make.three_address_in_invoice_report
                    )
                else:
                    search_default_logo = True
            else:
                search_default_logo = False
            if len(makes) == 2:
                makes2 = invoice.invoice_line_ids.filtered(
                    lambda z: z.make_id.common_logo
                ).mapped("make_id")
                if len(makes2) == 2:
                    invoice.logo_to_print = makes2[0].common_logo
                    invoice.three_address_in_invoice_report = True
                else:
                    search_default_logo = True
            if not makes or len(makes) > 3 or search_default_logo:
                make = make_obj.search([("use_logo", "=", True)], limit=1)
                company = self.env.user.company_id
                invoice.logo_to_print = make.logo if make else company.logo
                invoice.three_address_in_invoice_report = (
                    make.three_address_in_invoice_report if make else True
                )

    @api.depends(
        "partner_id",
        "partner_id.market_id",
        "partner_id.parent_id",
        "partner_id.parent_id.market_id",
    )
    def _compute_markek_id(self):
        for invoice in self:
            partner = invoice.partner_id
            parent = partner.parent_id if partner else None
            market = (partner.market_id if partner and partner.market_id else None) or (
                parent.market_id if parent and parent.market_id else None
            )
            invoice.market_id = market.id if market else False

    market_id = fields.Many2one(
        string="Market",
        comodel_name="res.partner.market",
        compute="_compute_markek_id",
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
    logo_to_print = fields.Binary("Image", compute="_compute_logo_to_print")
    three_address_in_sale_report = fields.Boolean(
        string="Show all three addresses in sales reports ",
        compute="_compute_logo_to_print",
    )
    city = fields.Char(string="City", related="partner_id.city", store=True)
    state_id = fields.Many2one(
        string="Province",
        comodel_name="res.country.state",
        related="partner_id.state_id",
        store=True,
    )
    shipping_city = fields.Char(
        string="Shipping city", related="partner_shipping_id.city", store=True
    )
    shipping_state_id = fields.Many2one(
        string="Shipping province",
        comodel_name="res.country.state",
        related="partner_shipping_id.state_id",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        invoices = super().create(vals_list)
        for invoice in invoices.filtered(lambda x: x.move_type == "out_invoice"):
            sales = invoice.invoice_line_ids.mapped("sale_line_ids.order_id")
            sales_with_team = sales.filtered(lambda s: s.team_id)
            if sales_with_team:
                invoice.team_id = sales_with_team[0].team_id.id
        return invoices

    def action_makes_in_lines(self):
        result = super().action_makes_in_lines()
        self.update_division_in_invoices()
        return result

    def update_division_in_invoices(self):
        for invoice in self:
            if invoice.move_type not in ("out_invoice", "out_refund"):
                invoice.team_id = False
            else:
                if invoice.invoice_line_ids:
                    missing_brand_lines = invoice.invoice_line_ids.filtered(
                        lambda x: not x.make_id
                        and x.display_type not in ("line_section", "line_note")
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
