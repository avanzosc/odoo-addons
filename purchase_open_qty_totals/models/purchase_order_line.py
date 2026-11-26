# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

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

    @api.depends("qty_invoiced", "price_unit", "taxes_id")
    def _compute_amount_invoiced(self):
        for line in self:
            taxes = line.taxes_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.qty_invoiced,
                line.product_id,
                line.order_id.partner_id,
            )
            line.update(
                {
                    "total_invoiced": taxes["total_included"],
                    "untaxed_invoiced": taxes["total_excluded"],
                }
            )

    @api.depends("qty_to_invoice", "price_unit", "taxes_id")
    def _compute_amount_to_invoice(self):
        for line in self:
            taxes = line.taxes_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.qty_to_invoice,
                line.product_id,
                line.order_id.partner_id,
            )
            line.update(
                {
                    "total_to_invoice": taxes["total_included"],
                    "untaxed_to_invoice": taxes["total_excluded"],
                }
            )

    @api.depends("qty_to_receive", "price_unit", "taxes_id")
    def _compute_amount_to_receive(self):
        for line in self:
            taxes = line.taxes_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.qty_to_receive,
                line.product_id,
                line.order_id.partner_id,
            )
            line.update(
                {
                    "total_to_receive": taxes["total_included"],
                    "untaxed_to_receive": taxes["total_excluded"],
                }
            )

    @api.depends("qty_received", "price_unit", "taxes_id")
    def _compute_amount_received(self):
        for line in self:
            taxes = line.taxes_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.qty_received,
                line.product_id,
                line.order_id.partner_id,
            )
            line.update(
                {
                    "total_received": taxes["total_included"],
                    "untaxed_received": taxes["total_excluded"],
                }
            )

    @api.depends("qty_received_manual", "price_unit", "taxes_id")
    def _compute_amount_received_manually(self):
        for line in self:
            taxes = line.taxes_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.qty_received_manual,
                line.product_id,
                line.order_id.partner_id,
            )
            line.update(
                {
                    "total_received_manually": taxes["total_included"],
                    "untaxed_received_manually": taxes["total_excluded"],
                }
            )
