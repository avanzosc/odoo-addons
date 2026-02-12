# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    sale_count = fields.Integer(
        compute="_compute_sale_count",
        string="# of Sale Orders",
    )
    picking_count = fields.Integer(
        compute="_compute_picking_count",
        string="# of Transfers",
    )
    sale_type_id = fields.Many2one(
        string="Sales Order Type",
        comodel_name="sale.order.type",
    )
    sale_tmpl_id = fields.Many2one(
        string="Quotation Template",
        comodel_name="sale.order.template",
    )

    def _compute_sale_count(self):
        order_obj = self.env["sale.order"]
        sale_res = order_obj.read_group(
            [("agreement_id", "in", self.ids)],
            ["agreement_id"],
            ["agreement_id"],
        )
        sale_data = {x["agreement_id"][0]: x["agreement_id_count"] for x in sale_res}
        for agreement in self:
            agreement.sale_count = sale_data.get(agreement.id, 0)

    def _compute_picking_count(self):
        picking_obj = self.env["stock.picking"]
        picking_res = picking_obj.read_group(
            [("agreement_id", "in", self.ids)],
            ["agreement_id"],
            ["agreement_id"],
        )
        picking_data = {
            x["agreement_id"][0]: x["agreement_id_count"] for x in picking_res
        }
        for agreement in self:
            agreement.picking_count = picking_data.get(agreement.id, 0)
