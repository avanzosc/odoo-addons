# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    lang = fields.Selection(string="Language", related="partner_id.lang")
    company_city = fields.Char(string="Partner City", related="partner_id.city")
    company_zip = fields.Char(string="Partner Zip", related="partner_id.zip")
    company_street = fields.Char(string="Partner Street", related="partner_id.street")
