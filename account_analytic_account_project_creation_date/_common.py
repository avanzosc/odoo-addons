# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

import pytz


def _get_local_date(date_to_convert, tz="UTC"):
    if isinstance(date_to_convert, str):
        date_to_convert = datetime.strptime(date_to_convert, "%Y-%m-%d %H:%M:%S")
    local_tz = pytz.timezone(tz)
    if date_to_convert.tzinfo is None:
        date_to_convert = pytz.utc.localize(date_to_convert)
    return date_to_convert.astimezone(local_tz)
