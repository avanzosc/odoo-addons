# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def delete_product_trainint_plan_constraint(cr):
    cr.execute("""ALTER TABLE product_training_plan
                  DROP CONSTRAINT IF EXISTS
                  product_training_plan_product_training_plan_unique""")


def migrate(cr, version):
    if not version:
        return
    delete_product_trainint_plan_constraint(cr)
