# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    origin_purchase_id = fields.Many2one(
        string="Origin purchase", comodel_name="purchase.order")
