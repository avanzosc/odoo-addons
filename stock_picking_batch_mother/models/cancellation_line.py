# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CancellationLine(models.Model):
    _name = "cancellation.line"
    _description = "Cancellation Line"

    batch_id = fields.Many2one(
        string="Mother",
        comodel_name="stock.picking.batch")
    week = fields.Integer(string="Week")
    date = fields.Date(string="Date")
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    lot_id = fields.Many2one(
        string="Lot/Serial Number",
        comodel_name="stock.production.lot")
    cancellation_qty = fields.Integer(
        string="Cancellations")
    inventory_qty = fields.Integer(
        string="Inventory")

    @api.onchange("cancellation_qty")
    def onchange_cancellation_qty(self):
        self.ensure_one()
        self = self.sudo()
        if self.cancellation_qty:
            quant = self.batch_id.location_id.quant_ids.filtered(
                lambda x: x.product_id == self.product_id and (
                    x.lot_id == self.lot_id))
            if not quant:
                raise ValidationError(
                    _("No stock line has been found for that product and lot.")
                    )
            quant[0].quantity = (
                quant[0].quantity - self.cancellation_qty)
