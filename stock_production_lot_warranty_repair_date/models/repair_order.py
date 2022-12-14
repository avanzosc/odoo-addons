# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class RepairOrder(models.Model):
    _inherit = "repair.order"

    lot_expiration_date = fields.Date(
        string="Lot warranty date", copy=False, store=True,
        related="lot_id.expiration_date_without_hour")
    lot_warranty_repair_date = fields.Date(
        string="Lot warranty repair date", copy=False, store=True,
        related="lot_id.warranty_repair_date")

    @api.onchange("lot_expiration_date", "lot_warranty_repair_date")
    def onchange_expiration_warranty_repair_date(self):
        self._check_if_it_is_under_warranty()

    def action_repair_end(self):
        result = super(RepairOrder, self).action_repair_end()
        for repair in self.filtered(lambda x: x.lot_id):
            repair.lot_id.warranty_repair_date = (
                fields.Datetime.now() + relativedelta(
                    months=repair.lot_id.product_id.repair_warranty_period))
        return result

    @api.model
    def create(self, vals):
        repair = super(RepairOrder, self).create(vals)
        repair._check_if_it_is_under_warranty()
        return repair

    def _check_if_it_is_under_warranty(self):
        in_warranty = False
        if (self.lot_id.expiration_date_without_hour and
            fields.Date.context_today(self) <
                self.lot_id.expiration_date_without_hour):
            in_warranty = True
        if (self.lot_id.warranty_repair_date and
            fields.Date.context_today(self) <
                self.lot_id.warranty_repair_date):
            in_warranty = True
        if in_warranty and self.invoice_method != "none":
            self.invoice_method = "none"
