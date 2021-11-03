
from odoo import api, fields, models


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    update_vat = fields.Boolean('Update VAT code')

    @api.model
    def _get_fpos_by_country(self, country=None):
        base_domain = [('auto_apply', '=', True)]
        fpos = False
        if country:
            domain_country = base_domain + [
                ('country_group_id', 'in', country.country_group_ids.ids)]
            fpos = self.search(domain_country, limit=1)
        return fpos
