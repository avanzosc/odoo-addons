# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    user_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )
    makes_in_lines = fields.Char(
        string="Makes", compute="_compute_makes_in_lines", store=True
    )
    team_id = fields.Many2one(
        string="Division",
        comodel_name="crm.team",
        copy=False,
    )
    commercial_make_id = fields.Many2one(
        string="Commercial Make", comodel_name="product.make", copy=False
    )
    allowed_commercial_make_ids = fields.Many2many(
        string="Allowed Commercial Makes", comodel_name="product.make", copy=False
    )
    num_allowed_commercial_make = fields.Integer(string="Num Allowed Commercial Makes")
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
        for picking in self:
            market = False
            if picking.partner_id and picking.partner_id.market_id:
                market = picking.partner_id.market_id
            if picking.partner_id.parent_id and picking.partner_id.parent_id.market_id:
                market = picking.partner_id.parent_id.market_id
            picking.market_id = market.id if market else False

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        # result = super().onchange_partner_id()
        if not self.partner_id:
            self.commercial_make_id = False
            self.allowed_commercial_make_ids = [(5, 0, 0)]
            self.num_allowed_commercial_make = 0
            return
        info = self.partner_id.get_partner_makes_info()
        self.commercial_make_id = info.get("commercial_make_id")
        self.allowed_commercial_make_ids = info.get("allowed_commercial_make_ids")
        self.num_allowed_commercial_make = info.get("num_allowed_commercial_make")
        # return result

    @api.depends(
        "move_ids_without_package",
        "move_ids_without_package.make_id",
        "move_ids_without_package.make_id.name",
    )
    def _compute_makes_in_lines(self):
        for picking in self:
            makes = ""
            for line in picking.move_ids_without_package.filtered(lambda x: x.make_id):
                if line.make_id.name not in makes:
                    if not makes:
                        makes = line.make_id.name
                    else:
                        makes = f"{makes}, {line.make_id.name}"
            picking.makes_in_lines = makes

    def action_makes_in_lines(self):
        for picking in self:
            lines = picking.move_ids_without_package.filtered(lambda x: not x.make_id)
            for line in lines:
                line.put_makes_in_line()

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
                        raise ValidationError(
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
