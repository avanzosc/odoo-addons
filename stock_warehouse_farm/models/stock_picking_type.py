# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    category_type_id = fields.Many2one(
        string='Origin Section',
        comodel_name='category.type',
        related="default_location_src_id.type_id",
        store=True)
    dest_category_type_id = fields.Many2one(
        string='Destination Section',
        comodel_name='category.type',
        related="default_location_dest_id.type_id",
        store=True)
    egg_production = fields.Boolean(
        string="Is Egg Production",
        default=False)
    burden_to_incubator = fields.Boolean(
        string="Is Burden to Incubator",
        default=False)
