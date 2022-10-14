# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    last_supplier_invoice_date = fields.Date(
        string="Last supplier invoice date")
    last_supplier_invoice_price = fields.Float(
        string="Last supplier invoice price",
        digits=dp.get_precision('Product Price'))
    last_supplier_invoice_id = fields.Many2one(
        comodel_name='res.partner', string="Last supplier invoice")

    @api.multi
    def set_product_last_supplier_invoice(self, invoice_id=False):
        invoice_line_obj = self.env['account.invoice.line']
        if not self.check_access_rights('write', raise_exception=False):
            return
        for product in self:
            last_supplier_invoice_date = False
            last_supplier_invoice_price = 0.0
            last_supplier_invoice_id = False
            if invoice_id:
                cond = [('invoice_id', '=', invoice_id),
                        ('product_id', '=', product.id)]
                lines = invoice_line_obj.search(cond, limit=1)
            else:
                cond = [('product_id', '=', product.id),
                        ('invoice_id.state', 'not in', ['draft', 'cancel'])]
                lines = invoice_line_obj.search(cond).sorted(
                    key=lambda l: l.invoice_id.date_invoice, reverse=True)
            if lines:
                last_line = lines[:1]
                last_supplier_invoice_date = last_line.invoice_id.date_invoice
                last_supplier_invoice_price = product.uom_id._compute_quantity(
                    last_line.price_unit, last_line.uom_id)
                last_supplier_invoice_id = last_line.invoice_id.partner_id
            product.write({
                "last_supplier_invoice_date": last_supplier_invoice_date,
                "last_supplier_invoice_price": last_supplier_invoice_price,
                "last_supplier_invoice_id": (
                    last_supplier_invoice_id.id if last_supplier_invoice_id else
                    False),
            })
            product.product_tmpl_id.set_product_template_last_purchase(
                last_supplier_invoice_date, last_supplier_invoice_price,
                last_supplier_invoice_id)
