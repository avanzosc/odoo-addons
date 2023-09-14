# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def migrate(cr, version):
    if not version:
        return
    cr.execute("""
        UPDATE account_analytic_billing_plan p
        SET journal_id = (
            SELECT journal_id
            FROM account_invoice i
            WHERE i.id = p.invoice_id)
        WHERE invoice_id IS NOT NULL;
     """)
