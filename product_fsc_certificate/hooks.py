# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    """
    With this pre-init-hook we want to avoid error when creating the UNIQUE
    code constraint when the module is installed and before the post-init-hook
    is launched.
    """
    cr.execute('ALTER TABLE account_invoice '
               'ADD COLUMN is_fsc_certificate BOOLEAN;')
    cr.execute('ALTER TABLE sale_order '
               'ADD COLUMN is_fsc_certificate BOOLEAN;')
    cr.execute('ALTER TABLE stock_picking '
               'ADD COLUMN is_fsc_certificate BOOLEAN;')
