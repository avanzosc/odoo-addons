# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def update_payment_reminder_date(cr):
    cr.execute(
        """
        UPDATE account_invoice
        SET payment_reminder_date = date_due
        WHERE payment_reminder_date IS NULL
        AND type = 'out_invoice'
        AND payment_term IS NOT NULL
        AND state = 'open';
        """)


def migrate(cr, version):
    if not version:
        return
    update_payment_reminder_date(cr)
