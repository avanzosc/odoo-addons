# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.tools import format_date


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_picking_names(self):
        pickings_info = []
        for move in self:
            picking_name = move.picking_id.name
            picking_name = _("%(picking_name)s - %(move_date)s") % {
                "picking_name": picking_name,
                "move_date": format_date(
                    move.env,
                    move.date.date(),
                    lang_code=move.partner_id.lang or "es_ES",
                ),
            }
            pickings_info.append(picking_name)
        return ", ".join(sorted(set(pickings_info))) if pickings_info else ""
