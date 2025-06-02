from . import models


def _pre_init_purchase_fleet(cr):
    """Allow installing in databases with large purchase.order.line table (>1M records)
    - Creating the computed+stored field purchase_order_line.purchase_vehicle_id
      can be terribly slow with the ORM and leads to "Out of Memory" crashes
    """
    cr.execute(
        """ALTER TABLE "purchase_order_line"
                   ADD COLUMN "purchase_vehicle_id" integer;"""
    )
    cr.execute(
        """UPDATE purchase_order_line pol
                     SET purchase_vehicle_id = (
                        SELECT vehicle_id
                          FROM account_analytic_account aa
                         WHERE aa.id = pol.account_analytic_id
                     )
                     WHERE account_analytic_id IS NOT NULL;"""
    )
