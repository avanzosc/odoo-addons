# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.depends('qc_test_ids')
    def _compute_qc_test_count(self):
        for record in self:
            record.qc_test_count = len(record.qc_test_ids)

    qc_test_ids = fields.One2many(comodel_name='qc.test',
                                  inverse_name='partner_id', string='Tests')
    qc_test_count = fields.Integer(string='Tests',
                                   compute='_compute_qc_test_count')
