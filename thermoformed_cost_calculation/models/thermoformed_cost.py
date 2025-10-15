# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ThermoformedCost(models.Model):
    _name = "thermoformed.cost"
    _description = "Thermoformed Cost"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    state = fields.Selection(
        selection=[("draft", "Draft"), ("closed", "Closed")],
        string="Status",
        default="draft",
        copy=False,
    )
    code = fields.Char(string="Reference", copy=False)
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
    )
    description = fields.Char()
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
    )
    workcenter_id = fields.Many2one(
        string="Work center",
        comodel_name="mrp.workcenter",
    )
    frame_id = fields.Many2one(
        string="Frame",
        comodel_name="frame",
    )
    product_id = fields.Many2one(
        string="Material",
        comodel_name="product.template",
    )
    serie = fields.Integer(
        string="Series",
        default=10000,
    )
    figure = fields.Integer(
        default=1,
    )
    adjustment_plates = fields.Integer(
        default=100,
    )
    width = fields.Float()
    step = fields.Float()
    thickness = fields.Float()
    density = fields.Float()
    plate_weight = fields.Float(
        compute="_compute_weight",
        digits="Stock Weight",
        store=True,
    )
    serie_weight = fields.Float(
        compute="_compute_weight",
        digits="Stock Weight",
        store=True,
    )
    amount = fields.Float(
        compute="_compute_amount",
        digits="Price Unit",
    )
    commission = fields.Float(
        default=1,
        digits="Discount",
    )
    commission_amount = fields.Float(
        compute="_compute_margin_commission",
        digits="Product Price",
        store=True,
    )
    margin_purchase = fields.Float(
        string="Default Purchase Margin",
    )
    value_added_margin = fields.Float(
        string="Default Value Added Margin",
    )
    unit_retail_price = fields.Float(
        digits="Product Price",
    )
    margin = fields.Float(
        compute="_compute_margin_commission",
        store=True,
    )
    plate_hour = fields.Integer(
        string="Plates in hour",
        default=1,
    )
    assembly = fields.Float()
    operator = fields.Float(
        string="Operators",
        default=1.0,
    )
    material_cost = fields.Float(
        string="Material Cost Price",
        digits="Product Price",
    )
    workcenter_cost = fields.Float(
        digits="Product Price",
    )
    operator_cost = fields.Float(
        digits="Product Price",
    )
    mechanic_cost = fields.Float(
        digits="Product Price",
    )
    plate_cost = fields.Float(
        string="Plate's cost",
        compute="_compute_plate_costs",
        digits="Product Price",
    )
    manufacturing_cost_unit = fields.Float(
        string="Manufacturing Cost per Unit",
        compute="_compute_costs_unit",
        digits="Product Price",
        store=True,
    )
    assembly_cost = fields.Float(
        compute="_compute_assembly_cost",
        digits="Product Price",
    )
    assembly_cost_unit = fields.Float(
        string="Assembly Cost per Unit",
        compute="_compute_assembly_cost",
        digits="Product Price",
    )
    box_id = fields.Many2one(
        string="Box reference",
        comodel_name="product.template",
    )
    box_quantity = fields.Integer(
        string="Plates per Box",
        default=1,
    )
    pallet_id = fields.Many2one(
        string="Pallet Reference",
        comodel_name="product.template",
    )
    box_pallet = fields.Integer(
        string="Box per Pallet",
        default=16,
    )
    box_cost = fields.Float(
        digits="Product Price",
    )
    pallet_cost = fields.Float(
        digits="Product Price",
    )
    pallet_transport_cost = fields.Float(
        default=40,
        digits="Product Price",
    )
    packaging_cost = fields.Float(
        compute="_compute_packaging_cost",
        digits="Product Price",
    )
    packaging_cost_unit = fields.Float(
        compute="_compute_packaging_cost",
        digits="Product Price",
    )
    transport_cost_unit = fields.Float(
        compute="_compute_transport_cost_unit",
        digits="Product Price",
    )
    annual_amount = fields.Integer()
    machine_hour_serie = fields.Float(
        string="Machine Hours per Serie",
        compute="_compute_machine_hour",
        digits="Product Price",
    )
    machine_hour_annual = fields.Float(
        string="Annual Machine Hours",
        compute="_compute_machine_hour",
        digits="Product Price",
    )
    purchase_cost_unit = fields.Float(
        compute="_compute_purchase_cost",
        digits="Product Price",
    )
    purchase_cost_serie = fields.Float(
        string="Purchase Cost per Serie",
        compute="_compute_purchase_cost",
        digits="Product Price",
    )
    purchase_cost_annual = fields.Float(
        compute="_compute_purchase_cost",
        digits="Product Price",
    )
    value_added_unit = fields.Float(
        string="Manufacturing cost",
        compute="_compute_value_added",
        digits="Product Price",
    )
    invoicing_serie = fields.Float(
        string="Invoicing By Series",
        compute="_compute_invoicing",
        digits="Product Price",
    )
    invoicing_annual = fields.Float(
        compute="_compute_invoicing",
        digits="Product Price",
    )
    value_added_serie = fields.Float(
        string="Value Added per Serie",
        compute="_compute_value_added",
        digits="Product Price",
    )
    value_added_annual = fields.Float(
        compute="_compute_value_added",
        digits="Product Price",
    )
    value_added_hour = fields.Float(
        compute="_compute_value_added",
        digits="Product Price",
    )
    cost_sales = fields.Float(
        string="Cost Over Sale",
        compute="_compute_cost_sale",
    )
    variant_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Reference",
    )
    waste_percentage = fields.Float(
        default=3.0,
    )

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "The name must be unique!"),
        (
            "figure_positive",
            "CHECK(figure > 0)",
            "The figure value must be strictly positive.",
        ),
        (
            "plate_hour_positive",
            "CHECK(plate_hour > 0)",
            "The plate hour value must be strictly positive.",
        ),
        (
            "serie_positive",
            "CHECK(serie > 0)",
            "The serie value must be strictly positive.",
        ),
        (
            "box_quantity_positive",
            "CHECK(box_quantity > 0)",
            "The box quantity must be strictly positive.",
        ),
        (
            "box_pallet_positive",
            "CHECK(box_pallet > 0)",
            "The box pallet value must be strictly positive.",
        ),
        (
            "adjustment_plates_positive",
            "CHECK(adjustment_plates >= 0)",
            "The adjustment plates must be strictly positive.",
        ),
        (
            "waste_percentage_is_percentage",
            "CHECK(waste_percentage >= 0)",
            "The waste percentage must be positive or 0 at least.",
        ),
    ]

    @api.depends(
        "width",
        "step",
        "thickness",
        "density",
        "serie",
        "waste_percentage",
        "adjustment_plates",
    )
    def _compute_weight(self):
        # width, step and thickness are defined in millimeters
        # density is defined as mg/mm3
        # weight is in kg
        for record in self:
            weight_mg = record.width * record.step * record.thickness * record.density
            plate_weight = weight_mg / 1000000

            plates = record.serie / record.figure
            plate_per_serie = plates * (1 + record.waste_percentage / 100)
            plate_units = plate_per_serie + record.adjustment_plates

            record.update(
                {
                    "plate_weight": plate_weight,
                    "serie_weight": plate_weight * plate_units,
                }
            )

    @api.depends("plate_weight", "material_cost")
    def _compute_plate_costs(self):
        for record in self:
            record.plate_cost = record.plate_weight * record.material_cost

    @api.depends("workcenter_cost", "operator_cost", "operator", "plate_hour", "figure")
    def _compute_costs_unit(self):
        for record in self:
            manufacturing_cost_unit = 0
            if record.plate_hour != 0 and record.figure != 0:
                manufacturing_cost_unit = (
                    record.workcenter_cost + (record.operator_cost * record.operator)
                ) / (record.plate_hour * record.figure)
            record.manufacturing_cost_unit = manufacturing_cost_unit

    @api.depends("mechanic_cost", "workcenter_cost", "assembly", "serie")
    def _compute_assembly_cost(self):
        for record in self:
            assembly_cost_unit = 0.0
            assembly_cost = (
                record.workcenter_cost + record.mechanic_cost
            ) * record.assembly
            if record.serie:
                assembly_cost_unit = assembly_cost / record.serie
            record.update(
                {
                    "assembly_cost": assembly_cost,
                    "assembly_cost_unit": assembly_cost_unit,
                }
            )

    @api.depends("serie", "box_quantity", "box_pallet", "box_cost", "pallet_cost")
    def _compute_packaging_cost(self):
        for record in self:
            packaging_cost_unit = packaging_cost = 0.0
            if record.box_quantity and record.box_pallet:
                boxes = int(record.serie / record.box_quantity)
                pallets = int(boxes / record.box_pallet)
                packaging_cost = (boxes * record.box_cost) + (
                    pallets * record.pallet_cost
                )
            if record.serie:
                packaging_cost_unit = packaging_cost / record.serie
            record.update(
                {
                    "packaging_cost": packaging_cost,
                    "packaging_cost_unit": packaging_cost_unit,
                }
            )

    @api.depends("box_quantity", "box_pallet", "pallet_transport_cost")
    def _compute_transport_cost_unit(self):
        for record in self:
            transport_cost_unit = 0.0
            if record.box_quantity and record.box_pallet:
                transport_cost_unit = record.pallet_transport_cost / (
                    record.box_quantity * record.box_pallet
                )
            record.transport_cost_unit = transport_cost_unit

    @api.depends(
        "figure",
        "serie",
        "plate_cost",
        "manufacturing_cost_unit",
        "assembly_cost_unit",
        "packaging_cost",
        "transport_cost_unit",
    )
    def _compute_amount(self):
        for record in self:
            record._compute_costs_unit()
            amount = 0.0
            if record.figure:
                amount = (
                    (record.plate_cost / record.figure)
                    + record.manufacturing_cost_unit
                    + record.assembly_cost_unit
                    + record.packaging_cost_unit
                    + record.transport_cost_unit
                )
            record.amount = amount

    @api.depends(
        "adjustment_plates",
        "waste_percentage",
        "unit_retail_price",
        "amount",
        "commission",
    )
    def _compute_margin_commission(self):
        for record in self:
            margin = 0.0
            commission_amount = record.unit_retail_price * (record.commission / 100)
            if record.unit_retail_price:
                margin = (
                    (record.unit_retail_price - commission_amount - record.amount)
                    * 100
                    / record.unit_retail_price
                )
            record.update(
                {
                    "commission_amount": commission_amount,
                    "margin": margin,
                }
            )

    @api.depends(
        "assembly", "serie", "figure", "plate_hour", "waste_percentage", "annual_amount"
    )
    def _compute_machine_hour(self):
        for record in self:
            machine_hour_annual = machine_hour_serie = 0.0
            if record.plate_hour and record.figure:
                machine_hour_serie = record.assembly + (
                    (
                        (record.serie * (1 + record.waste_percentage / 100))
                        / record.figure
                    )
                    / record.plate_hour
                )
            if record.serie:
                machine_hour_annual = (
                    machine_hour_serie / record.serie
                ) * record.annual_amount
            record.update(
                {
                    "machine_hour_serie": machine_hour_serie,
                    "machine_hour_annual": machine_hour_annual,
                }
            )

    @api.depends(
        "figure",
        "serie",
        "plate_cost",
        "packaging_cost_unit",
        "transport_cost_unit",
        "adjustment_plates",
        "waste_percentage",
        "annual_amount",
    )
    def _compute_purchase_cost(self):
        for record in self:
            purchase_cost_unit = (
                (record.plate_cost / record.figure)
                + record.packaging_cost_unit
                + record.transport_cost_unit
            )
            purchase_cost_serie = purchase_cost_unit * record.serie
            purchase_cost_annual = purchase_cost_unit * record.annual_amount
            record.update(
                {
                    "purchase_cost_unit": purchase_cost_unit,
                    "purchase_cost_serie": purchase_cost_serie,
                    "purchase_cost_annual": purchase_cost_annual,
                }
            )

    @api.depends("unit_retail_price", "serie", "annual_amount")
    def _compute_invoicing(self):
        for record in self:
            invoicing_serie = record.unit_retail_price * record.serie
            invoicing_annual = record.unit_retail_price * record.annual_amount
            record.update(
                {
                    "invoicing_serie": invoicing_serie,
                    "invoicing_annual": invoicing_annual,
                }
            )

    @api.depends(
        "commission",
        "manufacturing_cost_unit",
        "assembly_cost_unit",
        "machine_hour_serie",
        "purchase_cost_serie",
        "purchase_cost_annual",
        "invoicing_serie",
        "invoicing_annual",
        "adjustment_plates",
        "waste_percentage",
    )
    def _compute_value_added(self):
        for record in self:
            record._compute_costs_unit()
            value_added_unit = (
                record.manufacturing_cost_unit + record.assembly_cost_unit
            )
            value_added_serie = (
                record.invoicing_serie * (1 - record.commission / 100)
                - record.purchase_cost_serie
            )
            value_added_hour = 0.0
            if record.machine_hour_serie:
                value_added_hour = value_added_serie / record.machine_hour_serie
            value_added_annual = (
                record.invoicing_annual * (1 - record.commission / 100)
                - record.purchase_cost_annual
            )
            record.update(
                {
                    "value_added_unit": value_added_unit,
                    "value_added_serie": value_added_serie,
                    "value_added_hour": value_added_hour,
                    "value_added_annual": value_added_annual,
                }
            )

    @api.depends("purchase_cost_serie", "invoicing_serie")
    def _compute_cost_sale(self):
        for record in self:
            cost_sales = 0.0
            if record.invoicing_serie:
                cost_sales = (record.purchase_cost_serie / record.invoicing_serie) * 100
            record.cost_sales = cost_sales

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.density = self.product_id.density
            self.material_cost = self.product_id.list_price

    @api.onchange("workcenter_id")
    def onchange_workcenter_id(self):
        if self.workcenter_id:
            self.workcenter_cost = self.workcenter_id.costs_hour

    @api.onchange("company_id")
    def onchange_company_id(self):
        if self.company_id:
            self.operator_cost = self.company_id.costs_operator
            self.mechanic_cost = self.company_id.costs_mechanic
            self.margin_purchase = self.company_id.margin_purchase
            self.value_added_margin = self.company_id.value_added_margin

    @api.onchange("box_id")
    def onchange_box_id(self):
        if self.box_id:
            self.box_cost = self.box_id.list_price

    @api.onchange("pallet_id")
    def onchange_pallet_id(self):
        if self.pallet_id:
            self.pallet_cost = self.pallet_id.list_price

    @api.onchange("frame_id")
    def onchange_frame_id(self):
        if self.frame_id:
            self.width = self.frame_id.width
            self.step = self.frame_id.step

    @api.onchange(
        "purchase_cost_unit",
        "value_added_margin",
        "margin_purchase",
        "value_added_unit",
        "adjustment_plates",
        "waste_percentage",
    )
    def onchange_unit_retail_price(self):
        if self.purchase_cost_unit and self.value_added_unit:
            self.unit_retail_price = (
                self.purchase_cost_unit * (1 + self.margin_purchase / 100)
            ) + (self.value_added_unit * (1 + self.value_added_margin / 100))

    @api.onchange("serie")
    def onchange_annual_amount(self):
        if self.serie:
            self.annual_amount = self.serie

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", _("New")) == _("New"):
                values["name"] = self.env["ir.sequence"].next_by_code(
                    "thermoformed.cost"
                ) or _("New")
            if values.get("product_id") and not values.get("density"):
                values["density"] = (
                    self.env["product.template"]
                    .browse(values.get("product_id"))
                    .density
                )
        return super().create(vals_list)

    def write(self, vals):
        if not vals.get("density") and vals.get("product_id"):
            vals["density"] = (
                self.env["product.template"].browse(vals.get("product_id")).density
            )
        return super().write(vals)

    def action_block(self):
        self.state = "closed"

    def action_draft(self):
        self.state = "draft"

    def unlink(self):
        if any(thermoformed.state in ["closed"] for thermoformed in self):
            raise ValidationError(_("Deleting is only possible in case of draft"))
        return super().unlink()
