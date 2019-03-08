# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResAreaType(models.Model):
    _name = 'res.area.type'
    _description = 'Area types'
    _order = 'code,name'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    area_ids = fields.Many2many(
        string="Areas", comodel_name="res.area",
        relation="rel_area_area_type", columm1="res_area_type_id",
        columm2='res_area_id', copy=False)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        res = []
        for areatype in self:
            name = areatype.name
            if areatype.code:
                name = '{}. {}'.format(areatype.code, name)
            res.append((areatype.id, name))
        return res
