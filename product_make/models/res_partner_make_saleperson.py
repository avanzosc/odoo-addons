# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartnerMakeSaleperson(models.Model):
    _name = "res.partner.make.saleperson"
    _description = "Make and saleperson for customers"
    _rec_name = "make_id"

    commission_id = fields.Many2one(string="Commission", comodel_name="commission")
    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner")
    make_id = fields.Many2one(string="Make", comodel_name="product.make")
    salesperson_id = fields.Many2one(string="Salesperson", comodel_name="res.users")
