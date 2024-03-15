
from odoo import api, fields, models


class CrmTeamGroup(models.Model):
    _name = "crm.team.group"
    _description = "Sales Team Group"

    name = fields.Char('Name', required=True, translate=True)
    user_id = fields.Many2one('res.users', string='Team Group Leader')
    team_ids = fields.One2many('crm.team', 'group_id', string='Teams')


class CrmTeam(models.Model):
    _inherit = "crm.team"

    group_id = fields.Many2one(
        'crm.team.group', 'Team Group', readonly=False,
        store=True)
