
from odoo import api, fields, models
from odoo.osv import expression


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    name = fields.Char(readonly=False)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', 'ilike', name), ('warehouse_id', 'ilike', name)]
        return self._search(expression.AND([domain, args]), limit=limit,
                            access_rights_uid=name_get_uid)
