# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    stock_move_line_ids = fields.One2many(
        string="Stock Move Lines",
        comodel_name="stock.move.line",
        compute="_compute_stock_move_line")

    def _compute_stock_move_line(self):
        for contact in self:
            move_lines = self.env["stock.move.line"].search([
                ("picking_partner_id", "=", contact.id)])
            if move_lines:
                contact.stock_move_line_ids = [(6, 0, move_lines.ids)]
            else:
                contact.stock_move_line_ids = False

    def action_view_move_lines(self):
        context = self.env.context.copy()
        context.update({
            "search_default_groupby_product_id": 2,
            "search_default_from": 1,
            "pivot_measures": ["in_qty", "out_qty", "dif_qty"]})
        return {
            'name': _("Stock Move Lines"),
            'view_mode': 'pivot,tree',
            'res_model': 'stock.move.line',
            'domain': [('id', 'in', self.stock_move_line_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
