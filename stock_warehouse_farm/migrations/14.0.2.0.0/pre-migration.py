# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    categ_ids = [
        ("categ_reproductoras", "Reproductoras"),
        ("categ_integracion", "Integración"),
        ("categ_medicinas", "Medicinas"),
        ("categ_piensos", "Piensos"),
        ("categ_harinas", "Harinas"),
        ("categ_incubadora", "Incubadora"),
    ]
    for categ_id in categ_ids:
        res = env["category.type"].search([("name", "=", categ_id[1])])
        if res:
            openupgrade.add_xmlid(
                env.cr, "stock_warehouse_farm", categ_id[0],
                "category.type", res.id, noupdate=False)
    stage_ids = [
        ("stage_new", "Nuevo"),
        ("stage_active", "Activo"),
        ("stage_close", "Cerrado"),
    ]
    for stage_id in stage_ids:
        res = env["picking.batch.stage"].search([("name", "=", stage_id[1])])
        if res:
            openupgrade.add_xmlid(
                env.cr, "stock_warehouse_farm", stage_id[0],
                "picking.batch.stage", res.id, noupdate=False)
