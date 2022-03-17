# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity = fields.Selection(
        [('fattening', 'Fattening'),
         ('incubation', 'Incubation'),
         ('reproduction', 'Reproduction')], string="Activity", copy=False)
    farm_type = fields.Selection(
        [('integrated', 'Integrated'),
         ('own', 'Own')], string="Farm Type", copy=False)
    leaving_date = fields.Date(string='Leaving Date')
    other_activity = fields.Char(string='Other Activity')
    eurowin_account = fields.Char(string='Eurowin Account')
    account_journal_id = fields.Many2one(
        string='Journal',
        comodel_name='account.journal',
        domain=[('type', '=', 'purchase')])

    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name', 'ref')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()

    def name_get(self):
        result = []
        for partner in self:
            name = partner.name
            if partner.parent_id:
                name = u'{}, {}'.format(partner.parent_id.name, name)
            if partner.ref:
                name = u'{} {}'.format(partner.ref, name)
            result.append((partner.id, name))
        return result
