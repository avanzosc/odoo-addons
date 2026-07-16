# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    qty_to_invoice = fields.Float(
        string="To Invoice Qty",
        compute="_compute_qty_to_invoice",
        digits="Product Unit of Measure",
    )
    qty_invoiced = fields.Float(
        string="Billed Qty",
        compute="_compute_qty_invoiced",
        digits="Product Unit of Measure",
    )
    qty_to_receive = fields.Float(
        compute="_compute_qty_to_receive",
        digits="Product Unit of Measure",
    )
    qty_received = fields.Float(
        string="Received Qty",
        compute="_compute_qty_received",
        digits="Product Unit of Measure",
    )
    qty_received_manually = fields.Float(
        string="Manual Received Qty",
        compute="_compute_qty_received_manually",
        digits="Product Unit of Measure",
    )
    qty_ordered = fields.Float(
        string="Ordered Qty",
        compute="_compute_qty_ordered",
        digits="Product Unit of Measure",
    )
    untaxed_invoiced = fields.Monetary(
        compute="_compute_amount_invoiced",
        string="Untaxed Billed",
        store=True,
        copy=False,
        help="Taxes Excluded",
    )
    total_invoiced = fields.Monetary(
        compute="_compute_amount_invoiced",
        string="Total Billed",
        store=True,
        copy=False,
        help="Taxes Included",
    )
    untaxed_to_invoice = fields.Monetary(
        compute="_compute_amount_to_invoice",
        string="Untaxed To Bill",
        store=True,
        copy=False,
        help="Taxes Excluded",
    )
    total_to_invoice = fields.Monetary(
        compute="_compute_amount_to_invoice",
        string="Total To Bill",
        store=True,
        copy=False,
        help="Taxes Included",
    )
    untaxed_to_receive = fields.Monetary(
        compute="_compute_amount_to_receive",
        store=True,
        copy=False,
        help="Taxes Excluded",
    )
    total_to_receive = fields.Monetary(
        compute="_compute_amount_to_receive",
        store=True,
        copy=False,
        help="Taxes Included",
    )
    untaxed_received = fields.Monetary(
        compute="_compute_amount_received",
        store=True,
        copy=False,
        help="Taxes Excluded",
    )
    total_received = fields.Monetary(
        compute="_compute_amount_received",
        store=True,
        copy=False,
        help="Taxes Included",
    )
    untaxed_received_manually = fields.Monetary(
        compute="_compute_amount_received_manually", store=True, readonly=True
    )
    total_received_manually = fields.Monetary(
        compute="_compute_amount_received_manually", store=True, readonly=True
    )

    @api.depends("order_line", "order_line.qty_to_invoice")
    def _compute_qty_to_invoice(self):
        for purchase in self:
            purchase.qty_to_invoice = sum(purchase.order_line.mapped("qty_to_invoice"))

    @api.depends("order_line", "order_line.qty_invoiced")
    def _compute_qty_invoiced(self):
        for purchase in self:
            purchase.qty_invoiced = sum(purchase.order_line.mapped("qty_invoiced"))

    @api.depends("order_line", "order_line.qty_to_receive")
    def _compute_qty_to_receive(self):
        for purchase in self:
            purchase.qty_to_receive = sum(purchase.order_line.mapped("qty_to_receive"))

    @api.depends("order_line", "order_line.qty_received")
    def _compute_qty_received(self):
        for purchase in self:
            purchase.qty_received = sum(purchase.order_line.mapped("qty_received"))

    @api.depends("order_line", "order_line.qty_received_manual")
    def _compute_qty_received_manually(self):
        for purchase in self:
            purchase.qty_received_manually = sum(
                purchase.order_line.mapped("qty_received_manual")
            )

    @api.depends("order_line", "order_line.product_qty")
    def _compute_qty_ordered(self):
        for purchase in self:
            purchase.qty_ordered = sum(purchase.order_line.mapped("product_qty"))

    @api.depends(
        "order_line", "order_line.total_invoiced", "order_line.untaxed_invoiced"
    )
    def _compute_amount_invoiced(self):
        for purchase in self:
            purchase.total_invoiced = sum(purchase.order_line.mapped("total_invoiced"))
            purchase.untaxed_invoiced = sum(
                purchase.order_line.mapped("untaxed_invoiced")
            )

    @api.depends(
        "order_line", "order_line.total_to_invoice", "order_line.untaxed_to_invoice"
    )
    def _compute_amount_to_invoice(self):
        for purchase in self:
            purchase.total_to_invoice = sum(
                purchase.order_line.mapped("total_to_invoice")
            )
            purchase.untaxed_to_invoice = sum(
                purchase.order_line.mapped("untaxed_to_invoice")
            )

    @api.depends(
        "order_line", "order_line.total_to_receive", "order_line.untaxed_to_receive"
    )
    def _compute_amount_to_receive(self):
        for purchase in self:
            purchase.total_to_receive = sum(
                purchase.order_line.mapped("total_to_receive")
            )
            purchase.untaxed_to_receive = sum(
                purchase.order_line.mapped("untaxed_to_receive")
            )

    @api.depends(
        "order_line", "order_line.total_received", "order_line.untaxed_received"
    )
    def _compute_amount_received(self):
        for purchase in self:
            purchase.total_received = sum(purchase.order_line.mapped("total_received"))
            purchase.untaxed_received = sum(
                purchase.order_line.mapped("untaxed_received")
            )

    @api.depends(
        "order_line",
        "order_line.total_received_manually",
        "order_line.untaxed_received_manually",
    )
    def _compute_amount_received_manually(self):
        for purchase in self:
            purchase.total_received_manually = sum(
                purchase.order_line.mapped("total_received_manually")
            )
            purchase.untaxed_received_manually = sum(
                purchase.order_line.mapped("untaxed_received_manually")
            )
