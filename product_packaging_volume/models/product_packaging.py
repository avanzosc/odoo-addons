# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    def _get_default_volume_uom(self):
        return self.env[('product.template'
                         )]._get_volume_uom_name_from_ir_config_parameter()

    volume = fields.Float(string='Volume', compute='_compute_volume')
    volume_uom_name = fields.Char(
        string='Volume unit of measure label',
        compute='_compute_volume_uom_name', default=_get_default_volume_uom)

    def _compute_volume_uom_name(self):
        for packaging in self:
            packaging.volume_uom_name = (
                self.env[('product.template'
                          )]._get_volume_uom_name_from_ir_config_parameter())

    @api.depends("height", "width", "packaging_length")
    def _compute_volume(self):
        for record in self:
            record.volume = (
                record.height * record.width * record.packaging_length)
