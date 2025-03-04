# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from odoo.osv import expression


class StockLot(models.Model):
    _inherit = "stock.lot"

    def name_get(self):
        lots = super().name_get()
        for i, (lot_id, name) in enumerate(lots):
            lot = self.env["stock.lot"].browse(lot_id)
            if lot.ref:
                new_name = "%(name)s - %(ref)s" % {
                    "name": name,
                    "ref": lot.ref,
                }
                lots[i] = (lot_id, new_name)
        return lots

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        domain = ["|", ("name", operator, name), ("ref", operator, name)]
        domain = expression.AND([domain, args])
        return super()._name_search(
            name=name,
            args=domain,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
