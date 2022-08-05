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

    def _default_name(self):
        today = fields.Date.today()
        today = u'{}'.format(today)
        return today

    sequence = fields.Integer(string="Sequence", copy=False)
    name = fields.Char(string="Name", default=_default_name)
    saca_id = fields.Many2one(string="Saca", comodel_name="saca")
    lot = fields.Char(
        string="Lot/Serial Number",
        related="saca_id.name",
        store=True)
    seq = fields.Char(string="Seq")
    external_supplier = fields.Boolean(
        string="Is external supplier?", default=False)
    breeding_id = fields.Many2one(
        string="Breeding", comodel_name="stock.picking.batch",
        domain="[('batch_type', '=', ('breeding', False))]")
    farm_id = fields.Many2one(
        string="Farm",
        comodel_name="res.partner")
    farmer_id = fields.Many2one(
        string="Farmer",
        comodel_name="res.partner")
    supplier_id = fields.Many2one(
        string="Supplier", comodel_name="res.partner")
    street = fields.Char(
        string="Street", related="farm_id.street", store=True)
    street2 = fields.Char(
        string="Street2", related="farm_id.street2", store=True)
    city = fields.Char(string="City", related="farm_id.city", store=True)
    state_id = fields.Many2one(
        string="State",
        comodel_name="res.country.state",
        related="farm_id.state_id",
        store=True)
    zip = fields.Char(string="Zip", related="farm_id.zip", store=True)
    country_id = fields.Many2one(
        string="Country",
        comodel_name="res.country",
        related="farm_id.country_id",
        store=True)
    phone = fields.Char(string="Phone", related="farm_id.phone", store=True)
    mobile = fields.Char(string="Mobile", related="farm_id.mobile", store=True)
    existence = fields.Integer(string="Existence")
    age = fields.Integer(string="Age")
    vehicle_id = fields.Many2one(
        string="Vehicle", comodel_name="fleet.vehicle", copy=False)
    remolque_id = fields.Many2one(
        string="Remolque", comodel_name="fleet.vehicle", copy=False)
    ates = fields.Char(
        string="Ates", related="remolque_id.ates", store=True ,copy=False)
    cages_num = fields.Integer(
        string="Number of Cages", related="remolque_id.cages_num", store=True)
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
        copy=False,
        domain="['|', ('category_id', '=', 'Driver'), ('category_id', '=', 'Conductor')]")
    unit_burden = fields.Float(
        string="Units per Cages",
        digits="Weight Decimal Precision",
        copy=False)
    estimate_weight = fields.Float(
        string="Chicken Average Weight",
        digits="Weight Decimal Precision",
        copy=False)
    box_weight = fields.Float(
        string="Box weight",
        compute="_compute_box_weight",
        digits="Weight Decimal Precision",
        store=True)
    max_weight = fields.Float(
        string="Chicken Max Burden",
        help="Chicken unit",
        digits="Weight Decimal Precision",
        compute="_compute_max_weight",
        store=True)
    estimate_burden = fields.Integer(
        string="Chicken Estimate Burden",
        help = "Chicken unit",
        copy=False)
    coya_id = fields.Many2one(string="Coya", comodel_name="coya", copy=False)
    burden_type = fields.Selection(
        string="Burden Type", selection=[
            ("two_farms", "Two farms"),
            ("doublet", "Doublet"),
            ("triplet", "Triplet"),
            ("outside", "Outside"),
            ("quadruple", "Quadruple"),
            ("quintulete", "Quintuplete")],
        copy=False)
    cleaned_date = fields.Date(string="Remolque Disinfection Date", copy=False)
    saca_time = fields.Float(string="Saca Time", copy=False)
    cleaned_time = fields.Float(string="Cleaned Time", copy=False)
    fasting = fields.Float(string="Fasting", copy=False)
    cleaning_seal_number = fields.Char(
        string="Cleaning Seal Number", copy=False)
    main_scale = fields.Many2one(
        string="Scale", comodel_name="main.scale", copy=False)
    note = fields.Text(string="Note", copy=False)
    weight_uom_id = fields.Many2one(
        string="Weight UOM",
        comodel_name="uom.uom",
        default=_get_default_weight_uom,
        domain=lambda self: [
            ("category_id", "=",
             self.env.ref("uom.product_uom_categ_kgm").id)],
        copy=False)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id.id)
    distance = fields.Float(
        string="Distance", related="farm_id.distance", store=True)
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company.id)
    disinfectant_id = fields.Many2one(
        string="Disinfectant",
        comodel_name="product.product",
        default=lambda self: self.env.company.disinfectant_id.id, copy=False)
    date = fields.Date(
        string="Date",
        related="saca_id.date",
        store=True)
    quality_responsible_id = fields.Many2one(
        string="Quality Responsible",
        comodel_name="res.partner",
        copy=False,
        domain="[('category_id', '=', 'Quality Responsible')]")

    @api.depends("unit_burden", "estimate_weight")
    def _compute_box_weight(self):
        for line in self:
            line.box_weight = line.unit_burden * line.estimate_weight

    @api.depends("unit_burden", "cages_num")
    def _compute_max_weight(self):
        for line in self:
            line.max_weight = line.unit_burden * line.cages_num

    @api.onchange("seq")
    def onchange_seq(self):
        if self.seq:
            line = self.env["saca.line"].search([("lot", "=", self.lot), ("seq", "=", self.seq)], limit=1)
            if line:
                self.write({
                    "external_supplier": line.external_supplier,
                    "supplier_id": line.supplier_id.id,
                    "farmer_id": line.farmer_id.id,
                    "farm_id": line.farm_id.id,
                    "breeding_id": line.breeding_id.id,
                    "existence": line.existence,
                    "age": line.age})

    @api.onchange("supplier_id", "saca_id")
    def onchange_name(self):
        if self.supplier_id:
            today = fields.Date.today()
            self.name = u"{}, {}".format(
                today, self.supplier_id.name)

    @api.onchange("farmer_id", "breeding_id")
    def onchange_farmer(self):
        if self.farm_id and self.farmer_id.main_scale:
            self.main_scale = self.farmer_id.main_scale

    @api.onchange("breeding_id", "external_supplier")
    def onchange_breeding_id(self):
        if self.external_supplier is False:
            self.farm_id = self.breeding_id.warehouse_id.partner_id.id
            self.farmer_id = self.breeding_id.warehouse_id.farmer_id.id
            self.supplier_id = self.breeding_id.company_id.partner_id.id
        else:
            self.breeding_id = False
            self.farm_id = False
            self.farmer_id = False
            self.supplier_id = False

    @api.onchange("driver_id")
    def onchange_vehicle_id(self):
        if self.driver_id:
            cond = [("driver_id", "=", self.driver_id.id)]
            self.vehicle_id = self.env["fleet.vehicle"].search(
                cond, limit=1).id

    @api.constrains("lot", "seq", "farmer_id", "farm_id")
    def _check_lots(self):
        for line in self:
            same_lot = self.env["saca.line"].search(
                [("lot", "=", line.lot), ("seq", "=", line.seq)])
            if same_lot and same_lot.farm_id and same_lot.farmer_id and (
                same_lot.farmer_id != line.farmer_id or (
                    same_lot.farm_id != line.farm_id)):
                raise ValidationError(
                        _("It can't be that farm or farmer for that lot."))
