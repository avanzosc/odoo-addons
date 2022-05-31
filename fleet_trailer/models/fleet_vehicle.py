# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    def _default_date_issue_technical_data_sheet(self):
        return fields.Date.context_today(self)

    serial_number_id = fields.Many2one(
        string='(E) - Serial number (Chassis number)')
    brand_id = fields.Many2one(
        string='(D.1) - Vehicle brand')
    model_id = fields.Many2one(
        string='(D-3) - Vehicle model or commercial name')
    vehicle_classification_id = fields.Many2one(
        string='(C.L) - Vehicle classification',
        comodel_name='fleet.vehicle.classification')
    type_id = fields.Many2one(
        string='(D.2) - Vehicle type')
    vehicle_variant_id = fields.Many2one(
        string='(D.2) - Vehicle variant', comodel_name='fleet.vehicle.variant')
    vehicle_version_id = fields.Many2one(
        string='(D.2) - Vehicle version', comodel_name='fleet.vehicle.version')
    vehicle_category_id = fields.Many2one(
        string='(J) - Vehicle category',
        comodel_name='fleet.vehicle.category')
    password_for_total = fields.Char(
        string='(K) - Password for total')
    tare_on_axes = fields.Integer(
        string='(G) - Tare on axes (MOM)')
    vehicle_mmta_axe1_id = fields.Many2one(
        string='(F.1.1) - MMTA axe 1',
        comodel_name='fleet.vehicle.mmta')
    vehicle_mmta_axe2_id = fields.Many2one(
        string='(F.1.1) - MMTA axe 2',
        comodel_name='fleet.vehicle.mmta')
    vehicle_mmta_axe3_id = fields.Many2one(
        string='(F.1.1) - MMTA axe 3',
        comodel_name='fleet.vehicle.mmta')
    vehicle_mmta_axe4_id = fields.Many2one(
        string='(F.1.1) - MMTA axe 4',
        comodel_name='fleet.vehicle.mmta')
    vehicle_mma_id = fields.Many2one(
        string='(F.2) - MMA',
        comodel_name='fleet.vehicle.mma')
    vehicle_mma_axe1_id = fields.Many2one(
        string='(F.2.1) - MMA axe 1',
        comodel_name='fleet.vehicle.mma')
    vehicle_mma_axe2_id = fields.Many2one(
        string='(F.2.1) - MMA axe 2',
        comodel_name='fleet.vehicle.mma')
    vehicle_mma_axe3_id = fields.Many2one(
        string='(F.2.1) - MMA axe 3',
        comodel_name='fleet.vehicle.mma')
    vehicle_mma_axe4_id = fields.Many2one(
        string='(F.2.1) - MMA axe 4',
        comodel_name='fleet.vehicle.mma')
    vehicle_service_brake_type_id = fields.Many2one(
        string='(O.3) - Service brake type',
        comodel_name='fleet.vehicle.service.brake.type')
    total_width = fields.Integer(
        string='(F.5) - Total width')
    total_lenght = fields.Integer(
        string='(F.6) - Total lenght')
    previous_way = fields.Integer(
        string='(F.7) - Previous way')
    posterior_pathway = fields.Integer(
        string='(F.7.1) - Posterior pathway')
    posterior_overhang = fields.Integer(
        string='(F.8) - Posterior overhang')
    distance_between_axis = fields.Integer(
        string='(M.1) - Distance between axis')
    number_of_axes = fields.Integer(
        string='(L) - Number of axes')
    total_wheels_number = fields.Integer(
        string='(L) - Total wheels number')
    number_position_axles_with_twin_wheels = fields.Integer(
        string='(L.0) - Number and position of axles with twin wheels')
    tire_dimesion_id = fields.Many2one(
        string='(L.2) - Tire dimensions',
        comodel_name='fleet.vehicle.tire.dimension')
    ic_iv_tire_id = fields.Many2one(
        string='(L.2) - IC/IV Tires',
        comodel_name='fleet.vehicle.ic.iv.tire')
    manufacturing_year = fields.Integer(
        string='Manufacturing year')
    date_issue_technical_data_sheet = fields.Date(
        string='Date of issue of the technical data sheet',
        default=_default_date_issue_technical_data_sheet)
    vehicle_start_up_date = fields.Date(
        string='Vehicle start-up date')
    responsible_commissioning_id = fields.Many2one(
        string='Responsible of the commissioning', comodel_name='res.partner')
