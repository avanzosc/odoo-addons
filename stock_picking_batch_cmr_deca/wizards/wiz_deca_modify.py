# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError


class WizDecaModify(models.TransientModel):
    _name = "wiz.deca.modify"
    _description = "Wizard for Register a DeCA In-Route Modification (Método A)"

    batch_id = fields.Many2one("stock.picking.batch", required=True)
    # Dynamic domains on a field only accept fields living directly on this
    # model, not a dotted traversal through deca_id -- hence this related
    # field, purely so new_plate_tractor_id/new_plate_trailer_id's domains
    # below have something to point at.
    carrier_partner_id = fields.Many2one(related="batch_id.cmr_transportation_id")
    field_to_change = fields.Selection(
        [
            ("cmr_tractor_id", "Tractor"),
            ("cmr_tractor_license_plate", "Tractor Plate"),
            ("cmr_semi_trailer_id", "Trailer"),
            ("cmr_semi_trailer_license_plate", "Trailer Plate"),
            ("cmr_transportation_id", "Carrier"),
            ("cmr_special_traffic_authorization", "Special Circulation Authorization"),
            ("cmr_observations", "Observations"),
        ],
        required=True,
    )
    new_value_char = fields.Char(string="New Value")
    new_carrier_partner_id = fields.Many2one(
        "res.partner",
        string="New Carrier",
    )
    new_plate_tractor_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="New Tractor",
    )
    new_tractor_license_plate = fields.Char(string="Tractor license plate")
    new_plate_trailer_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="New Trailer",
    )
    new_semi_trailer_license_plate = fields.Char(
        string="New Semi-trailer Plate", copy=False
    )
    reason = fields.Char(required=True)

    def action_apply(self):
        self.ensure_one()
        if self.field_to_change == "cmr_transportation_id":
            if not self.new_carrier_partner_id:
                raise UserError(_("Select the new carrier."))
            new_value = self.new_carrier_partner_id.id
        elif self.field_to_change == "cmr_tractor_id":
            if not self.new_plate_tractor_id:
                raise UserError(_("Select the new tractor."))
            new_value = self.new_plate_tractor_id.id
        elif self.field_to_change == "cmr_tractor_license_plate":
            if not self.new_tractor_license_plate:
                raise UserError(_("Select the new trailer plate."))
            new_value = self.new_tractor_license_plate
        elif self.field_to_change == "cmr_semi_trailer_id":
            if not self.new_plate_trailer_id:
                raise UserError(_("Select the new trailer."))
            new_value = self.new_plate_trailer_id.id
        elif self.field_to_change == "cmr_semi_trailer_license_plate":
            if not self.new_semi_trailer_license_plate:
                raise UserError(_("Select the new trailer plate."))
            new_value = self.nnew_semi_trailer_license_plate
        else:
            if not self.new_value_char:
                raise UserError(_("Enter the new value."))
            new_value = self.new_value_char
        self.batch_id._apply_change(self.field_to_change, new_value, self.reason)
        return {"type": "ir.actions.act_window_close"}
