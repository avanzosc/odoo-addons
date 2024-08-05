# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResActivityType(models.Model):
    _name = "res.activity.type"
    _description = "Activity Types"

    name = fields.Char(required=True)
    description = fields.Text()
    activity_id = fields.Many2one(
        comodel_name="res.activity", required=True, string="Activity"
    )
