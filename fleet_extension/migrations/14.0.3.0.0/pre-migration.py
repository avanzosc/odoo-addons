# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        UPDATE fleet_vehicle
        set    product_id = (SELECT stock_production_lot.product_id
                             FROM   stock_production_lot
                             WHERE  stock_production_lot.id = fleet_vehicle.serial_number_id)
    """
    )
