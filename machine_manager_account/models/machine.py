# -*- coding: utf-8 -*-
# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class Machine(models.Model):
    _inherit = "machine"

    assetacc_id = fields.Many2one(
        string="Asset Account", comodel_name="account.account"
    )
    depracc_id = fields.Many2one(
        string="Depreciation Account", comodel_name="account.account"
    )
