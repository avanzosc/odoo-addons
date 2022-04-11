# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    second_uom_id = fields.Many2one(
        string='Second Unit of Measure', comodel_name='uom.uom')
    factor = fields.Float(
        string='Conversion Factor', default=1, digits='Factor')
    factor_inverse = fields.Float(
        string='Conversion Factor Inverse', compute='_compute_factor_inverse',
        digits='Factor')
    weight_second_uom = fields.Float(
        string='Weight Second UOM', compute='_compute_weight_second_uom',
        store=True)
    qty_available_second_uom = fields.Float(
        string='Available in Second UOM',
        compute='_compute_qty_available_second_uom', store=True)
    virtual_available_second_uom = fields.Float(
        string='Virtual Second UOM',
        compute='_compute_virtual_available_second_uom', store=True)

    @api.depends('factor')
    def _compute_factor_inverse(self):
        for product in self:
            if product.factor:
                product.factor_inverse = 1 / product.factor

    @api.depends('factor_inverse', 'weight')
    def _compute_weight_second_uom(self):
        for product in self:
            product.weight_second_uom = product.factor_inverse * product.weight

    @api.depends('qty_available', 'factor')
    def _compute_qty_available_second_uom(self):
        for product in self:
            product.qty_available_second_uom = product.qty_available * product.factor

    @api.depends('virtual_available', 'factor')
    def _compute_virtual_available_second_uom(self):
        for product in self:
            product.virtual_available_second_uom = product.virtual_available * product.factor
