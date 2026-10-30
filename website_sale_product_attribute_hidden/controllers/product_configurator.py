# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.sale_product_attribute_hidden.controllers.product_configurator import (
    HiddenAttributeProductConfiguratorMixin,
)
from odoo.addons.website_sale.controllers import product_configurator


class WebsiteSaleProductConfiguratorController(
    HiddenAttributeProductConfiguratorMixin,
    product_configurator.WebsiteSaleProductConfiguratorController,
):
    pass
