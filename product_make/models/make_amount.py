# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class MakeAmount(models.Model):
    _name = "make.amount"
    _description = "Amount by make"
    _order = "company_id, partner_name"

    company_id = fields.Many2one(string="Company", comodel_name="res.company")
    partner_id = fields.Many2one(string="Customer", comodel_name="res.partner")
    partner_name = fields.Char(
        string="Customer name", related="partner_id.name", store=True
    )
    partner_state_id = fields.Many2one(
        string="State",
        comodel_name="res.country.state",
        related="partner_id.state_id",
        store=True,
    )
    make_id = fields.Many2one(string="Make", comodel_name="product.make")
    commercial_id = fields.Many2one(string="Commercial", comodel_name="res.users")
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="company_id.currency_id",
        string="Company Currency",
        readonly=True,
        store=True,
    )
    debit = fields.Monetary(
        string="Amount", default=0.0, currency_field="company_currency_id"
    )
    purchase_group_id = fields.Many2one(
        comodel_name="res.partner.purchase_group",
        string="Purchase group",
        related="partner_id.purchase_group_id",
        store=True,
    )
    sale_warn_msg = fields.Text(string="Message for Sales Order")
    category_ids = fields.Many2many(
        comodel_name="res.partner.category",
        column1="make_amount_id",
        column2="category_id",
        string="Tags",
    )
    tariff_id = fields.Many2one(
        string="Tariff",
        comodel_name="product.pricelist",
        related="partner_id.tariff_id",
        store=True,
    )
    relation_id = fields.Many2one(
        string="Relation",
        comodel_name="res.partner.relation",
        related="partner_id.relation_id",
        store=True,
    )
    classification_id = fields.Many2one(
        string="Classification",
        comodel_name="res.partner.classification",
        related="partner_id.classification_id",
        store=True,
    )
