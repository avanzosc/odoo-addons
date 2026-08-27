from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
    )

    @api.model_create_multi
    def create(self, vals_list):
        cleaned = []
        for vals in vals_list:
            v = dict(vals)
            if (
                not self.env.context.get("force_mo_package_partner")
                and v.get("partner_id")
                and self.env.context.get("active_model") == "stock.picking"
            ):
                picking = self.env["stock.picking"].browse(
                    self.env.context.get("active_id")
                )
                if picking.exists() and picking.picking_type_code == "incoming":
                    v.pop("partner_id", None)
            cleaned.append(v)
        return super().create(cleaned)
