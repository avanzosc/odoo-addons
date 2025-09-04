# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ExtraPhone(models.Model):
    _name = "extra.phone"
    _description = "Contacts Extra Phones"

    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner")
    phone = fields.Text(string="Phone")
    email = fields.Text(string="Email")
    description = fields.Text(string="Description")
