# Copyright 2024 Oihane Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    lines = env["slide.channel.partner"].search(
        [("id", "in", (66475,66476)),
         ("event_id", "!=", False),
         ("event_registration_id", "!=", False)]
    )
    if lines:
        lines._put_event_registration_in_survey_user_input()
