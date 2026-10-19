# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    require_num_sales_authorization = fields.Boolean(
        string="Require num. sales authorization"
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if not self.partner_id:
            return result
        self.require_num_sales_authorization = getattr(
            self.partner_id.purchase_group_id, "require_num_sales_authorization", False
        )
        if (
            self.partner_id.purchase_group_id
            and self.partner_id.purchase_group_id.billing_customer_id
        ):
            billing_customer = self.partner_id.purchase_group_id.billing_customer_id
            addr = billing_customer.address_get(["delivery", "invoice"])
            self.partner_invoice_id = addr["invoice"]
            message = _("Invoice with purchasing group {}.").format(
                self.partner_id.purchase_group_id.name
            )
            if result is None:
                warning = {"title": _("Invoicing!"), "message": message}
                result = {}
                result["warning"] = warning
            else:
                if "warning" in result and result.get("warning").get("message", False):
                    message = result.get("warning").get("message")
                    message += _(", invoice with purchasing group {}").format(
                        self.partner_id.purchase_group_id.name
                    )
                    result["warning"]["message"] = message
        return result

    def action_confirm(self):
        for sale in self:
            if (
                not sale.client_order_ref
                and sale.partner_id.purchase_group_id
                and sale.partner_id.purchase_group_id.require_num_sales_authorization
            ):
                raise ValidationError(_("You must enter customer order reference"))
        return super().action_confirm()
