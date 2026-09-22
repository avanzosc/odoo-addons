# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    make_saleperson_ids = fields.One2many(
        string="Makes / Salesperson",
        inverse_name="partner_id",
        comodel_name="res.partner.make.saleperson",
    )
    make_logo = fields.Binary("Logo make", compute="_compute_logo_to_print")
    account_move_line_ids = fields.One2many(
        string="Account move lines",
        comodel_name="account.move.line",
        inverse_name="partner_id",
        domain=[
            ("journal_type", "=", "sale"),
            ("invoice_state", "=", "paid"),
            ("invoice_type", "in", ("out_invoice", "out_refund")),
        ],
    )
    make_amount_ids = fields.Many2many(
        comodel_name="make.amount",
        relation="rel_partner_make_amount",
        column1="partner_id",
        column2="make_amount_id",
        string="Make amount",
        copy=False,
        store=True,
        compute="_compute_make_amount_ids",
    )
    tariff_id = fields.Many2one(string="Tariff", comodel_name="product.pricelist")
    relation_id = fields.Many2one(
        string="Relation", comodel_name="res.partner.relation"
    )
    classification_id = fields.Many2one(
        string="Classification", comodel_name="res.partner.classification"
    )
    market_id = fields.Many2one(string="Market", comodel_name="res.partner.market")
    market_sector_id = fields.Many2one(
        string="Market sector", comodel_name="res.partner.market.sector"
    )

    _track = {
        "tariff_id": {"create": "field_update", "write": "field_update"},
    }

    @api.depends(
        "account_move_line_ids",
        "account_move_line_ids.invoice_state",
        "account_move_line_ids.make_ids",
        "account_move_line_ids.debit",
        "account_move_line_ids.credit",
    )
    def _compute_make_amount_ids(self):
        for partner in self:
            my_partner = str(partner)
            if "NewId object" not in my_partner:
                self._cr.execute(
                    "DELETE FROM rel_partner_make_amount WHERE partner_id=%s",
                    (partner.id,),
                )
                self._cr.execute(
                    "DELETE FROM make_amount WHERE partner_id=%s", (partner.id,)
                )
                partner.make_amount_ids.unlink()
                makes = partner.account_move_line_ids.mapped("make_ids")
                users = partner.account_move_line_ids.mapped("move_id.user_id")
                values = []
                for make in makes:
                    for user in users:
                        imp = 0
                        lines = partner.account_move_line_ids.filtered(
                            lambda c, current_make=make, current_user=user: (
                                current_make in c.make_ids
                                and c.move_id.user_id == current_user
                            )
                        )
                        if lines:
                            imp_positive = sum([x.credit for x in lines])
                            imp_negative = sum([x.debit for x in lines])
                            imp = imp_positive - imp_negative
                            vals = {
                                "company_id": self.env.user.company_id.id,
                                "partner_id": partner.id,
                                "commercial_id": user.id,
                                "make_id": make.id,
                                "debit": imp,
                            }
                            if partner.sale_warn == "warning" and partner.sale_warn_msg:
                                vals["sale_warn_msg"] = partner.sale_warn_msg
                            if partner.category_id:
                                vals["category_ids"] = [(6, 0, partner.category_id.ids)]
                            values.append((0, 0, vals))
                partner.make_amount_ids = values

    def _compute_logo_to_print(self):
        make_obj = self.env["product.make"]
        for partner in self:
            makes = partner.make_saleperson_ids.mapped("make_id")
            search_default_logo = False
            if len(makes) == 1:
                if makes.logo:
                    partner.make_logo = makes.logo
                else:
                    search_default_logo = True
            if len(makes) == 2:
                makes2 = make_obj
                lines = partner.make_saleperson_ids.filtered(
                    lambda x: x.make_id and x.make_id.common_logo
                )
                if lines:
                    makes2 |= lines.mapped("make_id") - makes2
                if len(makes2) == 2:
                    partner.make_logo = makes2[0].common_logo
                else:
                    search_default_logo = True
            if len(makes) == 0 or len(makes) > 3 or search_default_logo:
                cond = [("use_logo", "=", True)]
                make = make_obj.search(cond, limit=1)
                partner.make_logo = make.logo if make else self.env.user.company_id.logo

    def get_partner_makes_info(self):
        commercial_make_id = False
        allowed_commercial_make_ids = [(6, 0, [])]
        num_allowed_commercial_make = 0
        partner = self if not self.parent_id else self.parent_id
        if partner.make_saleperson_ids:
            makes = partner.make_saleperson_ids.mapped("make_id")
            if len(makes) == 1:
                commercial_make_id = makes.id
            allowed_commercial_make_ids = [(6, 0, makes.ids)]
            num_allowed_commercial_make = len(makes)
        vals = {
            "commercial_make_id": commercial_make_id,
            "allowed_commercial_make_ids": allowed_commercial_make_ids,
            "num_allowed_commercial_make": num_allowed_commercial_make,
        }
        return vals

    @api.model
    def load_tariff(self):
        partners = self.env["res.partner"].search([])
        count = 0
        for partner in partners:
            count += 1
            vals = {}
            if (
                not partner.prospect
                and partner.company_type == "company"
                and not partner.email
            ):
                vals["email"] = _("You must enter company email")
            if partner.property_product_pricelist:
                vals["tariff_id"] = partner.property_product_pricelist.id
            if vals:
                partner.write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "property_product_pricelist" in vals and vals.get(
                "property_product_pricelist", False
            ):
                vals["tariff_id"] = vals.get("property_product_pricelist")
        return super().create(vals_list)
