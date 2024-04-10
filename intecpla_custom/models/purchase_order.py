# Copyright 2023 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        if args:
            my_args = str(args)
            if "name" in my_args and len(args) == 1:
                to_find = str(args[0][2])
                args = [
                    "|",
                    ["name", "ilike", to_find],
                    ["partner_ref", "ilike", to_find],
                ]
        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
