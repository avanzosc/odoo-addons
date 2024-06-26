# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    lines_count = fields.Integer(
        string="Lines Count", compute="_compute_order_lines", store=True
    )
    price_subtotal_to_invoice = fields.Monetary(
        compute="_compute_amount_to_invoice",
        string="Subtotal to Bill",
        store=True,
    )
    price_total_to_invoice = fields.Monetary(
        compute="_compute_amount_to_invoice",
        string="Total to Bill",
        store=True,
    )
    price_subtotal_to_receive = fields.Monetary(
        compute="_compute_amount_to_receive",
        string="Subtotal to Receive",
        store=True,
    )
    price_total_to_receive = fields.Monetary(
        compute="_compute_amount_to_receive",
        string="Total to Receive",
        store=True,
    )
    price_subtotal_invoiced = fields.Monetary(
        compute="_compute_amount_invoiced",
        string="Billed Subtotal",
        store=True,
    )
    price_total_invoiced = fields.Monetary(
        compute="_compute_amount_invoiced",
        string="Billed Total",
        store=True,
    )
    price_subtotal_received = fields.Monetary(
        compute="_compute_amount_received",
        string="Received Subtotal",
        store=True,
    )
    price_total_received = fields.Monetary(
        compute="_compute_amount_received",
        string="Received Total",
        store=True,
    )

    @api.depends("order_line")
    def _compute_order_lines(self):
        for line in self:
            line.lines_count = len(line.order_line)

    @api.depends(
        "order_line",
        "order_line.price_total_to_invoice",
        "order_line.price_subtotal_to_invoice",
    )
    def _compute_amount_to_invoice(self):
        for sale in self:
            sale.price_total_to_invoice = sum(
                sale.order_line.mapped("price_total_to_invoice")
            )
            sale.price_subtotal_to_invoice = sum(
                sale.order_line.mapped("price_subtotal_to_invoice")
            )

    @api.depends(
        "order_line",
        "order_line.price_total_to_receive",
        "order_line.price_subtotal_to_receive",
    )
    def _compute_amount_to_receive(self):
        for sale in self:
            sale.price_total_to_receive = sum(
                sale.order_line.mapped("price_total_to_receive")
            )
            sale.price_subtotal_to_receive = sum(
                sale.order_line.mapped("price_subtotal_to_receive")
            )

    @api.depends(
        "order_line",
        "order_line.price_total_invoiced",
        "order_line.price_subtotal_invoiced",
    )
    def _compute_amount_invoiced(self):
        for sale in self:
            sale.price_total_invoiced = sum(
                sale.order_line.mapped("price_total_invoiced")
            )
            sale.price_subtotal_invoiced = sum(
                sale.order_line.mapped("price_subtotal_invoiced")
            )

    @api.depends(
        "order_line",
        "order_line.price_total_received",
        "order_line.price_subtotal_received",
    )
    def _compute_amount_received(self):
        for sale in self:
            sale.price_total_received = sum(
                sale.order_line.mapped("price_total_received")
            )
            sale.price_subtotal_received = sum(
                sale.order_line.mapped("price_subtotal_received")
            )

    def action_view_lines(self):
        action = self.env.ref("purchase_order_line_menu.action_purchase_orders_lines")
        result = action.read()[0]
        # create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        result["context"] = {
            "type": "in_invoice",
            "default_order_id": self.id,
            "default_currency_id": self.currency_id.id,
            "default_company_id": self.company_id.id,
            "company_id": self.company_id.id,
        }
        # choose the view_mode accordingly
        result["domain"] = "[('order_id', '=', {})]".format(self.id)
        return result


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

    @api.model
    def create(self, vals):
        if not vals.get("order_id", False):
            purchase_order = self.env["purchase.order"]
            new_po = purchase_order.new(
                {
                    "partner_id": vals.pop("partner_id"),
                }
            )
            for onchange_method in new_po._onchange_methods["partner_id"]:
                onchange_method(new_po)
            order_data = new_po._convert_to_write(new_po._cache)
            vals["order_id"] = new_po.create(order_data).id
        return super().create(vals)

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

    def action_purchase_order_form(self):
        self.ensure_one()
        action = self.env.ref("purchase.purchase_form_action")
        form = self.env.ref("purchase.purchase_order_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["res_id"] = self.order_id.id
        return action
