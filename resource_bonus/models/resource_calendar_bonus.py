# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResourceCalendarBonus(models.Model):
    _name = 'resource.calendar.bonus'
    _description = 'Bonus Days'

    @api.model
    def _get_selection_dayofweek(self):
        return self.env['resource.calendar.attendance'].fields_get(
            allfields=['dayofweek'])['dayofweek']['selection']

    def default_dayofweek(self):
        default_dict = self.env['resource.calendar.attendance'].default_get([
            'dayofweek'])
        return default_dict.get('dayofweek')

    calendar_id = fields.Many2one(
        comodel_name='resource.calendar', string='Working Time', required=True)
    dayofweek = fields.Selection(
        selection='_get_selection_dayofweek', string='Day of Week',
        required=True, index=True, default=default_dayofweek)
    bonus_percentage = fields.Float(string='Bonus')

    _sql_constraints = [
        ('calendar_bonus_uniq', 'unique(calendar_id,dayofweek)',
         'You can only select a day of week once per working time!'),
        ('percentage', 'check(bonus_percentage between 0 and 100)',
         'Bonus must be between 0 and 100!'),
    ]
