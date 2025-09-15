from odoo import api, models


class Gs1Barcode(models.Model):
    _inherit = "gs1_barcode"

    def name_get(self):
        result = []
        for record in self:
            name = f"({record.ai}) {record.name}"
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = ["|", ("ai", operator, name), ("name", operator, name)] if name else []
        return self.search(domain + args, limit=limit).name_get()
