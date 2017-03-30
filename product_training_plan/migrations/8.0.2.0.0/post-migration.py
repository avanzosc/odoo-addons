# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def assign_sequence_to_training_plan(cr):
    cr.execute("""UPDATE training_plan a
                  set sequence = 'TP-' || LPAD((select b.sequence::text
                  from product_training_plan b
                  where b.training_plan_id = a.id), 5, '0');""")
    cr.execute("""UPDATE ir_sequence
                  set number_next = (select
                  COALESCE(max(substring(sequence from 4 for 8)::int),0)+1
                  from training_plan) where code = 'training.plan';""")


def migrate(cr, version):
    if not version:
        return
    assign_sequence_to_training_plan(cr)
