from odoo import _, api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _update_number_of_packages(self):
        """Actualizar el campo number_of_packages basado en packages_qty."""
        for picking in self:
            picking.number_of_packages = picking.packages_qty

    @api.onchange("packages_qty")
    def _onchange_picking_packages_qty(self):
        self._update_number_of_packages()

    def action_create_package(self):
        super_result = super().action_create_package()
        self._update_number_of_packages()
        return super_result

    def _action_generate_number_of_packages_wizard(self):
        self.ensure_one()
        view = self.env.ref("delivery_package_number.view_number_package_validate")
        return {
            "name": _("Set number of packages"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "stock.number.package.validate.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": dict(
                self.env.context,
                default_pick_ids=[(4, p.id) for p in self],
                default_number_of_packages=self.number_of_packages,
            ),
        }

    def _get_pickings_to_set_number_of_packages(self):
        """Get the pickings that need the wizard to fill in the number of packages,
        regardless of whether number_of_packages is 0 or not."""
        pickings_to_set_number_of_packages = (
            super()._get_pickings_to_set_number_of_packages()
        )
        for picking in self:
            pickings_to_set_number_of_packages |= picking
        return pickings_to_set_number_of_packages
