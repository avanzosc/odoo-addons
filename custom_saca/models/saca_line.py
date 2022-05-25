# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class SacaLine(models.Model):
    _name = "saca.line"
    _description = "Saca Line"
    _order = "sequence"

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    def _default_lot(self):
        today = fields.Date.today()
        today = today + relativedelta(days=1)
        today = u'{}'.format(today)
        today = today.replace("-", "")
        return today

    sequence = fields.Integer(string="Sequence", copy=False)
    saca_id = fields.Many2one(string='Saca', comodel_name='saca')
    lot = fields.Char(
        string='Lot/Serial Number', default=_default_lot)
    external_supplier = fields.Boolean(
        string='Is external supplier?', default=False)
    breeding_id = fields.Many2one(
        string='Breeding', comodel_name='stock.picking.batch',
        domain="[('batch_type', 'in', ('breeding', False))]")
    farm_id = fields.Many2one(string='Farm', comodel_name='res.partner')
    farmer_id = fields.Many2one(
        string='Farmer', comodel_name='res.partner')
    supplier_id = fields.Many2one(
        string='Supplier', comodel_name='res.partner')
    street = fields.Char(
        string='Street', related='farm_id.street', store=True)
    street2 = fields.Char(
        string='Street2', related='farm_id.street2', store=True)
    city = fields.Char(string='City', related='farm_id.city', store=True)
    state_id = fields.Many2one(
        string='State',
        comodel_name='res.country.state',
        related='farm_id.state_id',
        store=True)
    zip = fields.Char(string='Zip', related='farm_id.zip', store=True)
    country_id = fields.Many2one(
        string='Country',
        comodel_name='res.country',
        related='farm_id.country_id',
        store=True)
    phone = fields.Char(string='Phone', related='farm_id.phone', store=True)
    mobile = fields.Char(string='Mobile', related='farm_id.mobile', store=True)
    existence = fields.Integer(string='Existence')
    age = fields.Integer(string='Age')
    vehicle_id = fields.Many2one(
        string='Vehicle', comodel_name='fleet.vehicle')
    remolque_id = fields.Many2one(
        string='Remolque', comodel_name='fleet.vehicle')
    ates = fields.Char(
        string='Ates', related='farm_id.ates', store=True)
    cages_num = fields.Integer(
        string='Number of Cages', related='remolque_id.cages_num', store=True)
    driver_id = fields.Many2one(
        string='Driver',
        comodel_name='res.partner',
        domain="['|', ('category_id', '=', 'Driver'), ('category_id', '=', 'Conductor')]")
    unit_burden = fields.Float(string='Unit Burden')
    estimate_weight = fields.Float(string='Estimate Weight')
    box_weight = fields.Float(
        string='Box weight', compute='_compute_box_weight')
    max_weight = fields.Float(
        string='Max Burden', compute='_compute_max_weight')
    estimated_burden = fields.Float(string='Estimated Burden')
    coya_id = fields.Many2one(string='Coya', comodel_name='coya')
    burden_type = fields.Selection(
        string='Burden Type', selection=[
            ('two_farms', 'Two farms'),
            ('doublet', 'Doublet'),
            ('triplet', 'Triplet'),
            ('outside', 'Outside'),
            ('quadruple', 'Quadruple'),
            ('quintulete', 'Quintuplete')])
    cleaned_date = fields.Date(string='Remolque Disinfection Date')
    saca_time = fields.Float(string='Saca Time')
    cleaned_time = fields.Float(string='Cleaned Time')
    fasting = fields.Float(string='Fasting')
    cleaning_seal_number = fields.Char(string='Cleaning Seal Number')
    main_scale = fields.Many2one(
        string='Main Scale', comodel_name='main.scale')
    note = fields.Text(string='Note')
    purchase_price = fields.Float(string='Purchase Price')
    weight_uom_name = fields.Char(
        string='Weight UOM', default=_get_default_weight_uom)
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id)
    distance = fields.Float(
        string='Distance', related='farm_id.distance', store=True)
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        default=lambda self: self.env.company.id)
    disinfectant_id = fields.Many2one(
        string='Disinfectant',
        comodel_name="product.product",
        default=lambda self: self.env.company.disinfectant_id.id)

    @api.depends('unit_burden', 'estimate_weight')
    def _compute_box_weight(self):
        for line in self:
            line.box_weight = line.unit_burden * line.estimate_weight

    @api.depends('unit_burden', 'cages_num')
    def _compute_max_weight(self):
        for line in self:
            line.max_weight = line.unit_burden * line.cages_num

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

    @api.onchange("max_weight")
    def onchange_estimated_burden(self):
        if self.max_weight:
            self.estimated_burden = self.max_weight
