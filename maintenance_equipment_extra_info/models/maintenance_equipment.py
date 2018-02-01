# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Lot/Serial Number')
    lot_product_id = fields.Many2one(
        comodel_name='product.product', string='Product of the lot',
        related='lot_id.product_id')
    invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line', string='Purchase invoice line')
    invoice_id = fields.Many2one(
        comodel_name='account.invoice', string='Invoice',
        related='invoice_line_id.invoice_id')
    supplier_id = fields.Many2one(
        comodel_name='res.partner', string='Supplier',
        related='invoice_id.partner_id')
    invoice_date = fields.Date(
        string='Date', related='invoice_id.date_invoice')
    invoice_state = fields.Selection(
        string='State', related='invoice_id.state')
    invoice_amount_untaxed = fields.Monetary(
        string='Untaxed Amount', related='invoice_id.amount_untaxed')
    currency_id = fields.Many2one(
        comodel_name='res.currency', related='invoice_id.currency_id')
