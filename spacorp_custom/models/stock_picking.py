# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _compute_text_delivery_vouchers(self):
        values = self.env["res.config.settings"].sudo().get_values()
        for picking in self:
            picking.text_delivery_vouchers = values.get("text_delivery_vouchers", " ")

    def _compute_print_make_sector(self):
        cond = [("print_make_on_out_picking", "=", True)]
        makes = self.env["product.make"].search(cond)
        for picking in self.filtered(lambda x: x.picking_type_id.code == "outgoing"):
            make_to_print = ""
            sector_to_print = ""
            for make in makes:
                if make.name in picking.makes_in_lines:
                    make_to_print = make.name
                    if (
                        make.market_to_print_ids
                        and picking.market_id in make.market_to_print_ids
                    ):
                        sector_to_print = picking.market_id.name
            if make_to_print:
                picking.make_to_print = make_to_print
            if sector_to_print:
                picking.sector_to_print = sector_to_print

    @api.depends(
        "move_line_ids_without_package",
        "move_line_ids_without_package.product_shipping_length",
    )
    def _compute_shipping_length(self):
        for picking in self:
            volume = 0.0
            for line in picking.move_line_ids_without_package:
                if line.product_shipping_length > volume:
                    volume = line.product_shipping_length
            picking.shipping_length = volume

    @api.depends(
        "partner_id",
        "partner_id.market_id",
        "partner_id.parent_id",
        "partner_id.parent_id.market_id",
    )
    def _compute_markek_id(self):
        for picking in self:
            market = False
            if picking.partner_id and picking.partner_id.market_id:
                market = picking.partner_id.market_id
            if picking.partner_id.parent_id and picking.partner_id.parent_id.market_id:
                market = picking.partner_id.parent_id.market_id
            picking.market_id = market.id if market else False

    text_delivery_vouchers = fields.Text(
        string="Text for delivery vouchers", compute="_compute_text_delivery_vouchers"
    )
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
    make_to_print = fields.Char(
        string="Make to print", compute="_compute_print_make_sector"
    )
    sector_to_print = fields.Char(
        string="Sector to print", compute="_compute_print_make_sector"
    )
    shipping_type_id = fields.Many2one(
        string="Shipping type", comodel_name="stock.picking.shipping.type"
    )
    shipping_length = fields.Float(
        string="Length", compute="_compute_shipping_length", store=True
    )
    contact_email_person_id = fields.Many2one(
        string="Contact email person", comodel_name="res.partner"
    )
    picking_type_code = fields.Selection(
        string="Type of Operation",
        related="picking_type_id.code",
        store=True,
        copy=False,
    )
    confirmation_email_sent = fields.Boolean(
        string="Confirmation email sent", default=False, copy=False
    )
    cost_of_transportation = fields.Monetary(
        string="Cost of transportation", copy=False, default=0.0, digits="Product Price"
    )
    weight = fields.Float(string="Net weight")
    gross_weight = fields.Float(string="Gross weight", default=0, copy=False)

    def action_makes_in_lines(self):
        result = super().action_makes_in_lines()
        self.update_division_in_pickings()
        return result

    def update_division_in_pickings(self):
        for picking in self:
            if picking.picking_type_code != "outgoing":
                picking.team_id = False
            else:
                if picking.move_ids_without_package:
                    lines_without_make = picking.move_ids_without_package.filtered(
                        lambda x: not x.make_id
                    )
                    if lines_without_make:
                        raise exceptions.ValidationError(
                            _("Check picking lines, some do not have a brand.")
                        )
                    make = picking.move_ids_without_package.mapped("make_id")
                    if picking.market_id and make and len(make) == 1:
                        cond = [
                            ("market_id", "=", picking.market_id.id),
                            ("product_make_id", "=", make.id),
                        ]
                        team = self.env["crm.team"].search(cond, limit=1)
                        if picking.team_id != team:
                            picking.team_id = team.id if team else False
