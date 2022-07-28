# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
    )
    show_analytic_account = fields.Boolean(
        string="Show Analytic Account",
        compute="_compute_show_analytic_account",
    )

    @api.depends("picking_type_id", "picking_type_id.code")
    def _compute_show_analytic_account(self):
        for record in self:
            record.show_analytic_account = record.picking_type_id.code in (
                "outgoing",
                "incoming",
            )

    @api.onchange("analytic_account_id")
    def onchange_analytic_account_id(self):
        for picking in self.filtered(
            lambda x: x.analytic_account_id and x.analytic_account_id.partner_id
        ):
            picking.partner_id = picking.analytic_account_id.partner_id.id


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        moves = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        for move in moves.filtered(
            lambda x: x.picking_id
            and x.picking_id.analytic_account_id
            and x.picking_id.picking_type_code in ("outgoing", "incoming")
        ):
            vals = move._prepare_data_for_create_analytic_line()
            if vals:
                self.env["account.analytic.line"].create(vals)
        return moves

    def _prepare_data_for_create_analytic_line(self):
        self.ensure_one()
        product_qty = self.product_qty
        if self.picking_id.picking_type_code == "outgoing":
            product_qty = -1 * product_qty
        vals = {
            "stock_move_id": self.id,
            "account_id": self.picking_id.analytic_account_id.id,
            "group_id": self.picking_id.analytic_account_id.group_id.id,
            "partner_id": self.picking_id.partner_id.id,
            "product_id": self.product_id.id,
            "product_uom_id": self.product_uom.id,
            "unit_amount": product_qty,
            "amount": product_qty * self._get_price_unit(),
            "name": "{} {}".format(self.picking_id.name, self.name),
        }
        return vals
