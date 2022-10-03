# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


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
        for picking in self:
            in_ml = self.env["stock.move.line"].search([
                ("location_dest_id", "=", picking.location_id.id),
                ("state", "=", "done")])
            out_ml = self.env["stock.move.line"].search([
                ("location_id", "=", picking.location_id.id),
                ("state", "=", "done")])
            if not picking.custom_date_done:
                raise ValidationError(_("You must enter the date done."))
            products = []
            for line in in_ml:
                if line.product_id not in products:
                    products.append(line.product_id)
                    expire_lines = in_ml.filtered(
                        lambda c: c.product_id == line.product_id and (
                            c.expiration_date) and (
                                c.expiration_date.date()) <= (
                                    picking.custom_date_done.date()))
                    in_qty = sum(expire_lines.mapped("qty_done"))
                    out_qty = sum(out_ml.filtered(
                        lambda c: c.product_id == line.product_id).mapped(
                            "qty_done"))
                    dif = in_qty - out_qty
                    if dif > 0 and not (
                        picking.move_ids_without_package.filtered(
                            lambda c: (c.product_id == line.product_id))):
                        self.env["stock.move.line"].create(
                            {"product_id": line.product_id.id,
                             "location_id": picking.location_id.id,
                             "location_dest_id": picking.location_dest_id.id,
                             "product_uom_id": line.product_id.uom_id.id,
                             "qty_done": dif,
                             "picking_id": picking.id})
            picking.action_confirm()
