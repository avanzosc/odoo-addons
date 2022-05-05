# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    code = fields.Char(size=6)
    farm_area = fields.Float()
    farm_capacity = fields.Float()
    farm_owned = fields.Boolean()
    farm_numexp = fields.Char()
    farm_rega_cmpl = fields.Char()
    farm_maximum = fields.Float()
    farm_minimum = fields.Float()
    farm_distance = fields.Float()
    partner_latitude = fields.Float(
        related="partner_id.partner_latitude",
        store=True,
    )
    partner_longitude = fields.Float(
        related="partner_id.partner_longitude",
        store=True,
    )
    farmer_id = fields.Many2one(
        string='Farmer',
        comodel_name='res.partner')
    tax_entity_id = fields.Many2one(
        string='Tax Entity',
        comodel_name='res.partner')
    activity = fields.Selection(
        [('fattening', 'Fattening'),
         ('incubation', 'Incubation'),
         ('reproduction', 'Reproduction')], string="Activity", copy=False)
    other_activity = fields.Char(string='Other Activity')
    farm_type = fields.Selection(
        [('integrated', 'Integrated'),
         ('own', 'Own')], string="Farm Type", copy=False)
    type_id = fields.Many2one(
        string='Type',
        comodel_name='category.type')
