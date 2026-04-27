# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Machine(models.Model):
    _name = "machine"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Holds Machine Records"

    name = fields.Char(string="Machine Name", required=True)
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company.id,
    )
    year = fields.Char()
    model = fields.Char()
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Associated product",
        domain="[('machine_ok','=',True), ('tracking','=','serial')]",
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
        selection=[
            ("active", "Active"),
            ("inactive", "InActive"),
            ("outofservice", "Out of Service"),
        ],
        required=True,
        default="active",
    )
    ownership = fields.Selection(
        selection=[
            ("own", "Own"),
            ("lease", "Lease"),
            ("rental", "Rental"),
        ],
        default="own",
        required=True,
    )
    enrolldate = fields.Date(
        string="Enrollment date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )
    ambit = fields.Selection(
        selection=[
            ("local", "Local"),
            ("national", "National"),
            ("international", "International"),
        ],
        default="local",
    )
    card = fields.Char()
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

    @api.constrains("product_id")
    def _check_product_tracking(self):
        for machine in self:
            if machine.product_id and machine.product_id.tracking != "serial":
                raise ValidationError(
                    _(
                        "Product '%s' must have serial number tracking "
                        "to be used as a machine."
                    )
                    % machine.product_id.display_name
                )
