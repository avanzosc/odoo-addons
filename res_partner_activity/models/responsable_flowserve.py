# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResponsableFlowServe(models.Model):
    _name = "responsable.flowserv"
    _description = "Flowserve Manager"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, index=True)
    active = fields.Boolean()
    sequence = fields.Integer()
