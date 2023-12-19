# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    mail_lists = env["mail.mass_mailing.list"].search([
        ("group_id", "!=", False)])
    mail_lists.write({
        "dynamic": True,
    })
    mail_lists.button_update_domain()
    mail_lists.action_sync()
