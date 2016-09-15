# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class QcInspection(models.Model):
    _inherit = 'qc.inspection'

    inventory_line_id = fields.Many2one(
        comodel_name="stock.inventory.line", string="Inventory Line")
    inventory_id = fields.Many2one(
        comodel_name="stock.inventory", string="Inventory",
        related="inventory_line_id.inventory_id", store=True)
