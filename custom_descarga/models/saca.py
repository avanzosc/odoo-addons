# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class Saca(models.Model):
    _inherit = "saca"

    historic_line_ids = fields.One2many(
        string="Historic Lines",
        comodel_name="saca.line",
        compute="_compute_historic_line_ids",
    )
    count_historic = fields.Integer(
        string="Count Historic", compute="_compute_count_historic"
    )

    def _compute_count_historic(self):
        for line in self:
            line.count_historic = len(line.historic_line_ids)

    def _compute_historic_line_ids(self):
        for saca in self:
            saca.historic_line_ids = False
            if saca.saca_line_ids:
                saca.historic_line_ids = (
                    self.env["saca.line"]
                    .search(
                        [
                            ("is_historic", "=", True),
                            ("historic_id", "in", saca.saca_line_ids.ids),
                        ]
                    )
                    .ids
                )

    def action_view_historic_lines(self):
        context = self.env.context.copy()
        return {
            "name": _("Historics"),
            "view_mode": "tree,form",
            "res_model": "saca.line",
            "domain": [
                ("id", "in", self.historic_line_ids.ids),
                ("is_historic", "=", True),
            ],
            "type": "ir.actions.act_window",
            "context": context,
        }
