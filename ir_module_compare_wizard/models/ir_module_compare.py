# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str


class IrModuleImport(models.Model):
    _name = "ir.module.import"
    _inherit = "base.import"
    _description = "Wizard to compare modules"

    import_line_ids = fields.One2many(
        comodel_name="ir.module.import.line",
    )
    module_line_count = fields.Integer(
        string="# Module Lines",
        compute="_compute_module_line_count",
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        print("_get_line_values: ",values)
        if row_values:
            module_technical_name = row_values.get("Name", "")
            module_last_version = row_values.get("LastVersion", "")
            module_website = row_values.get("Website", "")
            module_author = row_values.get("Author", "")
            module_notes = row_values.get("Notes", "")
            log_info = ""
            if (
                not module_technical_name
            ):
                return {}
            print("Before values update: ",values)

            values.update(
                {
                    "module_technical_name": convert2str(module_technical_name),
                    "module_last_version": convert2str(module_last_version),
                    "module_website": convert2str(module_website),
                    "module_author": convert2str(module_author),
                    "module_notes": convert2str(module_notes),
                    "log_info": log_info,
                }
            )
            print("After values update: ",values)

        return values

    def _compute_module_line_count(self):
        for record in self:
            record.module_line_count = len(record.import_line_ids)

    def action_process(self):
        for wiz in self:
            if not wiz.import_inventory_id:
                inventory = wiz._create_inventory()
                wiz.write(
                    {
                        "import_inventory_id": inventory.id,
                    }
                )
        return super().action_process()

    def button_open_modules(self):
        self.ensure_one()
        modules = self.mapped("import_line_ids.import_module_id")
        action = self.env["ir.actions.actions"]._for_xml_id(
            "base.open_module_tree"
        )
        action["domain"] = expression.AND(
            [[("id", "in", modules.ids)], safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(self._context, create=False)
        return action


class IrModuleImportLine(models.Model):
    _name = "ir.module.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import module lines"
    
    import_id = fields.Many2one(
        comodel_name="ir.module.import",
    )
    import_module_id = fields.Many2one(
        comodel_name="ir.module.module",
    )
    import_module_state = fields.Selection(
        related="import_module_id.state",
        store=True,
    )
    action = fields.Selection(
        selection_add=[
            ("install", "Install"),
        ],
        ondelete={"install": "set default"},
    )
    module_technical_name = fields.Char(
        string="Technical Name",
        states={"done": [("readonly", True)]},
        required=True,
    )
    module_last_version = fields.Char(
        string="Last Version",
        states={"done": [("readonly", True)]},
    )
    module_website = fields.Char(
        string="Module Website",
        states={"done": [("readonly", True)]},
    )
    module_author = fields.Char(
        string="Module Author",
        states={"done": [("readonly", True)]},
    )
    module_notes = fields.Char(
        string="Module Notes",
        states={"done": [("readonly", True)]},
    )

    def _action_validate(self):
        self.ensure_one()
        update_values = super()._action_validate()
        log_infos = []
        lot = False
        module, log_info_module = self._check_module()
        if log_info_module:
            log_infos.append(log_info_module)

        state = "error" if log_infos else "pass"
        action = "install" if state != "error" else "nothing"
        update_values.update(
            {
                "import_module_id": module and module.id,              
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        self.ensure_one()
        update_values = super()._action_process()

        return update_values

    def _check_module(self):
        self.ensure_one()
        log_info = ""
        if self.import_module_id:
            return self.import_module_id, log_info
        module_obj = self.env["ir.module.module"]
        if self.module_technical_name:
            search_domain = expression.AND(
                [[("name", "=", self.module_technical_name)]]
            )
        modules = module_obj.search(search_domain)
        if not modules:
            log_info = _("No module %(module_name)s found.") % {
                "module_name": self.module_technical_name,
            }
        return modules, log_info
    
    