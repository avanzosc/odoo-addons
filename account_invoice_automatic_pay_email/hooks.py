# -*- coding: utf-8 -*-
# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def post_init_hook(cr, pool):
    cr.execute(
        """
        UPDATE account_invoice
        SET payment_reminder_date = date_due;
        """)
