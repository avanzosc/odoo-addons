# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute("""
        DELETE FROM mail_mass_mailing_contact
        WHERE email ILIKE '%@nomail.no';
    """)
    cr.execute("""
        UPDATE res_partner
        SET email = ''
        WHERE email ILIKE '%@nomail.no';
    """)
