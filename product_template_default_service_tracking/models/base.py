from odoo import models


class BaseModelOnchangeMixin(models.AbstractModel):
    _inherit = "base"

    def onchange(self, values, field_name, field_onchange):
        res = super().onchange(values, field_name, field_onchange)
        if (
            self._name == "product.template"
            and res["value"].get("service_tracking") == "no"
        ):
            res["value"]["service_tracking"] = "project_only"
        return res
