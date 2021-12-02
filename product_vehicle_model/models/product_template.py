# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tag_ids = fields.Many2many(
        string='Distribution Tags', comodel_name='fleet.vehicle.tag')
    model_id = fields.Many2one(
        string='Model', comodel_name='fleet.vehicle.model')
    brand_id = fields.Many2one(
        string='Brand', comodel_name='fleet.vehicle.model.brand',
        related='model_id.brand_id', store=True)
    collection_id = fields.Many2one(
        string='Collection', comodel_name='fleet.vehicle.model.collection')
    type_id = fields.Many2one(
        string='Type', comodel_name='fleet.vehicle.model.type',
        related='model_id.type_id', store=True)
    range_id = fields.Many2one(
        string='Range', comodel_name='fleet.vehicle.range',
        related='model_id.range_id', store=True)
