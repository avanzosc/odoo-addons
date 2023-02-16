# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _gather(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
    ):
        force_lots = self.env.context.get("force_lots", None)
        records = self
        if not force_lots:
            records = super()._gather(
                product_id,
                location_id,
                lot_id=lot_id,
                package_id=package_id,
                owner_id=owner_id,
                strict=strict,
            )
        else:
            if lot_id:
                force_lots |= lot_id
            for force_lot in force_lots:
                records |= super()._gather(
                    product_id,
                    location_id,
                    lot_id=force_lot,
                    package_id=package_id,
                    owner_id=owner_id,
                    strict=strict,
                )
        return records
