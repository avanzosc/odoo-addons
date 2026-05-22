# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import (
    convert2date,
    convert2str,
)


class StockPickingBatchImport(models.Model):
    _name = "stock.picking.batch.import"
    _inherit = "base.import"
    _description = "Wizard to import picking batches"

    import_line_ids = fields.One2many(
        comodel_name="stock.picking.batch.import.line",
    )
    batch_count = fields.Integer(
        string="Batch",
        compute="_compute_batch_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id,
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            batch_entry_date = row_values.get("Entry Date", "")
            batch_entry_date = convert2date(
                batch_entry_date, datemode or 0, timezone_name=None
            )
            if batch_entry_date:
                batch_entry_date = batch_entry_date.date()
            batch_type = row_values.get("Type", "")
            batch_location = row_values.get("Location", "")
            batch_name = row_values.get("Name", "")
            batch_lineage = row_values.get("Lineage", "")
            mother = row_values.get("Mother", "")
            chick_code = row_values.get("Chick Code", "")
            chick_location = row_values.get("Chick Location", "")
            chick_lot = row_values.get("Chick Lot", "")
            chick_qty = row_values.get("Chick Qty", "")
            chicken_code = row_values.get("Chicken Code", "")
            chicken_lot = row_values.get("Chicken Lot", "")
            chicken_qty = row_values.get("Chicken Qty", "")
            medicine_code = row_values.get("Medicine Code", "")
            medicine_location = row_values.get("Medicine Location", "")
            medicine_qty = row_values.get("Medicine Qty", "")
            feed_code = row_values.get("Feed Code", "")
            feed_location = row_values.get("Feed Location", "")
            feed_qty = row_values.get("Feed Qty", "")
            feed_family = row_values.get("Feed Family", "")
            log_info = ""
            if not batch_name:
                return {}
            values.update(
                {
                    "batch_entry_date": batch_entry_date,
                    "batch_type": convert2str(batch_type),
                    "batch_location": convert2str(batch_location),
                    "batch_name": convert2str(batch_name),
                    "batch_lineage": convert2str(batch_lineage),
                    "mother": convert2str(mother),
                    "chick_code": convert2str(chick_code),
                    "chick_location": convert2str(chick_location),
                    "chick_lot": convert2str(chick_lot),
                    "chick_qty": chick_qty,
                    "chicken_code": convert2str(chicken_code),
                    "chicken_lot": convert2str(chicken_lot),
                    "chicken_qty": convert2str(chicken_qty),
                    "medicine_code": convert2str(medicine_code),
                    "medicine_location": convert2str(medicine_location),
                    "medicine_qty": medicine_qty,
                    "feed_code": convert2str(feed_code),
                    "feed_location": convert2str(feed_location),
                    "feed_qty": feed_qty,
                    "feed_family": convert2str(feed_family),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_batch_count(self):
        for record in self:
            record.batch_count = len(record.mapped("import_line_ids.batch_id"))

    def button_open_batch(self):
        self.ensure_one()
        batches = self.mapped("import_line_ids.batch_id")
        action = self.env.ref("stock_picking_batch.stock_picking_batch_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", batches.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class StockPickingBatchImportLine(models.Model):
    _name = "stock.picking.batch.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import batches"

    @api.model
    def _get_selection_batch_type(self):
        return self.env["stock.picking.batch"].fields_get(allfields=["batch_type"])[
            "batch_type"
        ]["selection"]

    import_id = fields.Many2one(
        comodel_name="stock.picking.batch.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
            ("update", "Update"),
        ],
        ondelete={"update": "set default", "create": "set default"},
    )
    batch_id = fields.Many2one(string="Batch", comodel_name="stock.picking.batch")
    batch_entry_date = fields.Date(
        string="Entry Date",
        copy=False,
    )
    batch_name = fields.Char(
        string="Name",
        copy=False,
    )
    batch_location = fields.Char(
        string="Location",
        copy=False,
        required=True,
    )
    batch_lineage = fields.Char(
        string="Lineage",
        copy=False,
        required=True,
    )
    batch_type = fields.Selection(
        selection="_get_selection_batch_type",
        string="Type",
        copy=False,
        required=True,
    )
    mother = fields.Char(
        copy=False,
    )
    batch_location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
    )
    batch_lineage_id = fields.Many2one(
        string="Lineage",
        comodel_name="lineage",
        copy=False,
    )
    chick_code = fields.Char(
        copy=False,
    )
    chick_location = fields.Char(
        copy=False,
    )
    chick_qty = fields.Float(
        copy=False,
    )
    chick_lot = fields.Char(
        copy=False,
    )
    chicken_code = fields.Char(
        copy=False,
    )
    chicken_qty = fields.Float(
        copy=False,
    )
    chicken_lot = fields.Char(
        copy=False,
    )
    medicine_code = fields.Char(
        copy=False,
    )
    medicine_location = fields.Char(
        copy=False,
    )
    medicine_qty = fields.Float(
        copy=False,
    )
    feed_code = fields.Char(
        copy=False,
    )
    feed_location = fields.Char(
        copy=False,
    )
    feed_qty = fields.Float(
        copy=False,
    )
    feed_family = fields.Char(
        copy=False,
    )
    feed_family_id = fields.Many2one(comodel_name="breeding.feed")

    def _action_validate(self):
        self.ensure_one()
        log_info = ""
        batch = location = lineage = feed_family = False
        batch, log_info_batch = self._check_batch()
        if log_info_batch:
            log_info += log_info_batch
        location, log_info_location = self._check_location()
        if log_info_location:
            log_info += log_info_location
        lineage, log_info_lineage = self._check_lineage()
        if log_info_lineage:
            log_info += log_info_lineage
        if self.feed_family:
            feed_family, log_info_feed_family = self._check_feed_family()
            if log_info_feed_family:
                log_info += log_info_feed_family
        state = "error" if log_info else "pass"
        action = "nothing"
        if batch and state != "error":
            action = "update"
        elif state != "error":
            action = "create"
        return {
            "batch_id": batch and batch.id,
            "batch_location_id": location and location.id,
            "batch_lineage_id": lineage and lineage.id,
            "feed_family_id": feed_family and feed_family.id,
            "log_info": log_info,
            "state": state,
            "action": action,
        }

    def _action_process(self):
        self.ensure_one()
        if self.action == "create":
            batch, log_info = self._create_batch()
            if batch:
                batch.action_copy_lineage_rates()
        elif self.action == "update":
            batch, log_info = self._update_batch()
        else:
            return {}
        state = "error" if log_info else "done"
        return {
            "batch_id": batch and batch.id,
            "log_info": log_info,
            "state": state,
        }

    def _check_batch(self):
        self.ensure_one()
        batch_obj = self.env["stock.picking.batch"].sudo()
        search_domain = [("name", "=", self.batch_name)]
        log_info = ""
        batches = batch_obj.search(search_domain)
        if len(batches) > 1:
            batches = False
            log_info = _("Error: More than one batch found")
        return batches and batches[:1], log_info

    def _check_location(self):
        self.ensure_one()
        log_info = ""
        if self.batch_location_id:
            return self.batch_location_id, log_info
        location_obj = self.env["stock.location"].sudo()
        search_domain = [
            "|",
            ("name", "=", self.batch_location),
            ("complete_name", "=", self.batch_location),
            ("usage", "!=", "view"),
        ]
        locations = location_obj.search(search_domain)
        if not locations:
            locations = False
            log_info = _("Error: No origin location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _("Error: More than location found.")
        return locations and locations[:1], log_info

    def _check_lineage(self):
        self.ensure_one()
        log_info = ""
        if self.batch_lineage_id:
            return self.batch_lineage_id, log_info
        lineage_obj = self.env["lineage"].sudo()
        search_domain = [("name", "=", self.batch_lineage)]
        lineages = lineage_obj.search(search_domain)
        if not lineages:
            lineages = False
            log_info = _("Error: No lineage found.")
        elif len(lineages) > 1:
            lineages = False
            log_info = _("Error: More than one lineage found.")
        return lineages and lineages[:1], log_info

    def _check_feed_family(self):
        self.ensure_one()
        log_info = ""
        if self.feed_family_id:
            return self.feed_family_id, log_info
        feed_family_obj = self.env["breeding.feed"].sudo()
        search_domain = [("name", "=", self.feed_family)]
        feed_families = feed_family_obj.search(search_domain)
        if not feed_families:
            feed_families = False
            log_info = _("Error: No feed family found.")
        elif len(feed_families) > 1:
            feed_families = False
            log_info = _("Error: More than one feed family found.")
        return feed_families and feed_families[:1], log_info

    def _create_batch(self):
        self.ensure_one()
        batch, log_info = self._check_batch()
        if not batch and not log_info:
            batch_obj = self.env["stock.picking.batch"].sudo()
            values = self._batch_values()
            values.update({"name": self.batch_name})
            batch = batch_obj.create(values)
            log_info = ""
        elif batch:
            batch = False
            log_info += _("Error: There is other line with this batch.")
        return batch, log_info

    def _update_batch(self):
        self.ensure_one()
        batch = self.batch_id
        values = self._batch_values()
        batch.write(values)
        log_info = ""
        return batch, log_info

    def _batch_values(self):
        vals = {
            "entry_date": self.batch_entry_date,
            "start_date": self.batch_entry_date,
            "batch_type": self.batch_type,
            "location_id": self.batch_location_id.id,
            "feed_family": self.feed_family_id.id,
        }
        if self.batch_type == "mother":
            vals.update({"lineage_id": self.batch_lineage_id.id})
        elif self.batch_type == "breeding":
            lineage = self.env["lineage.percentage"].create(
                {"lineage_id": self.batch_lineage_id.id, "percentage": 100}
            )
            vals.update({"lineage_percentage_ids": [(6, 0, lineage.ids)]})
        return vals
