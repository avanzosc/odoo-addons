# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    def _count_claims(self):
        claim_obj = self.env["crm.claim"]
        cond = [("model_ref_id", "=", "%s,%d" % (self._name, self.id))]
        claims = claim_obj.search(cond)
        self.claims = len(claims)

    automatic_claims = fields.Boolean(
        "Automatic Claims",
        default=False,
        help="If you want to create one claim when the quality test status is"
        " 'Quality failed'.",
    )
    automatic_claims_by_line = fields.Boolean(
        "Automatic Claims by line",
        default=False,
        help="If you want to create one claim per quality test line, when the"
        " quality test line status is 'No ok'.",
    )
    claims = fields.Integer(
        string="Created claims", compute="_count_claims", store=False
    )

    def _prepare_inspection_header(self, object_ref, trigger_line):
        result = super()._prepare_inspection_header(object_ref, trigger_line)
        result.update(
            {
                "automatic_claims": trigger_line.test.automatic_claims,
                "automatic_claims_by_line": trigger_line.test.automatic_claims_by_line,
            }
        )
        return result

    def action_approve(self):
        crm_claim_obj = self.env["crm.claim"]
        super().action_approve()
        for inspection in self:
            if inspection.state == "failed" and inspection.automatic_claims:
                vals = inspection.init_claim_vals()
                if self.object_id:
                    id, name = self.object_id.name_get()[0]
                    vals["name"] = _(
                        "Quality test %s for object %s " " unsurpassed"
                    ) % (self.name, name)
                else:
                    vals["name"] = _("Quality test %s unsurpassed") % (self.name)
                crm_claim_obj.create(vals)
            elif inspection.automatic_claims_by_line:
                for line in inspection.inspection_lines:
                    if not line.success:
                        inspection.create_claim_by_line(line)

    def init_claim_vals(self):
        vals = {
            "date": fields.Datetime.now(),
            "model_ref_id": "%s,%d" % (self._name, self.id),
        }
        return vals

    def create_claim_by_line(self, line):
        crm_claim_obj = self.env["crm.claim"]
        vals = self.init_claim_vals()
        if self.object_id:
            id, name = self.object_id.name_get()[0]
            vals["name"] = _(
                "Quality test %s for %s unsurpassed, in test" " line %s"
            ) % (self.name, name, line.name)
        else:
            vals["name"] = _("Quality test %s unsurpassed, in test line %s") % (
                self.name,
                line.name,
            )
        claim = crm_claim_obj.create(vals)
        return claim
