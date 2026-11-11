# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

import pytz

from odoo import api, models

STOCK_MAIL_DEFAULT_TIMEZONE = "Europe/Madrid"


class IrCron(models.Model):
    _inherit = "ir.cron"

    @api.model
    def _get_stock_mail_nextcall(self, nextcall, now, tz_name):
        tz = pytz.timezone(tz_name)
        call_time = pytz.utc.localize(nextcall).astimezone(tz).time()
        local_now = pytz.utc.localize(now).astimezone(tz)
        local_call = tz.localize(datetime.combine(local_now.date(), call_time))
        if local_call <= local_now:
            local_call = tz.localize(
                datetime.combine(local_now.date() + timedelta(days=1), call_time)
            )
        return local_call.astimezone(pytz.utc).replace(tzinfo=None)

    def _reschedule_later(self, job):
        res = super()._reschedule_later(job)
        cron = self.env.ref(
            "stock_partner_daily_mail.ir_cron_send_stock_mail",
            raise_if_not_found=False,
        )
        if cron and job["id"] == cron.id:
            nextcall = self._get_stock_mail_nextcall(
                job["nextcall"],
                datetime.utcnow(),
                cron.user_id.tz or STOCK_MAIL_DEFAULT_TIMEZONE,
            )
            self.env.cr.execute(
                "UPDATE ir_cron SET nextcall = %s WHERE id = %s", [nextcall, cron.id]
            )
        return res
