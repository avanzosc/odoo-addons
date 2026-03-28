from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    date_from = fields.Date(required=True, string="From")
    date_to = fields.Date(required=True, string="To")

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError(
                    _("The 'From' date cannot be later than the 'To' date.")
                )
