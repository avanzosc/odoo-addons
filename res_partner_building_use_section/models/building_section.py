# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BuildingSection(models.Model):
    _name = "building.section"
    _description = "Building Section/Area"

    name = fields.Char(string=_("Description"), required=True, copy=False)
    partner_id = fields.Many2one(
        string=_("Contact"), comodel_name="res.partner", required=True, copy=False
    )
    section_use = fields.Many2one("building.use", string=_("Section Use"))
    risk = fields.Char(string=_("Risk"), copy=False)

    superficie = fields.Float(string=_("Surface"), default=0.0, copy=False)
    evacuation_height = fields.Float(string=_('Evacuation Height'))

    configuration = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ], string='Configuration')


