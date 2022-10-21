# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from datetime import timedelta


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _default_get_custom_date_done(self):
        return fields.Datetime.now()

    expiration_operation = fields.Boolean(
        string="Is Expiration Operation",
        default=False,
        related="picking_type_id.expiration_operation",
        store=True)
    custom_date_done = fields.Datetime(
        default=_default_get_custom_date_done)

    def action_emptying_expired(self):
        expiration_products = self.env["product.product"].search(
            [("use_expiration_date", "=", True)])
        for picking in self:
            if not picking.custom_date_done:
                raise ValidationError(_("You must enter the date done."))
            for product in expiration_products:
                time = product.expiration_time
                date = picking.custom_date_done - timedelta(days=time)
                date = date.replace(hour=23, minute=59, second=59)
                date_stock = product.with_context(
                    to_date=date,
                    location=picking.location_id.id).qty_available
                out_ml = self.env["stock.move.line"].search([
                    ("product_id", "=", product.id),
                    ("location_id", "=", picking.location_id.id),
                    ("state", "=", "done")])
                out_ml = out_ml.filtered(
                    lambda l: date.date() < l.date.date() <= (
                        picking.custom_date_done.date()))
                out_qty = sum(out_ml.mapped("qty_done"))
                dif = date_stock - out_qty
                if float_compare(
                        dif, 0.0, precision_rounding=product.uom_id.rounding) > 0.0:
                    self.env["stock.move.line"].create(
                        {"product_id": product.id,
                         "location_id": picking.location_id.id,
                         "location_dest_id": picking.location_dest_id.id,
                         "product_uom_id": product.uom_id.id,
                         "qty_done": dif,
                         "picking_id": picking.id})
            picking.action_confirm()
