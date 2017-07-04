# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def delete_recomputable_fields(cr):
    cr.execute("UPDATE sale_order SET shipped=False;")
    cr.execute("""UPDATE sale_order SET shipped=True WHERE
    sale_order.procurement_group_id is not null AND NOT EXISTS(
    SELECT * FROM procurement_order po WHERE po.group_id=
    sale_order.procurement_group_id AND po.state not in ('cancel', 'done'));
    """)


def migrate(cr, version):
    if not version:
        return
    delete_recomputable_fields(cr)
