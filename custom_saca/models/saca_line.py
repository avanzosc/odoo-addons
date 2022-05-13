# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SacaLine(models.Model):
    _name = "saca.line"
    _description = "Saca Line"
    _order = "sequence"

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    sequence = fields.Integer(string="Sequence", copy=False)
    saca_id = fields.Many2one(string='Saca', comodel_name='saca')
    lot_id = fields.Many2one(
        string='Lot/Serial Number', comodel_name='stock.production.lot')
    external_supplier = fields.Boolean(
        string='Is external supplier?', default=False)
    partner_id = fields.Many2one(string='Supplier', comodel_name='res.partner')
    breeding_id = fields.Many2one(
        string='Breeding', comodel_name='stock.picking.batch',
        domain="[('batch_type', 'in', ('breeding', False))]")
    warehouse_id = fields.Many2one(
        string='Farm', comodel_name='stock.warehouse',
        related='breeding_id.warehouse_id', store=True)
    farmer_id = fields.Many2one(
        string='Farmer', comodel_name='res.partner',
        related='warehouse_id.farmer_id', store=True)
    street = fields.Char(
        string='Street', related='warehouse_id.street', store=True)
    street2 = fields.Char(
        string='Street2', related='warehouse_id.street2', store=True)
    city = fields.Char(
        string='City', related='warehouse_id.city', store=True)
    state_id = fields.Many2one(
        string='State', comodel_name='res.country.state',
        related='warehouse_id.state_id', store=True)
    zip = fields.Char(
        string='Zip', related='warehouse_id.zip', store=True)
    country_id = fields.Many2one(
        string='Country', comodel_name='res.country',
        related='warehouse_id.country_id', store=True)
    phone = fields.Char(
        string='Phone', related='warehouse_id.partner_id.phone', store=True)
    mobile = fields.Char(
        string='Mobile', related='warehouse_id.partner_id.mobile', store=True)
    existence = fields.Integer(string='Existence')
    age = fields.Integer(string='Age')
    vehicle_id = fields.Many2one(
        string='Vehicle', comodel_name='fleet.vehicle')
    remolque_id = fields.Many2one(
        string='Remolque', comodel_name='fleet.vehicle')
    ates = fields.Char(
        string='Ates', related='remolque_id.ates', store=True)
    cages_num = fields.Integer(
        string='Number of Cages', relates='remolque_id.cages_num', store=True)
    driver_id = fields.Many2one(
        string='Driver',
        comodel_name='res.partner',
        domain="['|', ('category_id', '=', 'Driver'), ('category_id', '=', 'Conductor')]")
    unit_burden = fields.Integer(string='Unit Burden')
    estimate_weight = fields.Float(string='Estimate Weight')
    box_weight = fields.Float(
        string='Box weight', compute = '_compute_box_weight')
    max_weight = fields.Float(string='Max Weight')
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
    guide_unit = fields.Float(string='Guide Units')
    cleaned_date = fields.Date(string='Cleaned Date')
    saca_time = fields.Float(string='Saca Time')
    cleaned_time = fields.Float(string='Cleaned Time')
    fasting = fields.Float(string='Fasting')
    cleaning_seal_number = fields.Char(string='Cleaning Seal Number')
    main_scale = fields.Many2one(
        string='Main Scale', comodel_name='main.scale')
    note = fields.Text(string='Note')
    purchase_price = fields.Float(string='Purchase Price')
    weight_uom_name = fields.Char(
        string='Weight UOM',default=_get_default_weight_uom)
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id)

    @api.depends('unit_burden', 'estimate_weight')
    def _compute_box_weight(self):
        for line in self:
            line.box_weight = line.unit_burden * line.estimate_weight
