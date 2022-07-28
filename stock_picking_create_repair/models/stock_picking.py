# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_repair = fields.Boolean(
        string="It's repair", default=False, copy=False)
    created_respair_ids = fields.One2many(
        string="Created repairs", comodel_name="repair.order",
        inverse_name="created_from_picking_id", copy=False)
    repairs_count = fields.Integer(
        string="# Repairs", compute="_compute_repairs_count", store=True,
        copy=False)
    sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=False)

    @api.depends("created_respair_ids")
    def _compute_repairs_count(self):
        for picking in self:
            picking.repairs_count = len(picking.created_respair_ids)

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        pickings = self.filtered(lambda x: x.state == 'done')
        if pickings:
            pickings.create_repairs_from_picking()
        return result

    def create_repairs_from_picking(self):
        for picking in self.filtered(
                lambda x: x.picking_type_code == 'incoming' and x.is_repair):
            for line in picking.move_line_ids_without_package.filtered(
                    lambda x: x.qty_done > 0 and not x.created_repair_id):
                vals = line.catch_values_from_create_repair_from_picking()
                repair = self.env['repair.order'].create(vals)
                line.created_repair_id = repair.id

    def action_repairs_from_picking(self):
        self.ensure_one()
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.created_respair_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict
