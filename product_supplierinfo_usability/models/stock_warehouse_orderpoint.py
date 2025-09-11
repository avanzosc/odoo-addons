from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    supplier_pending_to_receive = fields.Float(
        string="Pending receipt from supplier",
        related="supplier_id.supplier_pending_to_receive",
    )
