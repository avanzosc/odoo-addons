# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute(
        "DELETE FROM slide_channel_partner a"
        "      USING slide_channel_partner b"
        "      WHERE a.id > b.id"
        "      AND a.channel_id = b.channel_id"
        "      AND a.event_registration_id = b.event_registration_id"
        "      AND a.partner_id = b.partner_id;"
    )
