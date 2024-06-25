# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"
    _order = "sequence"

    def _default_date_issue_technical_data_sheet(self):
        return fields.Date.context_today(self)

    authorized_signature_id = fields.Many2one(
        strint="Authorized signature", comodel_name="res.users"
    )
    options_included = fields.Text(string="Options included in the type approval")
    reforms_in_vehicle = fields.Text(string="Reforms in vehicle")
    sequence = fields.Char(string="Sequence")
    serial_number_on_tecnical_sheet = fields.Char(
        string="Serial number on tecnical sheet"
    )
    serial_number_id = fields.Many2one(string="(E) - Serial number (Chassis number)")
    brand_id = fields.Many2one(string="(D.1) - Vehicle brand")
    model_id = fields.Many2one(string="(D-3) - Vehicle model or commercial name")
    vehicle_classification_id = fields.Many2one(
        string="(C.L) - Vehicle classification",
        comodel_name="fleet.vehicle.classification",
    )
    type_id = fields.Many2one(string="(D.2) - Vehicle type")
    vehicle_variant_id = fields.Many2one(
        string="(D.2) - Vehicle variant", comodel_name="fleet.vehicle.variant"
    )
    vehicle_version_id = fields.Many2one(
        string="(D.2) - Vehicle version", comodel_name="fleet.vehicle.version"
    )
    vehicle_category_id = fields.Many2one(
        string="(J) - Vehicle category", comodel_name="fleet.vehicle.category"
    )
    password_for_total = fields.Char(string="(K) - Password")
    total_tare = fields.Char(string="Total tare")
    tare_on_axes = fields.Char(string="(G) - Tare on axes (MOM)")
    vehicle_mmta_id = fields.Many2one(
        string="(F.1) - MMTA", comodel_name="fleet.vehicle.mmta"
    )
    vehicle_mmta_axe1_id = fields.Many2one(
        string="(F.1.1) - MMTA axe 1", comodel_name="fleet.vehicle.mmta"
    )
    vehicle_mmta_axe2_id = fields.Many2one(
        string="(F.1.1) - MMTA axe 2", comodel_name="fleet.vehicle.mmta"
    )
    vehicle_mmta_axe3_id = fields.Many2one(
        string="(F.1.1) - MMTA axe 3", comodel_name="fleet.vehicle.mmta"
    )
    vehicle_mmta_axe4_id = fields.Many2one(
        string="(F.1.1) - MMTA axe 4", comodel_name="fleet.vehicle.mmta"
    )
    vehicle_mma_id = fields.Many2one(
        string="(F.2) - MMA", comodel_name="fleet.vehicle.mma"
    )
    vehicle_mma_axe1_id = fields.Many2one(
        string="(F.2.1) - MMA axe 1", comodel_name="fleet.vehicle.mma"
    )
    vehicle_mma_axe2_id = fields.Many2one(
        string="(F.2.1) - MMA axe 2", comodel_name="fleet.vehicle.mma"
    )
    vehicle_mma_axe3_id = fields.Many2one(
        string="(F.2.1) - MMA axe 3", comodel_name="fleet.vehicle.mma"
    )
    vehicle_mma_axe4_id = fields.Many2one(
        string="(F.2.1) - MMA axe 4", comodel_name="fleet.vehicle.mma"
    )
    vehicle_service_brake_type_id = fields.Many2one(
        string="(O.3) - Service brake type",
        comodel_name="fleet.vehicle.service.brake.type",
    )
    total_width = fields.Char(string="(F.5) - Total width")
    total_lenght = fields.Char(string="(F.6) - Total lenght")
    previous_way = fields.Char(string="(F.7) - Previous way")
    posterior_pathway = fields.Char(string="(F.7.1) - Posterior pathway")
    posterior_overhang = fields.Char(string="(F.8) - Posterior overhang")
    distance_between_axis = fields.Char(string="(M.1) - Distance between axis")
    number_of_axes = fields.Char(string="(L) - Number of axes")
    total_wheels_number = fields.Char(string="(L) - Total wheels number")
    number_position_axles_with_twin_wheels = fields.Char(
        string="(L.0) - Number and position of axles with twin wheels"
    )
    tire_dimesion_id = fields.Many2one(
        string="(L.2) - Tire dimensions", comodel_name="fleet.vehicle.tire.dimension"
    )
    ic_iv_tire_id = fields.Many2one(
        string="(L.2) - IC/IV Tires", comodel_name="fleet.vehicle.ic.iv.tire"
    )
    manufacturing_year = fields.Char(string="Manufacturing year")
    date_issue_technical_data_sheet = fields.Date(
        string="Date of issue of the technical data sheet",
        default=_default_date_issue_technical_data_sheet,
    )
    vehicle_start_up_date = fields.Date(string="Vehicle start-up date")
    responsible_commissioning_id = fields.Many2one(
        string="Responsible of the commissioning", comodel_name="hr.employee"
    )
    f11 = fields.Char(string="F11", compute="_compute_f11")
    f12 = fields.Char(string="F12", compute="_compute_f12")
    l = fields.Char(string="L", compute="_compute_l")
    l2 = fields.Char(string="L2", compute="_compute_l2")
    d2 = fields.Char(string="D2", compute="_compute_d2")

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env.ref(
            "fleet_trailer.seq_fleet_vehicle", raise_if_not_found=False
        ).next_by_id()
        return super().create(vals)

    def _compute_f11(self):
        for vehicle in self:
            f11 = ""
            if vehicle.vehicle_mmta_axe1_id:
                f11 = vehicle.vehicle_mmta_axe1_id.name
            if vehicle.vehicle_mmta_axe2_id:
                f11 = (
                    vehicle.vehicle_mmta_axe2_id.name
                    if not f11
                    else "{} // {}".format(f11, vehicle.vehicle_mmta_axe2_id.name)
                )
            if vehicle.vehicle_mmta_axe3_id:
                f11 = (
                    vehicle.vehicle_mmta_axe3_id.name
                    if not f11
                    else "{} // {}".format(f11, vehicle.vehicle_mmta_axe3_id.name)
                )
            if vehicle.vehicle_mmta_axe4_id:
                f11 = (
                    vehicle.vehicle_mmta_axe4_id.name
                    if not f11
                    else "{} // {}".format(f11, vehicle.vehicle_mmta_axe4_id.name)
                )
            self.f11 = f11

    def _compute_f12(self):
        for vehicle in self:
            f12 = ""
            if vehicle.vehicle_mma_axe1_id:
                f12 = vehicle.vehicle_mma_axe1_id.name
            if vehicle.vehicle_mma_axe2_id:
                f12 = (
                    vehicle.vehicle_mma_axe2_id.name
                    if not f12
                    else "{} // {}".format(f12, vehicle.vehicle_mma_axe2_id.name)
                )
            if vehicle.vehicle_mma_axe3_id:
                f12 = (
                    vehicle.vehicle_mma_axe3_id.name
                    if not f12
                    else "{} // {}".format(f12, vehicle.vehicle_mma_axe3_id.name)
                )
            if vehicle.vehicle_mma_axe4_id:
                f12 = (
                    vehicle.vehicle_mma_axe4_id.name
                    if not f12
                    else "{} // {}".format(f12, vehicle.vehicle_mma_axe4_id.name)
                )
            self.f12 = f12

    def _compute_l(self):
        for vehicle in self:
            l = ""
            if vehicle.number_of_axes:
                l = vehicle.number_of_axes
            if vehicle.total_wheels_number:
                l = (
                    vehicle.total_wheels_number
                    if not l
                    else "{} // {}".format(l, vehicle.total_wheels_number)
                )
            self.l = l

    def _compute_l2(self):
        for vehicle in self:
            l2 = ""
            if vehicle.tire_dimesion_id:
                l2 = vehicle.tire_dimesion_id.name
            if vehicle.ic_iv_tire_id:
                l2 = (
                    vehicle.ic_iv_tire_id.name
                    if not l2
                    else "{}    {}".format(l2, vehicle.ic_iv_tire_id.name)
                )
            self.l2 = l2

    def _compute_d2(self):
        for vehicle in self:
            d2 = ""
            if vehicle.type_id:
                d2 = vehicle.type_id.name
            if vehicle.vehicle_variant_id:
                d2 = (
                    vehicle.vehicle_variant_id.name
                    if not d2
                    else "{}/{}".format(d2, vehicle.vehicle_variant_id.name)
                )
            if vehicle.vehicle_version_id:
                d2 = (
                    vehicle.vehicle_version_id.name
                    if not d2
                    else "{}/{}".format(d2, vehicle.vehicle_version_id.name)
                )
            self.d2 = d2
