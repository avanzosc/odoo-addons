# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    live_chicken = fields.Boolean(string="Live Chicken", default=False)
    one_day_chicken = fields.Boolean(string="One Day Chicken", default=False)
    egg = fields.Boolean(string="Incubator Egg", default=False)
