from odoo import api, models, tools


class IrModelAccess(models.Model):
    """Inherits the ir model access for restricting
    the user from accessing data."""

    _inherit = "ir.model.access"

    @api.model
    @tools.ormcache_context(
        "self.env.uid",
        "self.env.su",
        "model",
        "mode",
        "raise_exception",
        keys=("lang",),
    )
    def check(self, model, mode, raise_exception=True):
        """Overrides the default check method to allow
        only read access to the user."""
        res = super().check(model, mode, raise_exception=raise_exception)
        if self.env.user.has_group(
            "res_groups_readonly_user.group_users_readonly"
        ) and mode in ("write", "create", "unlink"):
            return False
        return res
