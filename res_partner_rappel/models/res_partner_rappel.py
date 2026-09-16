# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerRappel(models.Model):
    _name = "res.partner.rappel"
    _description = "Contact Rappel"

    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner")
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    percentage = fields.Float(string="Rappel")
    period = fields.Selection(
        selection=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("annual", "Annual"),
        ]
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company.id,
        required=True,
    )

    @api.constrains("partner_id", "product_id", "company_id")
    def _check_partner_rappels(self):
        for rappel in self:
            if rappel.company_id and rappel.partner_id:
                rappels_no_product = self.env["res.partner.rappel"].search(
                    [
                        ("company_id", "=", rappel.company_id.id),
                        ("partner_id", "=", rappel.partner_id.id),
                        ("product_id", "=", False),
                    ]
                )
                rappels_with_product = self.env["res.partner.rappel"].search(
                    [
                        ("company_id", "=", rappel.company_id.id),
                        ("partner_id", "=", rappel.partner_id.id),
                        ("product_id", "!=", False),
                    ]
                )
                if len(rappels_no_product) > 1:
                    raise ValidationError(
                        _("One rappel line without product per customer.")
                    )
                if rappels_no_product and rappels_with_product:
                    raise ValidationError(
                        _(
                            "There cannot be rappels with product and "
                            + "without product at the same time."
                        )
                    )
