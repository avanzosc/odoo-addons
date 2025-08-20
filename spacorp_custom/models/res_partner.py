# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("agent_ids", "agent_ids.agent", "agent_ids.active")
    def _compute_agents_count(self):
        for partner in self:
            partner.agents_count = len(
                partner.agent_ids.filtered(lambda x: x.agent and x.active)
            )

    contact_person = fields.Char(string="Accounting Contact")
    market_id = fields.Many2one(string="Market", comodel_name="res.partner.market")
    market_sector_id = fields.Many2one(
        string="Market sector", comodel_name="res.partner.market.sector"
    )

    state_id = fields.Many2one(string="Province")

    parent_is_customer = fields.Boolean(
        string="Parent is customer", compute="_compute_parent_is_customer", store=True
    )
    agents_count = fields.Integer(
        string="Num. agents", compute="_compute_agents_count", store=True
    )
    show_chatter = fields.Boolean(
        string="Show chatter", compute="_compute_show_chatter"
    )

    @api.depends("parent_id", "parent_id.customer_rank")
    def _compute_parent_is_customer(self):
        for partner in self:
            partner.parent_is_customer = bool(partner.parent_id.customer_rank)

    def _compute_show_chatter(self):
        group = self.env.ref("spacorp_custom.group_view_all_partner_form")
        for partner in self:
            partner.show_chatter = self.env.user in group.users

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("company_type") == "company":
                if "city" not in vals or not vals.get("city", False):
                    raise exceptions.ValidationError(_("You must enter the city"))
        partners = super().create(vals)
        for partner in partners.filtered(
            lambda x: x.company_type == "company" and x.customer_rank > 0
        ):
            if not partner.child_ids and "from_duplicate" not in self.env.context:
                raise exceptions.ValidationError(_("You must enter one contact"))
            contact = partner.child_ids.filtered(
                lambda x: x.type and x.type == "contact"
            )
            if not contact and "from_duplicate" not in self.env.context:
                raise exceptions.ValidationError(_("You must enter one contact"))
            if (
                not partner.make_saleperson_ids
                and "from_duplicate" not in self.env.context
            ):
                raise exceptions.ValidationError(
                    _("You must enter one make/saleperson")
                )
        return partners

    def copy(self, default=None):
        self.ensure_one()
        return super(ResPartner, self.with_context(from_duplicate=True)).copy(default)

    def write(self, vals):
        for partner in self:
            if (
                partner.supplier_rank > 1
                and partner.company_type == "company"
                and not partner.email
                and "email" not in vals
            ):
                raise exceptions.ValidationError(_("You must enter company email"))
        if "type" in vals and not vals.get("type", False):
            vals.pop("type")
        if "property_product_pricelist" in vals and vals.get(
            "property_product_pricelist", False
        ):
            vals["tariff_id"] = vals.get("property_product_pricelist")
        return super().write(vals)

    def create_user_from_contact(self):
        user_obj = self.env["res.users"]
        cond = [("is_agent", "=", True)]
        agent_user = user_obj.search(cond, limit=1)
        cond = [("partner_id", "=", self.id)]
        user = user_obj.search(cond)
        if not user:
            vals = {"name": self.name, "login": "poner@login.es", "partner_id": self.id}
            if self.email:
                vals["login"] = self.email
            if agent_user:
                agent_user.copy(vals)
            else:
                user_obj.create(vals)
