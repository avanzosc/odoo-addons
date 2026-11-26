# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.sale_product_attribute_hidden.controllers.combo_configurator import (
    HiddenAttributeComboConfiguratorMixin,
)
from odoo.addons.website_sale.controllers import combo_configurator


class WebsiteSaleComboConfiguratorController(
    HiddenAttributeComboConfiguratorMixin,
    combo_configurator.WebsiteSaleComboConfiguratorController,
):
    pass
