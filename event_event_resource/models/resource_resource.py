# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    email = fields.Char(string="Email")
    password = fields.Char(string="Password")
