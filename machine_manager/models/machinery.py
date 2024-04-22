# -*- coding: utf-8 -*-
# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.addons import decimal_precision as dp
from odoo import models, fields, _


class Machinery(models.Model):
    _name = "machinery"
    _description = "Holds records of Machines"

    def _def_company(self):
        return self.env.user.company_id.id

    name = fields.Char(
        string="Machine Name", required=True
    )
    company_id = fields.Many2one(
        string="Company", comodel_name="res.company", required=True,
        default=_def_company
    )
    assetacc_id = fields.Many2one(
        string="Asset Account", comodel_name="account.account"
    )
    depracc_id = fields.Many2one(
        string="Depreciation Account", comodel_name="account.account"
    )
    year = fields.Char(
        string="Year"
    )
    model = fields.Char(
        string="Model"
    )
    product_id = fields.Many2one(
        comodel_name="product.product", string="Associated product",
        help="This product will contain information about the machine such as"
        " the manufacturer."
    )
    manufacturer_id = fields.Many2one(
        comodel_name="res.partner", related="product_id.manufacturer_id",
        readonly=True, help="Manufacturer is related to the associated product"
        " defined for the machine.", store=True
    )
    serial_char = fields.Char(
        string="Product Serial #"
    )
    serial_id = fields.Many2one(
        comodel_name="stock.lot", string="Product Serial #",
        domain="[('product_id', '=', product_id)]"
    )
    model_type_id = fields.Many2one(
        string="Type", comodel_name="machine.model"
    )
    status = fields.Selection(
        string="Status",
        selection=[("active", "Active"),
                   ("inactive", "InActive"),
                   ("outofservice", "Out of Service")],
        required=True, default="active"
    )
    ownership = fields.Selection(
        string="Ownership",
        selection=[("own", "Own"),
                   ("lease", "Lease"),
                   ("rental", "Rental")],
        default="own", required=True
    )
    bcyl = fields.Float(
        string="Base Cycles", digits=(16, 3), help="Last recorded cycles",
        default=0.0
    )
    bdate = fields.Date(
        string="Record Date", help="Date on which the cycles is recorded"
    )
    purch_date = fields.Date(
        string="Purchase Date", help="Machine's date of purchase"
    )
    purch_cost = fields.Float(
        string="Purchase Value", digits=(16, 2), default=0.0
    )
    purch_partner_id = fields.Many2one(
        string="Purchased From", comodel_name="res.partner"
    )
    purch_inv_id = fields.Many2one(
        string="Purchase Invoice", comodel_name="account.move"
    )
    purch_cycles = fields.Integer(
        string="Cycles at Purchase", default=0
    )
    actcycles = fields.Integer(
        string="Actual Cycles", default=0
    )
    deprecperc = fields.Float(
        string="Depreciation in %", digits=(10, 2), default=0.0
    )
    deprecperiod = fields.Selection(
        string="Depr. period",
        selection=[("monthly", "Monthly"),
                   ("quarterly", "Quarterly"),
                   ("halfyearly", "Half Yearly"),
                   ("annual", "Yearly")],
        default="annual", required=True
    )
    primarymeter = fields.Selection(
        string="Primary Meter",
        selection=[("calendar", "Calendar"),
                   ("cycles", "Cycles"),
                   ("hourmeter", "Hour Meter")],
        default="cycles", required=True
    )
    warrexp = fields.Date(
        string="Date", help="Expiry date for warranty of product"
    )
    warrexpcy = fields.Integer(
        string="(or) cycles", help="Expiry cycles for warranty of product",
        default=0
    )
    location_id = fields.Many2one(
        string="Stk Location", comodel_name="stock.location",
        help="This association is necessary if you want to make repair orders "
        "with the machine"
    )
    enrolldate = fields.Date(
        string="Enrollment date", required=True,
        default=lambda self: fields.Date.context_today(self)
    )
    ambit = fields.Selection(
        string="Ambit",
        selection=[("local", "Local"),
                   ("national", "National"),
                   ("international", "International")],
        default="local"
    )
    card = fields.Char(
        string="Card"
    )
    cardexp = fields.Date(
        string="Card Expiration"
    )
    frame = fields.Char(
        string="Frame Number"
    )
    phone = fields.Char(
        string="Phone number"
    )
    mac = fields.Char(
        string="MAC Address"
    )
    insurance = fields.Char(
        string="Insurance Name"
    )
    policy = fields.Char(
        string="Machine policy"
    )
    user_ids = fields.One2many(
        string="Machine Users", comodel_name="machinery.users",
        inverse_name="machine_id"
    )
    power = fields.Char(
        string="Power (Kw)"
    )
    product_categ_id = fields.Many2one(
        string="Internal category", comodel_name="product.category",
        related='product_id.categ_id', store=True
    )
    salvage_value = fields.Float(
        string="Salvage Value",
        digits=dp.get_precision('Product Price'), default=0.0
    )


class MachineryUsers(models.Model):
    _name = "machinery.users"
    _description = "Machine users"

    m_user_id = fields.Many2one(
        string="User", comodel_name="res.users"
    )
    machine_id = fields.Many2one(
        string="Machine", comodel_name="machinery"
    )
    start_date = fields.Date(
        string="Homologation Start Date"
    )
    end_date = fields.Date(
        string="Homologation End Date"
    )

    _sql_constraints = [
        ("uniq_machine_user", "unique(machine_id, m_user_id)",
         _("User already defined for the machine"))
    ]
