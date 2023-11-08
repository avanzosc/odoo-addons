# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64
import logging
import os
from io import BytesIO, StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    csv = None

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

FILE_TYPE_DICT = {
    "text/csv": ("csv", True, None),
    "application/vnd.ms-excel": ("xls", xlrd, "xlrd"),
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
        "xlsx",
        xlsx,
        "xlrd >= 1.0.0",
    ),
}
EXTENSIONS = {
    "." + ext: handler for mime, (ext, handler, req) in FILE_TYPE_DICT.items()
}


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
            elif line_states and all(
                [state in ("pass", "done") for state in line_states]
            ):
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

    def _read_csv(self):
        lines = []
        import_file = BytesIO(base64.decodebytes(self.data))
        file_read = StringIO(import_file.read().decode())
        dialect = csv.Sniffer().sniff(file_read.read(2048))
        file_read.seek(0)
        reader = csv.DictReader(
            file_read, quotechar=dialect.quotechar, delimiter=dialect.delimiter
        )
        for entry in reader:
            line_data = self._get_line_values(entry)
            if line_data:
                lines.append((0, 0, line_data))
        return lines

    def _read_xls(self):
        lines = []
        workbook = xlrd.open_workbook(file_contents=base64.decodebytes(self.data))
        sheet_list = workbook.sheet_names()
        for sheet_name in sheet_list:
            sheet = workbook.sheet_by_name(sheet_name)
            if not sheet.nrows:
                continue
            keys = [c.value for c in sheet.row(0)]
            for counter in range(1, sheet.nrows):
                row_values = sheet.row_values(counter, 0, end_colx=sheet.ncols)
                values = dict(zip(keys, row_values))
                line_data = self._get_line_values(values)
                if line_data:
                    lines.append((0, 0, line_data))
        return lines

    # use the same method for xlsx and xls files
    _read_xlsx = _read_xls

    def _read_file(
        self,
    ):
        """
        Dispatch to specific method to read file content, according to its mimetype
        or file type
        """
        self.ensure_one()
        # guess mimetype from file content
        mimetype = guess_mimetype(self.data or b"")
        (file_extension, handler, req) = FILE_TYPE_DICT.get(
            mimetype, (None, None, None)
        )
        if handler:
            try:
                return getattr(self, "_read_" + file_extension)()
            except Exception:
                _logger.warning(
                    "Failed to read file '%s' using guessed mimetype %s",
                    self.filename or "<unknown>",
                    mimetype,
                )

        # fallback on file extensions as mime types can be unreliable (e.g.
        # software setting incorrect mime types, or non-installed software
        # leading to browser not sending mime types)
        if self.filename:
            p, ext = os.path.splitext(self.filename)
            ext = ext.lower()
            if ext in EXTENSIONS:
                try:
                    return getattr(self, "_read_" + ext[1:])()
                except Exception:
                    _logger.warning(
                        "Failed to read file '%s' using file extension", self.filename
                    )
        if req:
            raise UserError(
                _(
                    'Unable to load "{extension}" file: requires Python module "{modname}"'
                ).format(extension=file_extension, modname=req)
            )
        raise UserError(
            _("Unsupported file format, import only supports CSV, XLS and XLSX")
        )

    def action_import_file(self):
        self.ensure_one()
        self.import_line_ids.unlink()
        lines = self._read_file()
        if not lines:
            raise ValidationError(_("This is not a valid file."))
        self.import_line_ids = lines
        return True

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
    log_info = fields.Text()
    state = fields.Selection(
        selection=IMPORT_STATUS,
        string="Status",
        default="2validate",
        required=True,
        readonly=True,
    )
    action = fields.Selection(
        selection=[
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )

    def _action_validate(self):
        self.ensure_one()
        return {}

    def action_validate(self):
        line_values = []
        for line in self.filtered(lambda ln: ln.state != "done"):
            line_values.append(
                (
                    1,
                    line.id,
                    line._action_validate(),
                )
            )
        return line_values

    def button_validate(self):
        for line in self.filtered(lambda ln: ln.state != "done"):
            line.write(line._action_validate())

    def _action_process(self):
        self.ensure_one()
        update_values = {}
        if self.action == "nothing":
            update_values.update(
                {
                    "state": "done",
                }
            )
        return update_values

    def action_process(self):
        line_values = []
        for line in self.filtered(lambda ln: ln.state == "pass"):
            line_values.append(
                (
                    1,
                    line.id,
                    line._action_process(),
                )
            )
        return line_values

    def button_process(self):
        for line in self.filtered(lambda ln: ln.state == "pass"):
            line.write(line._action_process())
