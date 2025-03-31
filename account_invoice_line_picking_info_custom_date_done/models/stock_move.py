# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.tools import format_date


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_picking_names(self):
        picking_names = super()._get_picking_names()
        pickings = list(set(self.mapped("picking_id")))
        picking_info = []
        for picking in pickings:
            picking_names = picking.name
            if picking.custom_date_done:
                picking_names = _("%(picking_name)s - Date: %(picking_date)s") % {
                    "picking_name": picking_names,
                    "picking_date": format_date(
                        self.env,
                        picking.custom_date_done.date(),
                        lang_code=picking.partner_id.lang or "es_ES",
                    ),
                }
            picking_info.append(picking_names)
        return ", ".join(sorted(set(picking_info))) if picking_info else ""
