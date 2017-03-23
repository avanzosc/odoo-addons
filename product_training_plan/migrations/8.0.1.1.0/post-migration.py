# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def assign_category_to_training_plan(cr):
    cr.execute("""UPDATE training_plan
                  set category_id = (select id
                                     from training_plan_category
                                     where name = 'Training');""")


def migrate(cr, version):
    if not version:
        return
    assign_category_to_training_plan(cr)
