# -*- coding: utf-8 -*-
# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def update_reminder_date(cr, registry):
    cr.execute(
        """
        UPDATE account_invoice
        SET payment_reminder_date = date_due
        WHERE type = 'out_invoice'
        AND payment_term IS NOT NULL
        AND state = 'open';
        """)
