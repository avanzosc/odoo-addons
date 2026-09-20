# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    supplier_industry_id = fields.Many2one(
        string="Supplier sector",
        related="partner_id.industry_id",
        readonly=True,
        store=True,
        copy=False,
    )
    supplier_principal_activity_id = fields.Many2one(
        string="Supplier Principal Activity",
        comodel_name="principal.activity",
        related="partner_id.principal_activity_id",
        store=True,
        readonly=True,
        copy=False,
    )
    province_id = fields.Many2one(
        string="Province",
        comodel_name="res.country.state",
        related="partner_id.state_id",
        store=True,
        readonly=True,
        copy=False,
    )
    zip = fields.Char(
        string="Zip Code",
        related="partner_id.zip",
        store=True,
        readonly=True,
        copy=False,
    )
    interest_id = fields.Many2one(
        string="Interest",
        comodel_name="res.partner.interes",
        related="partner_id.interest_id",
        store=True,
        readonly=True,
        copy=False,
    )
    flowserve_manager_id = fields.Many2one(
        string="*Flowserve Manager",
        comodel_name="responsable.flowserv",
        related="partner_id.flowserve_manager_id",
        store=True,
        readonly=True,
        copy=False,
    )
