# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_supplier_invoice_price = fields.Float(
        string="Last supplier invoice price",
        digits=dp.get_precision('Product Price'))
    last_supplier_invoice_date = fields.Date(
        string="Last supplier invoice date")
    last_supplier_invoice_id = fields.Many2one(
        comodel_name='res.partner', string="Last supplier invoice")

    def set_product_template_last_purchase_invoice(
            self, last_supplier_invoice_date, last_supplier_invoice_price,
            last_supplier_invoice_id):
        return self.write({
            "last_supplier_invoice_date": last_supplier_invoice_date,
            "last_supplier_invoice_price": last_supplier_invoice_price,
            "last_supplier_invoice_id": (last_supplier_invoice_id.id if
                                         last_supplier_invoice_id else False),
        })
