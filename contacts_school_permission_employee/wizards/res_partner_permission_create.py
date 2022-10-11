# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartnerPermissionCreate(models.TransientModel):
    _inherit = "res.partner.permission.create"

    # Sobreescribir función
    @api.multi
    def create_permissions(self):
       # action_dict = super(ResPartnerPermissionCreate, self).create_permissions()
        permissions = permission_model = self.env["res.partner.permission"]
        for student in self.student_ids:
            for permission_type in self.type_ids:
                if not permission_type.is_for_employee or (permission_type.is_for_employee and student.employee_id):
                    permissions |= permission_model.create({
                        "partner_id": student.id,
                        "center_id": self.center_id.id,
                        "type_id": permission_type.id,
                        "type_description": permission_type.description or "",
                        "start_date": self.start_date,
                        "end_date": self.end_date,
                        "description": self.description or "",
                    })
        action = self.env.ref(
            "contacts_school_permission.action_res_partner_permission")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", permissions.ids)],
            safe_eval(action.domain or "[]")
        ])
        action_dict.update({"domain": domain})
        return action_dict
