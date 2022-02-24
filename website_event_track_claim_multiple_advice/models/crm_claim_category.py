# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class CrmClaimCategory(models.Model):
    _inherit = 'crm.claim.category'

    number_of_consecutive_fouls = fields.Integer(
        string='Number of consecutive fouls', default=0,
        help='When claims of this type are created in a participant of an '
        'event session with this number of consecutive sessions, an email will'
        ' be sent to the person in charge of the event.')
