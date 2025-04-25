# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def set_domain_for_partner_id(self):
        delivery_carrier = self.env["delivery.carrier"].search([(1, "=", 1)])
        partner_list = []
        for record in delivery_carrier:
            if record.partner_id:
                partner_list.append(record.partner_id.id)
        return [("id", "in", partner_list)]

    partner_id = fields.Many2one(
        string="Transporter",
        comodel_name="res.partner",
        domain=set_domain_for_partner_id,
    )
    number_of_packages = fields.Integer(
        string="Number of Packages", compute="_compute_number_of_packages"
    )
    packages_weight = fields.Float(
        compute="_compute_shipping_weight", store=True, copy=False
    )
    gross_weight_of_shipping = fields.Float(
        compute="_compute_shipping_weight", store=True, copy=False, readonly=False
    )

    def _compute_number_of_packages(self):
        for transfer in self:
            transfer.number_of_packages = sum(
                transfer.picking_ids.mapped("number_of_packages")
            )

    @api.depends(
        "move_line_ids",
        "move_line_ids.state",
        "move_line_ids.result_package_id",
        "move_line_ids.result_package_id.pack_weight",
        "move_line_ids.result_package_id.shipping_weight",
    )
    def _compute_shipping_weight(self):
        for batch in self:
            packages_weight = 0
            gross_weight_of_shipping = 0
            lines = batch.move_line_ids.filtered(
                lambda x: x.state != "cancel" and x.result_package_id
            )
            if lines:
                packages = list(set(lines.mapped("result_package_id")))
                if packages:
                    packages_weight = sum(
                        map(lambda package: package.pack_weight, packages)
                    )
                    gross_weight_of_shipping = sum(
                        map(lambda package: package.shipping_weight, packages)
                    )
            batch.packages_weight = packages_weight
            batch.gross_weight_of_shipping = gross_weight_of_shipping
