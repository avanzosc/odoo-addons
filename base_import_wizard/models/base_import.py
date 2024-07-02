# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

try:
    import xlrd

    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

IMPORT_STATUS = [
    ("draft", "Draft"),
    ("2validate", "To validate"),
    ("pass", "Validated"),
    ("error", "Error"),
    ("done", "Processed"),
]


def check_number(number):
    try:
        if isinstance(number, float) or isinstance(number, int):
            return number
        if "." in number:
            val = float(number)
        else:
            val = int(number)
        return val
    except ValueError:
        return False


def convert2str(value):
    if isinstance(value, float) or isinstance(value, int):
        new_value = str(value).strip()
        if "." in new_value:
            new_value = new_value[: new_value.index(".")]
        return new_value
    elif isinstance(value, tuple):
        return value[0]
    else:
        return value


class BaseImport(models.AbstractModel):
    _name = "base.import"
    _description = "Abstract Model for Import Wizards"
    _order = "file_date desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        copy=False,
    )
    data = fields.Binary(
        string="File",
        required=True,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    filename = fields.Char(
        string="Filename",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    file_date = fields.Date(
        string="Import Date",
        required=True,
        default=fields.Date.context_today,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    import_line_ids = fields.One2many(
        comodel_name="base.import.line",
        inverse_name="import_id",
        string="Lines to Import",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    state = fields.Selection(
        selection=IMPORT_STATUS,
        compute="_compute_state",
        string="Status",
        store=True,
    )
    log_info = fields.Text(
        string="Log Info",
        compute="_compute_log_info",
    )

    @api.depends("filename", "file_date")
    def _compute_name(self):
        for file_import in self:
            file_import.name = "{} - {}".format(
                file_import.filename, file_import.file_date
            )

    @api.depends(
        "import_line_ids",
        "import_line_ids.state",
    )
    def _compute_state(self):
        for bom_import in self:
            lines = bom_import.import_line_ids
            line_states = lines.mapped("state")
            if line_states and any([state == "error" for state in line_states]):
                bom_import.state = "error"
            elif line_states and all([state == "done" for state in line_states]):
                bom_import.state = "done"
            elif line_states and all([state == "pass" for state in line_states]):
                bom_import.state = "pass"
            elif lines:
                bom_import.state = "2validate"
            else:
                bom_import.state = "draft"

    @api.depends(
        "import_line_ids",
        "import_line_ids.log_info",
    )
    def _compute_log_info(self):
        for bom_import in self:
            lines = bom_import.import_line_ids
            logged_lines = lines.filtered("log_info")
            if logged_lines:
                bom_import.log_info = "\n".join(logged_lines.mapped("log_info"))
            else:
                bom_import.log_info = ""

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        if row_values:
            return {
                "import_id": self.id,
            }
        return False

    def action_import_file(self):
        self.ensure_one()
        self.import_line_ids.unlink()
        book = base64.decodebytes(self.data)
        reader = xlrd.open_workbook(file_contents=book)
        lines = []
        try:
            sheet_list = reader.sheet_names()
            for sheet_name in sheet_list:
                sheet = reader.sheet_by_name(sheet_name)
                keys = [c.value for c in sheet.row(0)]
                for counter in range(1, sheet.nrows):
                    row_values = sheet.row_values(counter, 0, end_colx=sheet.ncols)
                    values = dict(zip(keys, row_values))
                    line_data = self._get_line_values(values)
                    if line_data:
                        lines.append((0, 0, line_data))
            if lines:
                self.import_line_ids = lines
        except Exception:
            raise ValidationError(_("This is not a valid file."))

    def action_validate(self):
        for wiz in self:
            update_values = wiz.mapped("import_line_ids").action_validate()
            wiz.write(
                {
                    "import_line_ids": update_values,
                }
            )
        return True

    def action_process(self):
        for wiz in self:
            update_values = wiz.mapped("import_line_ids").action_process()
            wiz.write(
                {
                    "import_line_ids": update_values,
                }
            )
        return True

    def button_open_import_line(self):
        self.ensure_one()
        return {
            "name": _("Import Lines"),
            "type": "ir.actions.act_window",
            "res_model": self.import_line_ids._name,
            "view_mode": "tree,form",
            "target": "current",
            "domain": [("import_id", "=", self.id)],
            "context": {
                "default_import_id": self.id,
            },
        }


class BaseImportLine(models.AbstractModel):
    _name = "base.import.line"
    _description = "Abstract Model for Import Lines"

    import_id = fields.Many2one(
        comodel_name="base.import",
        string="Import Wizard",
        ondelete="cascade",
        required=True,
    )
    log_info = fields.Text(
        string="Log Info",
    )
    state = fields.Selection(
        selection=IMPORT_STATUS,
        string="Status",
        default="2validate",
        required=True,
        readonly=True,
    )

    def action_validate(self):
        return []

    def action_process(self):
        return []
