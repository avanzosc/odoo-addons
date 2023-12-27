# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    stored_partner_in_stock_move(cr)


def stored_partner_in_stock_move(cr):
    cr.execute("""
        UPDATE stock_move
        set    partner_id = (SELECT stock_picking.partner_id
                             FROM   stock_picking
                             WHERE  stock_picking.id = stock_move.picking_id)
        WHERE  partner_id is null
          AND  picking_id is not null
    """)
