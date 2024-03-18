from odoo import SUPERUSER_ID, api, exceptions, fields, models
from odoo.tools.translate import _

MODULE_NAME = "ir_rule_protected"


class IRRule(models.Model):
    _inherit = "ir.rule"

    protected = fields.Boolean(
        "Protected", help="Make rule editable only for superuser"
    )

    @api.multi
    def check_restricted(self):
        if self.env.user.id == SUPERUSER_ID:
            return
        for r in self:
            if r.protected:
                raise exceptions.Warning(
                    _("The Rule is protected. You don't have access for this operation")
                )

    @api.multi
    def write(self, vals):
        self.check_restricted()
        return super(IRRule, self).write(vals)

    @api.multi
    def unlink(self):
        self.check_restricted()
        return super(IRRule, self).unlink()


class Module(models.Model):
    _inherit = "ir.module.module"

    @api.multi
    def button_uninstall(self):
        for r in self:
            if r.name == MODULE_NAME and self.env.uid != SUPERUSER_ID:
                raise exceptions.Warning(_("Only admin can uninstall the module"))
        return super(Module, self).button_uninstall()
