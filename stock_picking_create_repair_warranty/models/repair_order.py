# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from dateutil.relativedelta import relativedelta


class RepairOrder(models.Model):
    _inherit = "repair.order"

    lot_expiration_date = fields.Date(
        string="Lot warranty date", copy=False, store=True,
        related="lot_id.expiration_date_without_hour")
    lot_warranty_repair_date = fields.Date(
        string="Lot warranty repair date", copy=False, store=True,
        related="lot_id.warranty_repair_date")

    def action_repair_end(self):
        result = super(RepairOrder, self).action_repair_end()
        for repair in self.filtered(
            lambda x: x.lot_id and x.sale_line_id and
            x.sale_line_id.product_id.is_repair and
            x.sale_line_id.product_to_repair_id and
            x.sale_line_id.product_to_repair_id.tracking ==
                "serial"):
            repair.lot_id.warranty_repair_date = (
                fields.Datetime.now() + relativedelta(
                    months=repair.lot_id.product_id.repair_warranty_period))
        return result
