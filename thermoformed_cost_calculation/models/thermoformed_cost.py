# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ThermoformedCost(models.Model):
    _name = 'thermoformed.cost'
    _description = 'Thermoformed Cost'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('closed', 'Closed')], string="State", default='draft', copy=False)
    code = fields.Char(string='Reference', copy=False)
    user_id = fields.Many2one(
        string='Responsible', comodel_name='res.users',
        default=lambda self: self.env.user)
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner')
    description = fields.Char(string='Description')
    company_id = fields.Many2one(
        string='Company', comodel_name='res.company',
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        string='Currency', comodel_name='res.currency',
        related='company_id.currency_id', store=True)
    amount = fields.Float(
        string='Amount', compute='_compute_amount',
        digits='Price Unit')
    commission = fields.Float(string='Commission', default=1)
    commission_amount = fields.Float(
        string='Commission amount', compute='_compute_commission_amount',
        digits='Price Unit')
    margin_purchase = fields.Float(string='Default Purchase Margin')
    value_added_margin = fields.Float(string='Default Value Added Margin')
    unit_retail_price = fields.Float(
        string='Unit Retail Price', digits='Price Unit')
    margin = fields.Float(
        string='Margin', compute='_compute_margin')
    workcenter_id = fields.Many2one(
        string='Work center', comodel_name='mrp.workcenter')
    frame_id = fields.Many2one(string='Frame', comodel_name='frame')
    width = fields.Float(string='Width')
    step = fields.Float(string='Step')
    thickness = fields.Float(string='Thickness')
    figure = fields.Integer(string='Figure', default=1)
    product_id = fields.Many2one(
        string='Material', comodel_name='product.template')
    density = fields.Float(string='Density')
    plate_hour = fields.Integer(string='Plates in hour', default=1)
    assembly = fields.Float(string='Assembly')
    operator = fields.Float(string='Operators', default=1.0)
    serie = fields.Integer(string='Series', default=10000)
    plate_weight = fields.Float(
        string='Plate Weight', compute='_compute_plate_weight',
        digits='Price Unit')
    costs_kilo = fields.Float(
        string='Euros per Kilo', digits='Price Unit')
    costs_plate = fields.Float(
        string='Costs Plate', compute='_compute_plate_costs',
        digits='Price Unit')
    costs_hour = fields.Float(
        string='Costs Hour')
    costs_operator = fields.Float(
        string='Costs Operator', readonly=False)
    costs_unit = fields.Float(
        string='Costs per Unit Manufactured', compute='_compute_costs_unit',
        digits='Price Unit')
    costs_mechanic = fields.Float(
        string='Costs Mechanic', readonly=False)
    costs_assembly = fields.Float(
        string='Costs per Assembly', compute='_compute_costs_assembly',
        digits='Price Unit')
    costs_assembly_unit = fields.Float(
        string='Cost Assembly per Unit',
        compute='_compute_costs_assembly_unit',
        digits='Price Unit')
    box_id = fields.Many2one(
        string='Box reference', comodel_name='product.template')
    costs_box = fields.Float(string='Cost of the Box')
    box_quantity = fields.Integer(string='Units per Box', default=1)
    pallet_id = fields.Many2one(
        string='Pallet Reference', comodel_name='product.template')
    costs_pallet = fields.Float(string='Pallet Costs')
    box_pallet = fields.Integer(string='Box per Pallet', default=16)
    unit_costs_packaging = fields.Float(
        string='Unit Packaging Cost', compute='_compute_unit_costs_packaging',
        digits='Price Unit')
    costs_pallet_transport = fields.Float(
        string='Pallet Transport Cost', default=40)
    costs_transport_unit = fields.Float(
        string='Unit Transport Cost', compute='_compute_costs_transport_unit',
        digits='Price Unit')
    hide_button = fields.Boolean(string='Hide button', default=False)
    plate_weight_serie = fields.Float(
        string='Plate weight per serie', compute='_compute_plate_weight_serie',
        digits='Price Unit')
    annual_amount = fields.Integer(string='Annual Amount')
    hour_machine_serie = fields.Float(
        string='Hours Machine per Serie',
        compute='_compute_hour_machine_serie', digits='Price Unit')
    annual_machine_hour = fields.Float(
        string='Annual Machine Hours', compute='_compute_annual_machine_hour',
        digits='Price Unit')
    unit_purchase_cost = fields.Float(
        string='Unit Purchase Cost', compute='_compute_unit_purchase_cost',
        digits='Price Unit')
    purchase_cost_serie = fields.Float(
        string='Purchase Cost per Serie',
        compute='_compute_purchase_cost_serie', digits='Price Unit')
    annual_purchase_cost = fields.Float(
        string='Annual Purchase Cost', compute='_compute_annual_purchase_cost',
        digits='Price Unit')
    value_added_unit = fields.Float(
        string='Manufacturing cost', compute='_compute_value_added_unit',
        digits='Price Unit')
    invoicing_serie = fields.Float(
        string='Invoicing By Series', compute='_compute_invoicing_serie',
        digits='Price Unit')
    annual_invoicing = fields.Float(
        string='Annual Invoicing', compute='_compute_annual_invoicing',
        digits='Price Unit')
    value_added_serie = fields.Float(
        string='Value Added per Serie', compute='_compute_value_added_serie',
        digits='Price Unit')
    annual_value_added = fields.Float(
        string='Annual Value Added', compute='_compute_annual_value_added',
        digits='Price Unit')
    value_added_hour = fields.Float(
        string='Value Added Hour', compute='_compute_value_added_hour',
        digits='Price Unit')
    cost_sales = fields.Float(
        string='Cost Over Sale', compute='_compute_cost_sale')

    @api.depends('width', 'step', 'thickness', 'density')
    def _compute_plate_weight(self):
        for record in self:
            record.plate_weight = (
                (record.width * record.step) * (
                    record.thickness * record.density)) / 1000000

    @api.depends('costs_plate', 'figure', 'costs_unit', 'costs_assembly_unit',
                 'unit_costs_packaging', 'costs_transport_unit')
    def _compute_amount(self):
        for record in self:
            if record.figure == 0:
                raise ValidationError(
                    _("The figure quantity cannot be 0."))
            else:
                record.amount = (
                    (record.costs_plate / record.figure) + (
                        record.costs_unit + record.costs_assembly_unit) + (
                            record.unit_costs_packaging + (
                                record.costs_transport_unit)))

    @api.depends('unit_retail_price', 'commission')
    def _compute_commission_amount(self):
        for record in self:
            record.commission_amount = record.unit_retail_price * (
                record.commission / 100)

    @api.depends('unit_retail_price', 'amount', 'commission_amount')
    def _compute_margin(self):
        for record in self:
            if record.unit_retail_price != 0:
                record.margin = ((
                    record.unit_retail_price) - record.commission_amount - (
                        record.amount)) * 100 / record.unit_retail_price
            else:
                record.margin = 0

    @api.depends('plate_weight', 'costs_kilo')
    def _compute_plate_costs(self):
        for record in self:
            record.costs_plate = record.plate_weight * record.costs_kilo

    @api.depends('costs_hour', 'costs_operator', 'operator', 'plate_hour',
                 'figure')
    def _compute_costs_unit(self):
        for record in self:
            if record.plate_hour != 0 and record.figure != 0:
                record.costs_unit = (
                    record.costs_hour + (
                        record.costs_operator * record.operator)) / (
                            record.plate_hour * record.figure)
            else:
                raise ValidationError(
                    _("The number of figures or the number of plates per hour "
                      "can not be 0."))

    @api.depends('costs_mechanic', 'costs_hour', 'assembly')
    def _compute_costs_assembly(self):
        for record in self:
            record.costs_assembly = (
                record.costs_hour + record.costs_mechanic) * record.assembly

    @api.depends('costs_assembly', 'serie')
    def _compute_costs_assembly_unit(self):
        for record in self:
            if record.serie != 0:
                record.costs_assembly_unit = (
                    record.costs_assembly / record.serie)
            else:
                raise ValidationError(
                    _("The number of series can not be 0."))

    @api.depends('box_quantity', 'box_pallet', 'costs_box', 'costs_pallet')
    def _compute_unit_costs_packaging(self):
        for record in self:
            if record.box_quantity != 0 and record.box_pallet != 0:
                record.unit_costs_packaging = (
                    record.costs_box + record.costs_pallet / (
                        record.box_pallet)) / record.box_quantity
            else:
                raise ValidationError(
                    _("The quantity of boxes or the number of boxes per "
                      "pallet can not be 0."))

    @api.depends('box_quantity', 'box_pallet', 'costs_pallet_transport')
    def _compute_costs_transport_unit(self):
        for record in self:
            if record.box_quantity != 0 and record.box_pallet != 0:
                record.costs_transport_unit = record.costs_pallet_transport / (
                    record.box_quantity * record.box_pallet)
            else:
                raise ValidationError(
                    _("The quantity of boxes or the number of boxes per "
                      "pallet can not be 0."))

    @api.depends('plate_weight', 'serie', 'figure')
    def _compute_plate_weight_serie(self):
        for record in self:
            if record.figure != 0:
                record.plate_weight_serie = record.plate_weight * (
                    record.serie / record.figure)
            else:
                raise ValidationError(
                    _("The figure can not be 0."))

    @api.depends('assembly', 'serie', 'figure', 'plate_hour')
    def _compute_hour_machine_serie(self):
        for record in self:
            if record.plate_hour != 0 and record.figure:
                record.hour_machine_serie = record.assembly + (
                    record.serie / record.figure) / record.plate_hour
            else:
                raise ValidationError(
                    _("Plate per hour and figure can not be 0."))

    @api.depends('annual_amount', 'serie', 'hour_machine_serie')
    def _compute_annual_machine_hour(self):
        for record in self:
            if record.serie != 0:
                record.annual_machine_hour = (
                    record.annual_amount / record.serie) * (
                        record.hour_machine_serie)
            else:
                raise ValidationError(
                    _("Serie can not be 0."))

    @api.depends('costs_plate', 'figure', 'unit_costs_packaging',
                 'costs_transport_unit')
    def _compute_unit_purchase_cost(self):
        for record in self:
            record.unit_purchase_cost = record.costs_plate / record.figure + (
                record.unit_costs_packaging) + record.costs_transport_unit

    @api.depends('unit_purchase_cost', 'serie')
    def _compute_purchase_cost_serie(self):
        for record in self:
            record.purchase_cost_serie = record.unit_purchase_cost * (
                record.serie)

    @api.depends('unit_purchase_cost', 'annual_amount')
    def _compute_annual_purchase_cost(self):
        for record in self:
            record.annual_purchase_cost = record.unit_purchase_cost * (
                record.annual_amount)

    @api.depends('costs_unit', 'costs_assembly_unit')
    def _compute_value_added_unit(self):
        for record in self:
            record.value_added_unit = (
                record.costs_unit + record.costs_assembly_unit)

    @api.depends('unit_retail_price', 'serie')
    def _compute_invoicing_serie(self):
        for record in self:
            record.invoicing_serie = (
                record.unit_retail_price * record.serie)

    @api.depends('unit_retail_price', 'annual_amount')
    def _compute_annual_invoicing(self):
        for record in self:
            record.annual_invoicing = (
                record.unit_retail_price * record.annual_amount)

    @api.depends('invoicing_serie', 'commission', 'purchase_cost_serie')
    def _compute_value_added_serie(self):
        for record in self:
            record.value_added_serie = record.invoicing_serie * (
                1-record.commission/100) - record.purchase_cost_serie

    @api.depends('annual_invoicing', 'commission', 'annual_purchase_cost')
    def _compute_annual_value_added(self):
        for record in self:
            record.annual_value_added = record.annual_invoicing * (
                1-record.commission/100) - record.annual_purchase_cost

    @api.depends('value_added_serie', 'hour_machine_serie')
    def _compute_value_added_hour(self):
        for record in self:
            if record.hour_machine_serie != 0:
                record.value_added_hour = (
                    record.value_added_serie / record.hour_machine_serie)
            else:
                raise ValidationError(
                    _("Hour machine per serie can not be 0."))

    @api.depends('purchase_cost_serie', 'invoicing_serie')
    def _compute_cost_sale(self):
        for record in self:
            record.cost_sales = 0
            if record.invoicing_serie != 0:
                record.cost_sales = (
                    record.purchase_cost_serie / record.invoicing_serie) * 100

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.density = self.product_id.density
            self.costs_kilo = self.product_id.list_price

    @api.onchange('workcenter_id')
    def onchange_workcenter_id(self):
        if self.workcenter_id:
            self.costs_hour = self.workcenter_id.costs_hour

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            self.costs_operator = self.company_id.costs_operator
            self.costs_mechanic = self.company_id.costs_mechanic
            self.margin_purchase = self.company_id.margin_purchase
            self.value_added_margin = self.company_id.value_added_margin

    @api.onchange('box_id')
    def onchange_box_id(self):
        if self.box_id:
            self.costs_box = self.box_id.list_price

    @api.onchange('pallet_id')
    def onchange_pallet_id(self):
        if self.pallet_id:
            self.costs_pallet = self.pallet_id.list_price

    @api.onchange('frame_id')
    def onchange_frame_id(self):
        if self.frame_id:
            self.width = self.frame_id.width
            self.step = self.frame_id.step

    @api.onchange('unit_purchase_cost', 'value_added_margin',
                  'margin_purchase', 'value_added_unit')
    def onchange_unit_retail_price(self):
        if self.unit_purchase_cost and self.value_added_unit:
            self.unit_retail_price = self.unit_purchase_cost * (
                1 + self.margin_purchase / 100) + self.value_added_unit * (
                    1 + self.value_added_margin / 100)

    @api.onchange('serie')
    def onchange_annual_amount(self):
        if self.serie:
            self.annual_amount = self.serie

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'thermoformed.cost') or _('New')
        if vals.get('product_id'):
            vals['density'] = self.env['product.template'].browse(
                vals.get('product_id')).density
        result = super(ThermoformedCost, self).create(vals)
        return result

    def write(self, vals):
        if vals.get('product_id'):
            vals['density'] = self.env['product.template'].browse(
                vals.get('product_id')).density
        res = super(ThermoformedCost, self).write(vals)
        return res

    def action_block(self):
        self.state = 'closed'
        self.hide_button = True

    def action_draft(self):
        self.state = 'draft'
        self.hide_button = False

    def unlink(self):
        for thermoformed in self:
            if thermoformed.state in ('closed'):
                raise ValidationError(_(
                    'Deleting is only possible in case of draft'))
        return super(ThermoformedCost, self).unlink()
