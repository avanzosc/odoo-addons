# -*- coding: utf-8 -*-
# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    cnae_id = fields.Many2one(
        string="CNAE", comodel_name="res.partner.cnae"
    )
