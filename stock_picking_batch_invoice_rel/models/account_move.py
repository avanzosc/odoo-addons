# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    stock_picking_batch_ids = fields.Many2many(
        string="Batch Transfers",
        comodel_name="stock.picking.batch",
        relation="rel_picking_batch_invoice",
        column1="invoice_id",
        column2="picking_batch_id",
    )
    stock_picking_batch_count = fields.Integer(
        string="Batch Transfers Counter", compute="_compute_stock_picking_batch_count"
    )

    def _compute_stock_picking_batch_count(self):
        for invoice in self:
            invoice.stock_picking_batch_count = len(invoice.stock_picking_batch_ids)

    def action_view_picking_batch(self):
        self.ensure_one()
        action = {
            "name": _("Batch Transfers"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "stock.picking.batch",
        }
        action.update(
            {
                "name": _("Batch Transfers"),
                "view_mode": "tree,kanban,form",
                "domain": [("id", "in", self.stock_picking_batch_ids.ids)],
            }
        )
        return action
