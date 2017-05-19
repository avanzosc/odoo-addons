# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def rename_sequence2code(cr):
    cr.execute("""ALTER TABLE training_plan
                  RENAME COLUMN sequence TO code""")


def migrate(cr, version):
    if not version:
        return
    rename_sequence2code(cr)
