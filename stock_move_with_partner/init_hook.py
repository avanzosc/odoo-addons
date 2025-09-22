# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    """
    Hook pre-init para Odoo v18 - recibe solo env como parámetro
    """
    _logger.info("Starting pre_init_hook for stock_move_with_partner")
    
    _logger.info("Checking if partner_id column exists in stock_move_line")
    env.cr.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'stock_move_line' 
        AND column_name = 'partner_id'
    """)
    
    if not env.cr.fetchone():
        _logger.info("Creating partner_id column in stock_move_line")
        env.cr.execute("""
            ALTER TABLE stock_move_line
            ADD COLUMN partner_id integer;
            COMMENT ON COLUMN stock_move_line.partner_id IS 'Destination Address';
        """)
    
    _logger.info("Updating partner_id in stock_move")
    env.cr.execute(
        """
        UPDATE stock_move sm
        SET partner_id = sp.partner_id
        FROM stock_picking sp
        WHERE sm.picking_id = sp.id
          AND sm.partner_id IS NULL
          AND sm.picking_id IS NOT NULL
        """
    )
    
    _logger.info("Updating partner_id in stock_move_line")
    env.cr.execute(
        """
        UPDATE stock_move_line sml
        SET partner_id = sm.partner_id
        FROM stock_move sm
        WHERE sml.move_id = sm.id
          AND sml.move_id IS NOT NULL
        """
    )
    
    _logger.info("Completed pre_init_hook for stock_move_with_partner")