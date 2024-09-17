# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RepairOrder(models.Model):
    _inherit = "repair.order"

    lot_expiration_date = fields.Date(
        string="Lot warranty date",
        copy=False,
        store=True,
        related="lot_id.expiration_date_without_hour",
    )
    lot_warranty_repair_date = fields.Date(
        string="Lot warranty repair date",
        copy=False,
        store=True,
        related="lot_id.warranty_repair_date",
    )

    @api.onchange("lot_expiration_date", "lot_warranty_repair_date")
    def onchange_expiration_warranty_repair_date(self):
        self._calculate_guarantee_limit()
        self._check_if_it_is_under_warranty()

    @api.onchange("guarantee_limit")
    def onchange_guarantee_limit(self):
        if self.guarantee_limit:
            if self.guarantee_limit < fields.Date.context_today(self):
                self.invoice_method = "b4repair"
            else:
                self.invoice_method = "none"

    def action_repair_end(self):
        result = super().action_repair_end()
        for repair in self.filtered(lambda x: x.lot_id):
            repair.lot_id.warranty_repair_date = fields.Datetime.now() + relativedelta(
                months=repair.lot_id.product_id.repair_warranty_period
            )
        return result

    @api.model
    def create(self, vals):
        repair = super().create(vals)
        repair._calculate_guarantee_limit()
        repair._check_if_it_is_under_warranty()
        return repair

    def _check_if_it_is_under_warranty(self):
        in_warranty = False
        if (
            self.lot_id.expiration_date_without_hour
            and fields.Date.context_today(self)
            < self.lot_id.expiration_date_without_hour
        ):
            in_warranty = True
        if (
            self.lot_id.warranty_repair_date
            and fields.Date.context_today(self) < self.lot_id.warranty_repair_date
        ):
            in_warranty = True
        if in_warranty and self.invoice_method != "none":
            self.invoice_method = "none"

    def _calculate_guarantee_limit(self):
        guarantee_limit = False
        if self.lot_expiration_date:
            guarantee_limit = self.lot_expiration_date
        if self.lot_warranty_repair_date and (
            not guarantee_limit
            or (self.lot_warranty_repair_date > self.lot_expiration_date)
        ):
            guarantee_limit = self.lot_warranty_repair_date
        self.guarantee_limit = guarantee_limit
        if guarantee_limit:
            if guarantee_limit < fields.Date.context_today(self):
                self.invoice_method = "b4repair"
            else:
                self.invoice_method = "none"

    def action_validate(self):
        self.ensure_one()
        if self.sale_order_id and self.sale_order_id.state == "draft":
            raise UserError(
                _("You must confirm the sales order before starting the " "repair.")
            )
        return super(RepairOrder, self).action_validate()
