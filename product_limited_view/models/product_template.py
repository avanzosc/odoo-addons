# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """ fields_view_get([view_id | view_type='form'])

        Get the detailed composition of the requested view like fields, model,
        view architecture

        :param view_id: id of the view or None
        :param view_type: type of the view to return if view_id is None
                ('form', 'tree', ...)
        :param toolbar: true to include contextual actions
        :param submenu: deprecated
        :return: dictionary describing the composition of the requested view
                (including inherited views and extensions)
        :raise AttributeError:
                * if the inherited view has unknown position to work with other
                  than 'before', 'after', 'inside', 'replace'
                * if some tag other than 'position' is found in parent view
        :raise Invalid ArchitectureError: if there is view type other than
                form, tree, calendar, search etc defined on the structure
        """
        if self.env.user.has_group(
                "product_limited_view.group_product_limited_view"):
            if view_type == "form":
                view_id = self.env.ref("product_limited_view."
                                       "product_template_base_minimal_form").id
            elif view_type == "tree":
                view_id = self.env.ref("product_limited_view."
                                       "product_template_minimal_tree").id
        return super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
