# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplateCustomerCode(models.Model):
    _name = "product.template.customer.code"
    _description = "Customer code for products"

    partner_id = fields.Many2one(
        string="Customer", comodel_name="res.partner", copy=False
    )
    customer_code = fields.Char(string="Customer product code", copy=False)
    template_id = fields.Many2one(
        string="Product", comodel_name="product.template", copy=False
    )
