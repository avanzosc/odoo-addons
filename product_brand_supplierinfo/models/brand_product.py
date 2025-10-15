# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class BrandProduct(models.Model):
    _name = "brand.product"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin", "utm.mixin"]
    _description = "Product Brands"

    name = fields.Char(string="Description", required=True, copy=False)
    product_tmpl_id = fields.Many2one(
        string="Product", comodel_name="product.template", copy=False
    )
    brand_id = fields.Many2one(
        string="Product Brand", comodel_name="product.brand", copy=False
    )
    brand_code = fields.Char(copy=False)
    homologation_date = fields.Date(copy=False)
    dehomologation_date = fields.Date(copy=False)
    responsible_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        copy=False,
        default=lambda self: self.env.user,
    )
    state = fields.Selection(
        selection=[
            ("homologation", "Homologation"),
            ("dehomologation", "Dehomologation"),
        ],
        string="Status",
        copy=False,
    )
    dehomologation_reason = fields.Text(copy=False)
    marking = fields.Char(copy=False)
    footprint_id = fields.Many2one(
        string="Footprint", comodel_name="brand.product.footprint", copy=False
    )
    observations = fields.Text(copy=False)

    @api.onchange("product_tmpl_id", "brand_id")
    def onchange_claim_description(self):
        if self.product_tmpl_id and self.brand_id:
            self.name = ("%(product_code)s-%(brand_name)s") % {
                "product_code": self.product_tmpl_id.default_code,
                "brand_name": self.brand_id.name,
            }
        elif self.product_tmpl_id:
            self.name = self.product_tmpl_id.default_code
        elif self.brand_id:
            self.name = self.brand_id.name
        else:
            self.name = ""

    def action_set_homologation(self):
        self.write(
            {
                "state": "homologation",
                "homologation_date": fields.Date.context_today(self),
                "dehomologation_reason": "",
                "dehomologation_date": False,
            }
        )

    def action_set_dehomologation(self):
        if self.dehomologation_reason:
            self.write(
                {
                    "state": "dehomologation",
                    "dehomologation_date": fields.Date.context_today(self),
                }
            )
        else:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "product_brand_supplierinfo.action_wizard_dehomologation_reason"
            )
            return action

    def name_get(self):
        result = []
        for record in self:
            name = record.name or ""
            code = record.brand_code or ""
            if code:
                name = "[%s] %s" % (code, name)
            result.append((record.id, name))
        return result

    def write(self, vals):
        if "state" in vals:
            message = _("%(old_state)s --> %(new_state)s") % {
                "old_state": self.state,
                "new_state": vals.get("state"),
            }
            if vals.get("state", "") == "homologation":
                message = _(
                    "%(old_message)s, homologation date: %(homologation_date)s"
                ) % {
                    "old_message": message,
                    "homologation_date": vals.get("homologation_date"),
                }

            if vals.get("state", "") == "dehomologation":
                message = _(
                    "%(old_message)s, dehomologation date: "
                    "%(deshomologation_date)s: %(dehomologation_reason)s"
                ) % {
                    "old_message": message,
                    "deshomologation_date": vals.get("dehomologation_date"),
                    "dehomologation_reason": vals.get("dehomologation_reason"),
                }
        else:
            if "homologation_date" in vals:
                message = _("Homologation Date Changed To: %(homologation_date)s") % {
                    "homologation_date": vals.get("homologation_date"),
                }
            if "dehomologation_date" in vals:
                message = _(
                    "Dehomologation Date Changed To: %(dehomologation_date)s"
                ) % {
                    "dehomologation_date": vals.get("dehomologation_date"),
                }
        result = super().write(vals)
        if (
            "state" in vals
            or "homologation_date" in vals
            or "dehomologation_date" in vals
        ):
            self.message_post(body=message)
        return result
