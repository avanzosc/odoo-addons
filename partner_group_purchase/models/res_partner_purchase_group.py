# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerPurchaseGroup(models.Model):
    _name = "res.partner.purchase_group"
    _description = "Cooperatives"

    name = fields.Char(required=True, translate=True)
    billing_customer_id = fields.Many2one(
        string="Billing customer", comodel_name="res.partner"
    )
    require_num_sales_authorization = fields.Boolean(
        string="Require num. sales authorization", default=False
    )
