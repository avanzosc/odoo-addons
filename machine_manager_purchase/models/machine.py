# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import pytz

from odoo import api, fields, models


class Machine(models.Model):
    _inherit = "machine"

    move_line_id = fields.Many2one(
        string="Stock Move Line", comodel_name="stock.move.line", copy=False
    )
    purchase_id = fields.Many2one(
        string="Purchase Order",
        comodel_name="purchase.order",
        compute="_compute_purchase_info",
        store=True,
        copy=False,
    )
    purch_date = fields.Date(
        string="Purchase Date",
        help="Machine's date of purchase",
        compute="_compute_purchase_info",
        store=True,
        copy=False,
    )
    purch_cost = fields.Float(
        string="Purchase Value",
        digits=(16, 2),
        default=0.0,
        compute="_compute_purchase_info",
        store=True,
        copy=False,
    )
    purch_partner_id = fields.Many2one(
        string="Purchased From",
        comodel_name="res.partner",
        compute="_compute_purchase_info",
        store=True,
        copy=False,
    )
    in_picking_id = fields.Many2one(
        string="In Picking",
        comodel_name="stock.picking",
        compute="_compute_purchase_info",
        store=True,
        copy=False,
    )

    @api.depends(
        "move_line_id",
        "move_line_id.move_id",
        "move_line_id.move_id.purchase_line_id",
        "move_line_id.move_id.purchase_line_id.order_id",
        "move_line_id.move_id.purchase_line_id.order_id.date_approve",
        "move_line_id.move_id.purchase_line_id.price_subtotal",
        "move_line_id.move_id.purchase_line_id.order_id.partner_id",
    )
    def _compute_purchase_info(self):
        for machine in self:
            purchase_id = False
            purch_date = False
            purch_partner_id = False
            in_picking_id = False
            purch_cost = 0
            pline = machine.move_line_id.move_id.purchase_line_id
            if pline.order_id:
                purchase_id = pline.order_id.id
            if pline.order_id.date_approve:
                user_tz = self.env.user.tz or self.env.context.get("tz")
                user_pytz = pytz.timezone(user_tz) if user_tz else pytz.utc
                purch_date = (
                    pline.order_id.date_approve.now()
                    .astimezone(user_pytz)
                    .replace(tzinfo=None)
                    .date()
                )
            if pline.price_subtotal:
                purch_cost = pline.price_subtotal
            if pline.order_id.partner_id:
                purch_partner_id = pline.order_id.partner_id.id
            if machine.move_line_id.move_id.picking_id:
                in_picking_id = machine.move_line_id.move_id.picking_id.id
            machine.purchase_id = purchase_id
            machine.purch_date = purch_date
            machine.purch_cost = purch_cost
            machine.purch_partner_id = purch_partner_id
            machine.in_picking_id = in_picking_id
