# Copyright 2018 Xanti Pablo - AvanzOSC
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResArea(models.Model):
    _name = "res.area"
    _description = "Areas"
    _order = "code,name"

    name = fields.Char(required=True)
    code = fields.Char()
    description = fields.Text()
    type_ids = fields.Many2many(
        string="Area Types",
        comodel_name="res.area.type",
        relation="rel_area_area_type",
        column1="res_area_id",
        column2="res_area_type_id",
        copy=False,
    )

    def name_get(self):
        """name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        res = []
        for area in self:
            name = area.name
            if area.code:
                name = "{}. {}".format(area.code, name)
            res.append((area.id, name))
        return res
