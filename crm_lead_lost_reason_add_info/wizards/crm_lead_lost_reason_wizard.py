from odoo import api, fields, models


class CrmLeadLostReasonWizard(models.TransientModel):
    _inherit = "crm.lead.lost"

    competitor_manufacturer_id = fields.Many2one(
        "res.partner",
        string="Competitor Manufacturer",
        domain=[("is_company", "=", True)],
    )
    competitor_integrator_id = fields.Many2one(
        "res.partner",
        string="Competitor Integrator",
        domain=[("is_company", "=", True)],
    )
    competitor_reseller_id = fields.Many2one(
        "res.partner",
        string="Competitor Reseller",
        domain=[("is_company", "=", True)],
    )
    competitor_price = fields.Float()
    lost_reason_notes = fields.Text()

    @api.model
    def default_get(self, fields):
        res = super(CrmLeadLostReasonWizard, self).default_get(fields)
        lead = self.env["crm.lead"].browse(self.env.context.get("active_id"))
        res.update(
            {
                "competitor_manufacturer_id": lead.competitor_manufacturer_id.id,
                "competitor_integrator_id": lead.competitor_integrator_id.id,
                "competitor_reseller_id": lead.competitor_reseller_id.id,
                "competitor_price": lead.competitor_price,
                "lost_reason_notes": lead.lost_reason_notes,
            }
        )
        return res

    def action_lost_reason_apply(self):
        """
        Applies the lost reason and updates the lead with additional fields.
        """
        res = super(CrmLeadLostReasonWizard, self).action_lost_reason_apply()
        lead = self.env["crm.lead"].browse(self.env.context.get("active_id"))
        lead.write(
            {
                "competitor_manufacturer_id": self.competitor_manufacturer_id.id,
                "competitor_integrator_id": self.competitor_integrator_id.id,
                "competitor_reseller_id": self.competitor_reseller_id.id,
                "competitor_price": self.competitor_price,
                "lost_reason_notes": self.lost_reason_notes,
            }
        )
        return res
