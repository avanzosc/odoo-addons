# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SacaLine(models.Model):
    _name = "saca.line"
    _description = "Saca Line"
    _order = "sequence"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_default_weight_uom(self):
        try:
            return self.env.ref("uom.product_uom_kgm").id
        except Exception:
            return False

    def _default_sequence(self):
        sequence = 0
        if "default_saca_id" in self.env.context:
            saca = self.env["saca"].search(
                [("id", "=", self.env.context["default_saca_id"])]
            )
            sequence = len(saca.saca_line_ids)
        return sequence

    sequence = fields.Integer(
        string="Sequence", copy=False, required=True, default=_default_sequence
    )
    name = fields.Char(string="Order", compute="_compute_name")
    saca_id = fields.Many2one(string="Saca", comodel_name="saca")
    lot = fields.Char(string="Lot/Serial Number", related="saca_id.name", store=True)
    seq = fields.Char(string="Seq")
    external_supplier = fields.Boolean(string="Is external supplier?", default=False)
    breeding_id = fields.Many2one(
        string="Breeding",
        comodel_name="stock.picking.batch",
        domain="[('batch_type', '=', ('breeding', False))]",
    )
    farm_id = fields.Many2one(string="Farm1", comodel_name="res.partner")
    farm_warehouse_id = fields.Many2one(
        string="Farm",
        comodel_name="stock.warehouse",
        related="breeding_id.warehouse_id",
        store=True,
    )
    farmer_id = fields.Many2one(string="Farmer", comodel_name="res.partner")
    supplier_id = fields.Many2one(string="Supplier", comodel_name="res.partner")
    street = fields.Char(string="Street", related="farm_id.street", store=True)
    street2 = fields.Char(string="Street2", related="farm_id.street2", store=True)
    city = fields.Char(string="City", related="farm_id.city", store=True)
    state_id = fields.Many2one(
        string="State",
        comodel_name="res.country.state",
        related="farm_id.state_id",
        store=True,
    )
    zip = fields.Char(string="Zip", related="farm_id.zip", store=True)
    country_id = fields.Many2one(
        string="Country",
        comodel_name="res.country",
        related="farm_id.country_id",
        store=True,
    )
    phone = fields.Char(string="Phone", related="farm_id.phone", store=True)
    mobile = fields.Char(string="Mobile", related="farm_id.mobile", store=True)
    existence = fields.Integer(
        string="Existence", compute="_compute_existence_age", store=True
    )
    age = fields.Integer(string="Age", compute="_compute_existence_age", store=True)
    vehicle_id = fields.Many2one(string="Vehicle", comodel_name="fleet.vehicle")
    remolque_id = fields.Many2one(string="Remolque", comodel_name="fleet.vehicle")
    ates = fields.Char(string="Ates", related="remolque_id.ates")
    cages_num = fields.Integer(string="Rows")
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
        domain="['|', ('category_id', '=', 'Driver'), ('category_id', '=', 'Conductor')]",
    )
    unit_burden = fields.Float(string="Units per Cage")
    estimate_weight = fields.Float(
        string="Chicken Average Weight", digits="Weight Decimal Precision"
    )
    box_weight = fields.Float(
        string="Box weight",
        compute="_compute_box_weight",
        digits="Weight Decimal Precision",
    )
    max_weight = fields.Integer(
        string="Chicken Max Burden", help="Chicken unit", compute="_compute_max_weight"
    )
    estimate_burden = fields.Integer(
        string="Chicken Estimate Burden", help="Chicken unit"
    )
    coya_id = fields.Many2one(string="Coya", comodel_name="coya")
    burden_type_id = fields.Many2one(string="Burden Type", comodel_name="burden.type")
    cleaned_date = fields.Date(string="Remolque Disinfection Date")
    saca_time = fields.Float(string="Saca Time")
    cleaned_time = fields.Float(string="Cleaned Time")
    cleaning_seal_number = fields.Char(string="Cleaning Seal Number")
    main_scale = fields.Many2one(string="Scale", comodel_name="main.scale")
    note = fields.Text(string="Note")
    weight_uom_id = fields.Many2one(
        string="Weight UOM",
        comodel_name="uom.uom",
        default=_get_default_weight_uom,
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_kgm").id)
        ],
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self.company_id.currency_id.id,
    )
    distance = fields.Float(string="Distance", compute="_compute_distance", store=True)
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="saca_id.company_id",
        store=True,
    )
    disinfectant_id = fields.Many2one(
        string="Disinfectant",
        comodel_name="product.product",
        default=lambda self: self.env.company.disinfectant_id.id,
    )
    date = fields.Date(string="Date", related="saca_id.date", store=True)
    unload_date = fields.Datetime(string="Unload Date", copy=False)
    is_historic = fields.Boolean(string="Is Historic", default=False)

    @api.depends(
        "external_supplier",
        "farm_id",
        "farm_id.distance",
        "farm_warehouse_id",
        "farm_warehouse_id.distance_slaughterhouse",
    )
    def _compute_distance(self):
        for saca_line in self:
            saca_line.distance = 0
            if saca_line.external_supplier and saca_line.farm_id:
                saca_line.distance = saca_line.farm_id.distance
            if not saca_line.external_supplier and saca_line.farm_warehouse_id:
                saca_line.distance = saca_line.farm_warehouse_id.distance_slaughterhouse

    @api.depends("breeding_id", "breeding_id.estimate_weight_ids")
    def _compute_existence_age(self):
        for line in self:
            line.existence = 0
            line.age = 0
            if line.breeding_id and line.breeding_id.estimate_weight_ids:
                scale = line.breeding_id.estimate_weight_ids.search(
                    [("date", "=", line.date), ("batch_id", "=", line.breeding_id.id)],
                    limit=1,
                )
                line.existence = scale.unit
                line.age = scale.day

    @api.depends("unit_burden", "estimate_weight")
    def _compute_box_weight(self):
        for line in self:
            line.box_weight = line.unit_burden * line.estimate_weight

    @api.depends("unit_burden", "cages_num")
    def _compute_max_weight(self):
        for line in self:
            line.max_weight = line.unit_burden * line.cages_num * 18

    @api.depends("sequence")
    def _compute_name(self):
        for line in self:
            name = 1
            if line.sequence:
                name = line.sequence + 1
            line.name = "{}".format(name)

    @api.onchange("driver_id")
    def onchange_vehicle_id(self):
        if self.driver_id:
            cond = [("driver_id", "=", self.driver_id.id)]
            self.vehicle_id = self.env["fleet.vehicle"].search(cond, limit=1).id

    @api.onchange("remolque_id")
    def onchange_remolque_id(self):
        if self.remolque_id:
            self.cages_num = self.remolque_id.cages_num / 18

    @api.onchange("breeding_id", "external_supplier")
    def onchange_breeding_id(self):
        if self.external_supplier and self.breeding_id:
            raise ValidationError(
                _("There is a lot with a breeding so it can't be external.")
            )
        if self.external_supplier is False:
            self.farm_id = self.breeding_id.warehouse_id.partner_id.id
            self.farmer_id = self.breeding_id.warehouse_id.farmer_id.id
            self.supplier_id = self.breeding_id.company_id.partner_id.id
            self.main_scale = self.farm_warehouse_id.main_scale.id
        else:
            lines = self.saca_id.saca_line_ids.filtered(lambda c: c.seq == self.seq)
            if lines:
                for line in lines:
                    self.supplier_id = line.supplier_id.id
                    self.farmer_id = line.farmer_id.id
                    self.farm_id = line.farm_id.id
                    self.main_scale = self.farm_id.main_scale.id
            else:
                self.breeding_id = False
                self.farm_id = False
                self.farmer_id = False
                self.supplier_id = False
                self.main_scale = False

    @api.onchange("seq", "saca_id")
    def onchange_breeding_domain(self):
        domain = {}
        self.ensure_one()
        if self.seq and self.saca_id:
            self.breeding_id = False
            self.external_supplier = False
            self.main_scale = False
            breeding = []
            lines = self.saca_id.saca_line_ids.filtered(lambda c: c.seq == self.seq)
            if lines:
                for line in lines:
                    if line.breeding_id and (line.breeding_id.id) not in (breeding):
                        breeding.append(line.breeding_id.id)
                    elif line.external_supplier:
                        self.external_supplier = True
                        self.supplier_id = line.supplier_id.id
                        self.farmer_id = line.farmer_id.id
                        self.farm_id = line.farm_id.id
                        self.main_scale = line.farm_id.main_scale.id
            else:
                self.supplier_id = False
                lines_breeding = []
                lines = self.saca_id.saca_line_ids.filtered("breeding_id")
                for line in lines:
                    if line.breeding_id.id not in lines_breeding:
                        lines_breeding.append(line.breeding_id.id)
                    if lines_breeding:
                        breedings = self.env["stock.picking.batch"].search(
                            [
                                ("id", "not in", lines_breeding),
                                ("batch_type", "=", "breeding"),
                            ]
                        )
                        for b in breedings:
                            breeding.append(b.id)
                if not lines:
                    breeding = (
                        self.env["stock.picking.batch"]
                        .search([("batch_type", "=", "breeding")])
                        .ids
                    )
            domain = {"domain": {"breeding_id": [("id", "in", breeding)]}}
            if len(breeding) == 1:
                self.breeding_id = breeding[0]
        return domain
