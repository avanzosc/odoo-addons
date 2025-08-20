# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id", "product_uom_qty", "product_uom", "route_id")
    def _onchange_product_show_warning_availability(self):
        """Take into account only on hand - outgoing, not incoming quantities.
        Standard takes into account virtual available (on hand - outgoing +
        incoming). The code is copied with this adapted.
        """
        if (
            not self.product_id
            or not self.product_uom_qty
            or not self.product_uom
            or self.product_id.type != "product"
        ):
            return
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        product = self.product_id.with_context(
            warehouse=self.order_id.warehouse_id.id,
            lang=(self.order_id.partner_id.lang or self.env.user.lang or "en_US"),
        )
        product_qty = self.product_uom._compute_quantity(
            self.product_uom_qty, self.product_id.uom_id
        )
        my_message = ""
        qty = product.virtual_available - product.incoming_qty
        if float_compare(qty, product_qty, precision_digits=precision) == -1:
            is_available = self._check_routing()
            if not is_available:
                message = _(
                    "You plan to sell %s %s of %s but you only have %s %s "
                    "available in %s warehouse."
                ) % (
                    self.product_uom_qty,
                    self.product_uom.name,
                    product.display_name,
                    qty,
                    product.uom_id.name,
                    self.order_id.warehouse_id.name,
                )
                # We check if some products are available in other warehouses.
                wh_msg = ""
                for warehouse in self.env["stock.warehouse"].search(
                    [("id", "!=", self.order_id.warehouse_id.id)]
                ):
                    wh_qtys = 0
                    wh_prod = self.product_id.with_context(warehouse=warehouse.id)
                    qty = wh_prod.virtual_available - wh_prod.incoming_qty
                    if qty > 0:
                        wh_qtys += qty
                        wh_msg += "{}: {} {}\n".format(
                            warehouse.name,
                            qty,
                            self.product_id.uom_id.name,
                        )
                if wh_msg:
                    message += (
                        _("\nThere are %s %s available across all " "warehouses.\n\n")
                        % (wh_qtys, product.uom_id.name)
                        + wh_msg
                    )
                my_message = "{}\n{}".format(my_message, message)
        if my_message:
            return {
                "warning": {
                    "title": _("Warning!"),
                    "message": my_message,
                }
            }

    @api.depends(
        "qty_delivered_method",
        "analytic_line_ids.so_line",
        "analytic_line_ids.unit_amount",
        "analytic_line_ids.product_uom_id",
    )
    def _compute_qty_delivered(self):
        """Compute qty delivered to property_stock_customer without taking
        into account the location usage
        """
        for line in self:
            stock_customer = line.order_id.partner_shipping_id.property_stock_customer
            if stock_customer.usage == "customer":
                super(SaleOrderLine, line)._compute_qty_delivered()
            elif line.qty_delivered_method == "stock_move":
                qty = 0.0
                for move in line.move_ids.filtered(
                    lambda r: (
                        r.state == "done"
                        and not r.scrapped
                        and line.product_id == r.product_id
                    )
                ):
                    if (
                        move.location_dest_id.usage == "customer"
                        or move.location_dest_id == stock_customer
                    ):
                        if not move.origin_returned_move_id or (
                            move.origin_returned_move_id and move.to_refund
                        ):
                            qty += move.product_uom._compute_quantity(
                                move.product_uom_qty, line.product_uom
                            )
                    elif move.to_refund:
                        qty -= move.product_uom._compute_quantity(
                            move.product_uom_qty, line.product_uom
                        )
                line.qty_delivered = qty

    @api.onchange("make_id")
    def make_agents_change(self):
        self.put_agents_commissions()

    @api.onchange("product_id", "product_uom_qty")
    def _onchange_product_id_agents_commissions(self):
        self.agent_ids.update({"active": True})
        self.put_agents_commissions()

    def put_agents_commissions(self):
        sale = self.order_id
        if self.make_id and self.agent_ids and sale.partner_id.make_saleperson_ids:
            for agent in self.agent_ids:
                cond = [("partner_id", "=", agent.agent.id)]
                user = self.env["res.users"].search(cond, limit=1)
            if user:
                if sale.partner_id != sale.partner_shipping_id:
                    make_saleperson_ids = sale.partner_shipping_id.make_saleperson_ids
                else:
                    self.order_id.partner_id.make_saleperson_ids
                self._review_commission_from_saleperson(
                    make_saleperson_ids, user, agent, desactive_commission=True
                )

    def _review_commission_from_saleperson(
        self, partner_makes, user, agent, desactive_commission
    ):
        lines = partner_makes.filtered(
            lambda x: x.salesperson_id.id == user.id and x.make_id.id == self.make_id.id
        )
        if not lines and desactive_commission:
            agent.update({"active": False})
        if len(lines) == 1:
            if lines[0].commission_id and lines[0].commission_id != agent.commission:
                agent.update({"commission": lines[0].commission_id.id})

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            line.order_id.update_division_in_sales()
        return lines
