# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    price_subtotal_to_invoice = fields.Monetary(
        compute="_compute_amount_to_invoice",
        string="Subtotal to Bill",
        store=True,
        copy=False,
    )
    price_total_to_invoice = fields.Monetary(
        compute="_compute_amount_to_invoice",
        string="Total to Bill",
        store=True,
        copy=False,
    )
    price_subtotal_to_receive = fields.Monetary(
        compute="_compute_amount_to_receive",
        string="Subtotal to Receive",
        store=True,
        copy=False,
    )
    price_total_to_receive = fields.Monetary(
        compute="_compute_amount_to_receive",
        string="Total to Receive",
        store=True,
        copy=False,
    )
    price_subtotal_invoiced = fields.Monetary(
        compute="_compute_amount_invoiced",
        string="Billed Subtotal",
        store=True,
        copy=False,
    )
    price_total_invoiced = fields.Monetary(
        compute="_compute_amount_invoiced",
        string="Billed Total",
        store=True,
        copy=False,
    )
    price_subtotal_received = fields.Monetary(
        compute="_compute_amount_received",
        string="Received Subtotal",
        store=True,
        copy=False,
    )
    price_total_received = fields.Monetary(
        compute="_compute_amount_received",
        string="Received Total",
        store=True,
        copy=False,
    )

    @api.depends("qty_received", "price_unit", "taxes_id")
    def _compute_amount_received(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals["price_unit"],
                vals["currency_id"],
                vals["qty_received"],
                vals["product"],
                vals["partner"],
            )
            line.update(
                {
                    "price_total_received": taxes["total_included"],
                    "price_subtotal_received": taxes["total_excluded"],
                }
            )

    @api.depends("qty_invoiced", "price_unit", "taxes_id")
    def _compute_amount_invoiced(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals["price_unit"],
                vals["currency_id"],
                vals["qty_invoiced"],
                vals["product"],
                vals["partner"],
            )
            line.update(
                {
                    "price_total_invoiced": taxes["total_included"],
                    "price_subtotal_invoiced": taxes["total_excluded"],
                }
            )

    @api.depends("qty_to_invoice", "price_unit", "taxes_id")
    def _compute_amount_to_invoice(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals["price_unit"],
                vals["currency_id"],
                vals["qty_to_invoice"],
                vals["product"],
                vals["partner"],
            )
            line.update(
                {
                    "price_total_to_invoice": taxes["total_included"],
                    "price_subtotal_to_invoice": taxes["total_excluded"],
                }
            )

    @api.depends("qty_to_receive", "price_unit", "taxes_id")
    def _compute_amount_to_receive(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals["price_unit"],
                vals["currency_id"],
                vals["qty_to_receive"],
                vals["product"],
                vals["partner"],
            )
            line.update(
                {
                    "price_total_to_receive": taxes["total_included"],
                    "price_subtotal_to_receive": taxes["total_excluded"],
                }
            )

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        vals = super()._prepare_compute_all_values()
        vals.update(
            {
                "qty_invoiced": self.qty_invoiced,
                "qty_received": self.qty_received,
                "qty_to_invoice": self.qty_to_invoice,
                "qty_to_receive": self.qty_to_receive,
            }
        )
        return vals
