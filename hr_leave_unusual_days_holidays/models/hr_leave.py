from odoo import api, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    @api.model
    def get_unusual_days(self, date_from, date_to=None):
        # We are overriding the get_unusual_days method
        # to include bank holidays in the list of unusual days
        # The unusual days are the ones that appear in gray
        # on the calendar, while bank holidays are shown on the right.
        # We want to make sure that the bank holidays
        # also appear in gray on the calendar.

        unusual_days = super().get_unusual_days(date_from, date_to)
        employee_id = self.env.context.get("employee_id", False)
        employee = (
            self.env["hr.employee"].browse(employee_id)
            if employee_id
            else self.env.user.employee_id
        )
        special_days = employee.get_special_days_data(date_from, date_to)
        bank_holidays = special_days.get("bankHolidays", [])
        for holiday in bank_holidays:
            date_str = holiday["start"][:10]
            if date_str not in unusual_days:
                unusual_days[date_str] = True
        return unusual_days
