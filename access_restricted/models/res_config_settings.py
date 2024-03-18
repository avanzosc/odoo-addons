from odoo import SUPERUSER_ID, api, models
from odoo.tools import ustr
from odoo.tools.translate import _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.model
    def _get_classified_fields(self):
        uid = self.env.uid
        classified = super(ResConfigSettings, self)._get_classified_fields()
        if uid == SUPERUSER_ID:
            return classified

        group = []
        ResUsers = self.env["res.users"]
        for name, groups, implied_group in classified["group"]:
            if ResUsers.search_count(
                [("id", "=", uid), ("groups_id", "in", [implied_group.id])]
            ) or ResUsers.has_group(
                "access_restricted.group_allow_add_implied_from_settings"
            ):
                group.append((name, groups, implied_group))
        classified["group"] = group
        return classified

    @api.model
    def fields_get(self, fields=None, **kwargs):
        uid = self.env.uid
        fields = super(ResConfigSettings, self).fields_get(fields, **kwargs)

        if uid == SUPERUSER_ID:
            return fields

        for name in fields:
            if not name.startswith("group_"):
                continue
            f = self._fields[name]
            ResUsers = self.env["res.users"]
            if ResUsers.has_group(f.implied_group) or ResUsers.has_group(
                "access_restricted.group_allow_add_implied_from_settings"
            ):
                continue

            fields[name].update(
                readonly=True,
                help=ustr(fields[name].get("help", ""))
                + _(
                    "\n\nYou don't have access to change this settings, because you administration rights are restricted"
                ),
            )
        return fields

    @api.multi
    def execute(self):
        res = super(ResConfigSettings, self.with_context({"config": self})).execute()
        return res
