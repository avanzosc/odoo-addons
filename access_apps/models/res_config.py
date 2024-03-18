# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.model
    def _install_modules(self, modules):
        if self.env["res.users"].has_group(
            "access_apps.group_allow_apps_only_from_settings"
        ):
            self = self.sudo()

        return super(ResConfigSettings, self)._install_modules(modules)

    @api.model
    def default_get(self, fields):
        # We restricted any access to apps by default (`ir.module.module`) but in `website_sale` module configuration
        # there is a field that gets its default value by searching in apps.
        # Without this there is a possibility to encounter the `Access Error` when trying to open settings
        # - e.g. when administrators without access to apps open ``[[ Website Admin ]] >> Configuration >> Settings``

        # TODO: this solution may lead to unexpected result
        # if some of default methods uses self self.env.user to compute default value
        res = super(ResConfigSettings, self.sudo()).default_get(fields)

        # modules: which modules are installed/to install
        classified = self._get_classified_fields()
        for name, module in classified["to_uninstall"]:
            res[name] = module.state in ("installed", "to install", "to upgrade")
            if self._fields[name].type == "selection":
                res[name] = int(res[name])

        return res

    @api.model
    def _get_classified_fields(self):
        # classify mudules to install and uninstall independently
        res = super(ResConfigSettings, self)._get_classified_fields()

        to_uninstall_modules = []

        for name, module in res["module"]:
            if not self[name]:
                if module and module.state in ("installed", "to upgrade"):
                    to_uninstall_modules.append((name, module))

        modules = list(set(res["module"]).difference(set(to_uninstall_modules)))

        res["module"] = modules
        res["to_uninstall"] = to_uninstall_modules

        return res

    @api.multi
    def execute(self):
        # base `exectute` doesn't know about new classification - it only has a list of modules to install now
        res = super(ResConfigSettings, self).execute()
        # uninstall modules if needed and a user has access
        to_uninstall = self._get_classified_fields()["to_uninstall"]
        if to_uninstall and self.env["res.users"].has_group(
            "access_apps.group_allow_apps_only_from_settings"
        ):
            to_uninstall_modules = self.env["ir.module.module"]
            for _name, module in to_uninstall:
                to_uninstall_modules += module
            to_uninstall_modules.sudo().button_immediate_uninstall()
        return res
