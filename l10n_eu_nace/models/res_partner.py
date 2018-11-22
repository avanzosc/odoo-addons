
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    main_nace_id = fields.Many2one(
        comodel_name='res.partner.nace',
        string='Main activity',
        ondelete='set null',
    )
    secondary_nace_ids = fields.Many2many(
        comodel_name='res.partner.nace',
        string='Other activities',
        ondelete='set null',
    )
