# Copyright 2022 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.osv import expression


class ProductFinal(models.Model):
    _name = "product.final"
    _description = "Final Product"
    _order = "code"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("product_final_unique_code", "UNIQUE (code)", _("The code must be unique!")),
    ]

    def name_get(self):
        result = super().name_get()
        new_result = []

        for record in result:
            rec = self.browse(record[0])
            name = "[{}] {}".format(rec.code, record[1])
            new_result.append((rec.id, name))
        return new_result

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("code", operator, name)]
        return self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )
