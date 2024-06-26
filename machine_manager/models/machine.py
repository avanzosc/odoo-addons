# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class Machine(models.Model):
    _name = "machine"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Holds Machine Records"

    def _def_company(self):
        return self.env.user.company_id.id

    name = fields.Char(string="Machine Name", required=True)
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=_def_company,
    )
    year = fields.Char(string="Year")
    model = fields.Char(string="Model")
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Associated product",
        help="This product will contain information about the machine such as"
        " the manufacturer.",
    )
    serial_id = fields.Many2one(
        comodel_name="stock.lot",
        string="Product Serial #",
        domain="[('product_id', '=', product_id)]",
    )
    model_type_id = fields.Many2one(string="Type", comodel_name="machine.model")
    status = fields.Selection(
        string="Status",
        selection=[
            ("active", "Active"),
            ("inactive", "InActive"),
            ("outofservice", "Out of Service"),
        ],
        required=True,
        default="active",
    )
    ownership = fields.Selection(
        string="Ownership",
        selection=[("own", "Own"), ("lease", "Lease"), ("rental", "Rental")],
        default="own",
        required=True,
    )
    enrolldate = fields.Date(
        string="Enrollment date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )
    ambit = fields.Selection(
        string="Ambit",
        selection=[
            ("local", "Local"),
            ("national", "National"),
            ("international", "International"),
        ],
        default="local",
    )
    card = fields.Char(string="Card")
    cardexp = fields.Date(string="Card Expiration")
    frame = fields.Char(string="Frame Number")
    phone = fields.Char(string="Phone number")
    mac = fields.Char(string="MAC Address")
    insurance = fields.Char(string="Insurance Name")
    policy = fields.Char(string="Machine policy")
    power = fields.Char(string="Power (Kw)")
    product_categ_id = fields.Many2one(
        string="Internal category",
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
    )
