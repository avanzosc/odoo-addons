# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contact_id = fields.Many2one(
        comodel_name='res.partner', string='Contact Values')
