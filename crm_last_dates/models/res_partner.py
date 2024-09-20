from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    last_lead_date = fields.Datetime(
        compute="_compute_last_dates",
        store=True,
    )
    last_meeting_date = fields.Datetime(
        compute="_compute_last_dates",
        store=True,
    )
    last_invoice_date = fields.Datetime(
        compute="_compute_last_dates",
        store=True,
    )

    @api.depends("commercial_partner_id")
    def _compute_last_dates(self):
        for partner in self:
            lead = self.env["crm.lead"].search(
                [("partner_id", "=", partner.commercial_partner_id.id)],
                order="create_date desc",
                limit=1,
            )
            partner.last_lead_date = lead.create_date if lead else False

            meeting = self.env["calendar.event"].search(
                [("partner_ids", "in", partner.commercial_partner_id.id)],
                order="create_date desc",
                limit=1,
            )
            partner.last_meeting_date = meeting.create_date if meeting else False

            invoice = self.env["account.move"].search(
                [
                    ("partner_id", "=", partner.commercial_partner_id.id),
                    ("move_type", "=", "out_invoice"),
                ],
                order="invoice_date desc",
                limit=1,
            )
            partner.last_invoice_date = invoice.invoice_date if invoice else False
