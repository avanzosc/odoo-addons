# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    fields_list = ["student_progenitor_ids"]
    other_children = env["res.partner"].search([
        ("educational_category", "=", "otherchild")])
    for field in fields_list:
        env.add_todo(other_children._fields[field], other_children)
    other_children.recompute()
