# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    @api.depends("object_id")
    def _generate_ref_model_name(self):
        model_obj = self.env["ir.model"]
        for inspection in self:
            inspection.ref_model_name = False
            if inspection.object_id:
                cond = [("model", "=", str(inspection.object_id._model))]
                model = model_obj.search(cond)
                inspection.ref_model_name = model.name

    @api.depends("object_id")
    def _generate_ref_name(self):
        for inspection in self.filtered(lambda x: x.object_id):
            try:
                inspection.ref_name = inspection.object_id.name
            except Exception:
                inspection.ref_name = inspection.object_id.display_name

    ref_model_name = fields.Char(
        string="Ref. Model", compute="_generate_ref_model_name", store=True
    )
    ref_name = fields.Char(string="Ref. Name", compute="_generate_ref_name", store=True)
