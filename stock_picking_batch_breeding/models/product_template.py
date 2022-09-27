# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    one_day_chicken = fields.Boolean(string="One Day Chicken", default=False)
    asphyxiated = fields.Boolean(string="Asphyxiated", default=False)
    chicken_seized = fields.Boolean(string="Chicken Seized", default=False)
