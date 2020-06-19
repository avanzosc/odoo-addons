# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class FleetRoute(models.Model):
    _inherit = 'account.invoice'

    invoice_text = fields.Char(string='Invoice text',
                               comodel_name='account.fiscal.position',
                               related='fiscal_position_id.invoice_text')
    invoice_text_hide = fields.Boolean(string='Hide',
                                       compute="_compute_invoice_text_hide")

    @api.onchange('fiscal_position_id')
    def _compute_invoice_text_hide(self):
        if self.fiscal_position_id:
            self.invoice_text_hide = False
        else:
            self.invoice_text_hide = True
