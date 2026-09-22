# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerPurchaseGroup2(models.Model):
    _name = "res.partner.purchase_group2"
    _description = "Purchase Groups"

    name = fields.Char(required=True, translate=True)
