# Copyright 2023 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    state = fields.Selection(
        [("red", _("Red")), ("green", _("Green"))], string="Status",
        compute="_compute_state"
    )
    contracting_company_id = fields.Many2one(
        string="Contracting company", comodel_name="res.partner", copy=False
    )
    document_type = fields.Selection(
        [("admin", _("Administrative")),
         ("worker", _("Worker")),
         ("machinery", _("Machinery"))], string="Document type", copy=False
    )
    worker_id = fields.Many2one(
        string="Worker", comodel_name="res.partner", copy=False
    )
    machinery = fields.Text(
        string="Machinery", copy=False)
    revision = fields.Selection(
        [("to_review", _("To review")), ("reviewed", _("Reviewed"))],
        string="Revision", copy=False
    )
    date_request = fields.Date(
        string="Date request", copy=False
    )
    expiration_date = fields.Date(
        string="Expiration date", copy=False
    )
    is_prl = fields.Boolean(
        string="Is PRL", default=False, copy=False)

    def _compute_state(self):
        for file in self:
            color = "green"
            if (file.expiration_date and
                    file.expiration_date > fields.Date.context_today(self)):
                color = "red"
            file.state = color

    @api.model_create_multi
    def create(self, vals_list):
        if "default_is_prl" not in self.env.context:
            return super(IrAttachment, self).create(vals_list)
        for vals in vals_list:
            vals["res_model"] = "res.partner"
            if "is_prl" in vals and vals.get("is_prl", False):
                if ("document_type" in vals and "worker_id" in vals
                    and vals.get("document_type") == "worker" and
                        vals.get("worker_id", False)):
                    partner_id = vals.get("worker_id")
                else:
                    partner_id = vals.get("contracting_company_id")
                partner = self.env["res.partner"].browse(partner_id)
                vals.update({"res_id": partner.id,
                             "res_name": partner.name})
        attachments = super(IrAttachment, self).create(vals_list)
        return attachments
