# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import SUPERUSER_ID
from openerp.api import Environment


def uninstall_hook(cr, pool):
    '''
     There is a domain that is not erased when uninstalling so in order to
     avoid problems we reinstall 'event_track_assistant' as the action is
     created in that module.
    '''
    env = Environment(cr, SUPERUSER_ID, {})
    update_module = env['ir.module.module'].search(
        [('name', '=', 'event_track_assistant')])
    update_module.button_upgrade()
