
import re
from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):

    def values_preprocess(self, order, mode, values):
        if 'vat' in values:
            vat = values.get('vat')
            alpha = " ".join(re.findall("[a-zA-Z]+", vat))
            if alpha:
                values['vat'] = str(alpha) + vat.replace(alpha, '')
        result = super().values_preprocess(order, mode, values)
        return result
