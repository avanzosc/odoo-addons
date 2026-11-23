# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairService(models.Model):
    _inherit = "repair.service"

    @api.model
    def _get_default_product_id(self):
        cond = [("default_product_manufacturing_operations", "=", True)]
        return self.env["product.product"].search(cond, limit=1)

    product_id = fields.Many2one(default=_get_default_product_id)
    price_unit = fields.Float(string="Unit Price", digits="Product Price")
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="repair_service_account_tax_rel",
        column1="service_id",
        column2="tax_id",
        domain=[("type_tax_use", "=", "sale")],
        check_company=True,
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        digits="Product Price",
        compute="_compute_price_subtotal",
        store=True,
    )
    price_tax = fields.Float(
        string="Tax Amount",
        digits="Product Price",
        compute="_compute_price_subtotal",
        store=True,
    )

    @api.depends("product_uom_qty", "price_unit", "tax_ids")
    def _compute_price_subtotal(self):
        for service in self:
            amounts = service.tax_ids.compute_all(
                service.price_unit,
                currency=service.company_id.currency_id,
                quantity=service.product_uom_qty,
                product=service.product_id,
                partner=service.repair_id.partner_id,
            )
            service.price_subtotal = amounts["total_excluded"]
            service.price_tax = amounts["total_included"] - amounts["total_excluded"]

    def _get_product_sale_price(self):
        self.ensure_one()
        price_unit = self.product_id.lst_price
        if self.product_uom and self.product_id:
            price_unit = self.product_id.uom_id._compute_price(
                price_unit, self.product_uom
            )
        return price_unit

    def _get_repair_taxes(self):
        self.ensure_one()
        if not self.product_id:
            return self.env["account.tax"]
        return self.repair_id._get_repair_product_taxes(self.product_id)

    @api.onchange("product_id", "product_uom")
    def _onchange_product_price_unit(self):
        if self.repair_id.sale_id:
            self.price_unit = self._get_product_sale_price()
            self.tax_ids = self._get_repair_taxes()

    @api.model_create_multi
    def create(self, vals_list):
        services = super().create(vals_list)
        for service, vals in zip(services, vals_list, strict=True):
            if not service.repair_id.sale_id:
                continue
            if "price_unit" not in vals:
                service.price_unit = service._get_product_sale_price()
            if "tax_ids" not in vals:
                service.tax_ids = service._get_repair_taxes()
        services.repair_id._put_amount_untaxed_in_price_in_sale_budget()
        return services

    def write(self, vals):
        result = super().write(vals)
        if "product_uom_qty" in vals or "price_unit" in vals:
            self.repair_id._put_amount_untaxed_in_price_in_sale_budget()
        return result
