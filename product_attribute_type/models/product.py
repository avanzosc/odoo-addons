# Copyright 2015 Oihane Crucelaegui - AvanzOSC
# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_type = fields.Selection(required=True, selection=[
        ('select', 'Select'),
        ('range', 'Range'),
        ('numeric', 'Numeric')], string="Type", default='select')


class ProductAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    required = fields.Boolean('Required')
    default = fields.Many2one('product.attribute.value', 'Default')
    attr_type = fields.Selection(string='Type', store=False,
                                 related='attribute_id.attr_type')


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_type = fields.Selection(string='Type',
                                 related='attribute_id.attr_type')
    numeric_value = fields.Float('Numeric Value', digits=(12, 6))
    min_range = fields.Float('Min', digits=(12, 6))
    max_range = fields.Float('Max', digits=(12, 6))

    @api.onchange('name')
    def onchange_name(self):
        if self.attr_type == 'numeric' and not self.numeric_value:
            try:
                self.numeric_value = float(self.name)
            except Exception:
                pass
