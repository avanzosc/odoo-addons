# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _catch_picking_info_section(self):
        picking_name = super()._catch_picking_info_section()
        if self.custom_date_done:
            picking_name = _("%(picking_name)s, Date: %(date)s") % {
                "picking_name": picking_name,
                "date": self.custom_date_done.date(),
            }
        return picking_name
