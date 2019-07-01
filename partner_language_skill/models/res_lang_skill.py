# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResLangSkill(models.Model):
    _name = 'res.lang.skill'
    _description = 'Language skills'

    name = fields.Char(required=True)
    lang_id = fields.Many2one(
        comodel_name='res.lang', string='Language', required=True,
        context={'active_test': False})
    level = fields.Selection(
        selection=[('A1', 'A1'),
                   ('A2', 'A2'),
                   ('B1', 'B1'),
                   ('B2', 'B2'),
                   ('C1', 'C1'),
                   ('C2', 'C2')],
        string='Level', required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append((record.id, '{} - {} - {}'.format(
                record.level, record.name, record.lang_id.name)))
        return result
