# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_barcode_unique = fields.Selection(
        related='company_id.partner_barcode_unique', store=True,
    )

    @api.onchange('ref')
    def onchange_ref(self):
        self.barcode = self.ref

    @api.onchange('barcode')
    def onchange_barcode(self):
        self.ref = self.barcode

    @api.multi
    @api.constrains('barcode', 'is_company', 'company_id',
                    'partner_barcode_unique')
    def _check_barcode(self):
        for partner in self:
            mode = partner.partner_barcode_unique
            if (partner.barcode and (
                    mode == 'all' or
                    (mode == 'companies' and partner.is_company))):
                domain = [
                    ('id', '!=', partner.id),
                    ('barcode', '=', partner.barcode),
                ]
                if mode == 'companies':
                    domain.append(('is_company', '=', True))
                other = self.search(domain)

                if other and self.env.context.get("active_test", True):
                    raise ValidationError(
                        _("This barcode is equal to partner '%s'") %
                        other[0].display_name)
