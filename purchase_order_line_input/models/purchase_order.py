# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    lines_count = fields.Integer(
        compute="_compute_order_lines",
        store=True,
    )

    @api.depends("order_line")
    def _compute_order_lines(self):
        for line in self:
            line.lines_count = len(line.order_line)

    def action_view_lines(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "purchase_order_line_menu.action_purchase_orders_lines"
        )
        # create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        action["context"] = {
            "type": "in_invoice",
            "default_order_id": self.id,
            "default_currency_id": self.currency_id.id,
            "default_company_id": self.company_id.id,
            "company_id": self.company_id.id,
        }
        # choose the view_mode accordingly
        action["domain"] = expression.AND(
            [[("order_id", "in", self.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    user_id = fields.Many2one(
        related="order_id.user_id",
        store=True,
        string="Purchase Representative",
        readonly=True,
    )
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

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            # partner_id = values.pop("partner_id")
            if not values.get("order_id", False):
                purchase_order = self.env["purchase.order"]
                new_po = purchase_order.new(
                    {
                        "partner_id": values.get("partner_id"),
                    }
                )
                for onchange_method in new_po._onchange_methods[
                    "partner_id", "product_qty"
                ]:
                    onchange_method(new_po)
                order_data = new_po._convert_to_write(new_po._cache)
                values["order_id"] = new_po.create(order_data).id
            if not values.get("display_type", False) and (
                "date_planned" in values and not values.get("date_planned", False)
            ):
                values.pop("date_planned")
        lines = super().create(vals_list)
        return lines

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        vals = {
            "price_unit": self.price_unit,
            "currency_id": self.order_id.currency_id,
            "product_qty": self.product_qty,
            "product": self.product_id,
            "partner": self.order_id.partner_id,
        }

        vals.update(
            {
                "qty_invoiced": self.qty_invoiced,
                "qty_received": self.qty_received,
                "qty_to_invoice": self.qty_to_invoice,
                "qty_to_receive": self.qty_to_receive,
            }
        )
        return vals

    def action_purchase_order_form(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "purchase.purchase_form_action"
        )
        form = self.env.ref("purchase.purchase_order_form")
        action["views"] = [(form.id, "form")]
        action["res_id"] = self.order_id.id
        return action
