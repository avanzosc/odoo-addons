from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    inactive_leads_count = fields.Integer(
        "Inactive Leads Count",
        compute="_compute_inactive_leads_count",
    )

    def _get_inactive_leads_domain(self):
        """Returns the domain to filter inactive leads for\
            the current partner or commercial partner."""
        self.ensure_one()
        return [
            "|",
            ("partner_id.commercial_partner_id", "=", self.commercial_partner_id.id),
            ("partner_id", "=", self.id),
            ("active", "=", False),
        ]

    def action_view_inactive_leads(self):
        """Returns an action to view inactive leads associated with the partner\
            or commercial partner."""
        self.ensure_one()
        action = self.env.ref("crm.crm_lead_all_leads").read()[0]
        action["domain"] = self._get_inactive_leads_domain()
        action["context"] = dict(self.env.context, default_partner_id=self.id)
        return action

    @api.depends("child_ids")
    def _compute_inactive_leads_count(self):
        """Compute the count of inactive leads for each partner."""
        Lead = self.env["crm.lead"]
        for partner in self:
            partner.inactive_leads_count = Lead.search_count(
                partner._get_inactive_leads_domain()
            )
