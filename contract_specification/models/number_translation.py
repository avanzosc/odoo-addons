# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models


class NumberTranslation(models.Model):
    _name = 'number.translation'

    name = fields.Char(string='Name', translate=True, required=True)
    item_ids = fields.One2many(
        comodel_name='number.translation.item', string='Items',
        inverse_name='list_id')


class NumberTranslationItem(models.Model):
    _name = 'number.translation.item'

    number = fields.Integer(string='Number', required=True)
    translation = fields.Char(
        string='Translate as', required=True, translate=True)
    list_id = fields.Many2one(
        comodel_name='number.translation', string='List', required=True)

    _sql_constraints = [
        ('number_list_uniq', 'unique(number, list_id)',
         'There can not be same number in one list'),
    ]

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        results = super(NumberTranslationItem, self).name_get()
        return results
