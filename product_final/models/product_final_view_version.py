# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class ProductFinalViewVersion(models.Model):
    _name = "product.final.view.version"
    _description = "Views Version"
    _order = "code"

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        required=True,
    )

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.code, record.name)) for record in self]

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("code", operator, name), ("name", operator, name)]
        return self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )

    @api.constrains("code")
    def _check_unique_code(self):
        for final in self:
            cond = [("id", "!=", final.id), ("code", "=", final.code)]
            f = self.env["product.final.view.version"].search(cond, limit=1)
            if f:
                raise UserError(
                    _(
                        'You are putting the code "%(final_code)s" to the name '
                        '"%(final_name)s", and that code already exists for the name '
                        '"%(name)s".'
                    )
                    % {
                        "final_code": final.code,
                        "final_name": final.name,
                        "name": f.name,
                    }
                )
