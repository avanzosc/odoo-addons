# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartnerPermissionCreate(models.TransientModel):
    _name = 'res.partner.permission.create'
    _description = 'Wizard to create permission from students'

    student_ids = fields.Many2many(
        comodel_name='res.partner', string='Students')
    center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center")
    type_id = fields.Many2one(
        comodel_name='res.partner.permission.type', string='Type',
        required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.model
    def default_get(self, fields_list):
        res = super(ResPartnerPermissionCreate, self).default_get(fields_list)
        context = self.env.context
        active_ids = context.get('active_ids')
        students = self.env['res.partner']
        if context.get('active_model') == 'res.partner' and active_ids:
            students = students.browse(active_ids).filtered(
                lambda p: p.educational_category in ['student', 'otherchild'])
        res.update({
            'student_ids': [(6, 0, students.ids)],
        })
        return res

    @api.multi
    def create_permissions(self):
        permissions = permission_model = self.env['res.partner.permission']
        for student in self.student_ids:
            permissions |= permission_model.create({
                'partner_id': student.id,
                'center_id': self.center_id.id,
                'type_id': self.type_id.id,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'description': self.description or '',
            })
        action = self.env.ref(
            'contacts_school_permission.action_res_partner_permission')
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [('id', 'in', permissions.ids)],
            safe_eval(action.domain or '[]')
        ])
        action_dict.update({'domain': domain})
        return action_dict
