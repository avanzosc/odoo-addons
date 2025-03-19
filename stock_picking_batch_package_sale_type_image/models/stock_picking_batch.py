# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    sale_order_type_id = fields.Many2one(
        string="Sale Order type",
        comodel_name="sale.order.type",
        compute="_compute_sale_order_type_id",
        store=True,
        copy=False,
    )

    @api.depends(
        "picking_ids",
        "picking_ids.group_id",
        "picking_ids.group_id.sale_id",
        "picking_ids.group_id.sale_id.type_id",
        "picking_ids.group_id.sale_id.type_id.sale_type_image",
    )
    def _compute_sale_order_type_id(self):
        for batch in self:
            pickings = batch.picking_ids.filtered(
                lambda x: x.group_id
                and x.group_id.sale_id
                and x.group_id.sale_id.type_id
                and x.group_id.sale_id.type_id.sale_type_image
            )
            sale_types = pickings.mapped(lambda x: x.group_id.sale_id.type_id)
            distinct_sale_types = list(set(sale_types))
            if len(distinct_sale_types) == 1:
                batch.sale_order_type_id = distinct_sale_types[0].id
            else:
                batch.sale_order_type_id = False
