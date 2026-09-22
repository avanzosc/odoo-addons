# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    purchase_group_id = fields.Many2one(
        string="Cooperative",
        comodel_name="res.partner.purchase_group",
    )
    purchase_group2_id = fields.Many2one(
        string="Purchase Group",
        comodel_name="res.partner.purchase_group2",
    )
