# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    crm_lead_id = fields.Many2one(
        string="Initiative/Opportunity", comodel_name="crm.lead", copy=False
    )
