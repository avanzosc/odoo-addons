from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_last_move_locations_in_lots(cr, registry):
    """
    Set the last move locations for all lots based on the latest stock move line.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    query = """
WITH latest_lines AS (
    SELECT
        lot_id,
        MAX(write_date) AS max_write_date
    FROM
        stock_move_line
    WHERE
        qty_done > 0 AND state = 'done' AND lot_id IS NOT NULL
    GROUP BY
        lot_id
)
SELECT
    sml.lot_id,
    l.name AS location_name,
    ld.name AS location_dest_name
FROM
    stock_move_line sml
INNER JOIN
    latest_lines ll ON sml.lot_id = ll.lot_id AND sml.write_date = ll.max_write_date
INNER JOIN
    stock_location l ON sml.location_id = l.id
INNER JOIN
    stock_location ld ON sml.location_dest_id = ld.id
ORDER BY
    sml.write_date DESC;
    """
    cr.execute(query)
    results = cr.fetchall()

    for _, lot_id, location_name, location_dest_name in results:
        last_move_locations = f"{location_name} - {location_dest_name}"
        env["stock.lot"].browse(lot_id).write(
            {"last_move_locations": last_move_locations}
        )
