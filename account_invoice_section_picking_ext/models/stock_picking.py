# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_invoice_section_name(self):
        super()._get_invoice_section_name()
        pickings_names = ""
        for picking in self:
            picking_name = picking._catch_picking_info_section()
            if not pickings_names:
                pickings_names = picking_name
            else:
                pickings_names = "%(pickings_names)s \n%(picking_name)s" % {
                    "pickings_names": pickings_names,
                    "picking_name": picking_name,
                }
        return pickings_names

    def _catch_picking_info_section(self):
        picking_name = _("Picking: %(picking)s") % {
            "picking": self.name,
        }
        if self.origin:
            picking_name = _("Order: %(origin)s, %(picking_name)s") % {
                "origin": self.origin,
                "picking_name": picking_name,
            }
        return picking_name
