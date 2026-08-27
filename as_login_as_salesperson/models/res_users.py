from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsersSalespersons(models.Model):
    _name = "res.users.salespersons"

    person_id = fields.Many2one("res.users", string="User")
    user_id = fields.Many2one(
        "res.users",
        string="Access User",
        domain=lambda self: [
            "|",
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id),
            ("groups_id", "in", self.env.ref("base.group_portal").id),
            ("is_login_saleperson", "!=", True),
        ],
    )
    login = fields.Char(string="Login", related="user_id.email")

    _sql_constraints = [
        (
            "code_user_uniq",
            "unique (user_id)",
            "You Can Add User one time in Access List!",
        )
    ]


class ResUsers(models.Model):
    _inherit = "res.users"

    available_portal_user_ids = fields.One2many(
        "res.users.salespersons", "person_id", string="Available Users"
    )
    is_login_saleperson = fields.Boolean(string="Is Sale Person?")

    @api.constrains("available_portal_user_ids", "available_portal_user_ids.user_id")
    def check_unique_sale_user(self):
        for record in self:
            exist_user = []
            if record.available_portal_user_ids:
                for portal_user in record.available_portal_user_ids:
                    if portal_user.user_id and portal_user.user_id.id in exist_user:
                        raise ValidationError(_("Duplicate Access Users"))
                    if portal_user.user_id and record.id == portal_user.user_id.id:
                        raise ValidationError(
                            _("Current User not allow to add in Access Users")
                        )
                    exist_user.append(portal_user.user_id.id)
