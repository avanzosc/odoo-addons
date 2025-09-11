# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import date, datetime

import xlrd

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import check_number, convert2str


class AccountAssetLineImport(models.Model):
    _name = "account.asset.line.import"
    _inherit = "base.import"
    _description = "Wizard to import account asset lines"

    import_line_ids = fields.One2many(
        comodel_name="account.asset.line.import.line",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id,
        states={"done": [("readonly", True)]},
    )
    account_asset_count = fields.Integer(
        string="# Account Asset",
        compute="_compute_account_asset_count",
    )
    search_asset_by_ref = fields.Boolean(
        string="Search Asset By Reference",
        default=False,
        states={"done": [("readonly", True)]},
    )
    update_data = fields.Boolean(
        string="Update Data",
        default=False,
        states={"done": [("readonly", True)]},
    )

    def _compute_account_asset_count(self):
        for record in self:
            record.account_asset_count = len(
                record.mapped("import_line_ids.account_asset_id")
            )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            reference = row_values.get("Reference", "")
            name = row_values.get("Name", "")
            asset_date = row_values.get("Date Start", "")
            if asset_date:
                asset_date = xlrd.xldate.xldate_as_datetime(asset_date, 0).date()
            purchase_value = row_values.get("Purchase Value", "")
            profile = row_values.get("Category", "")
            date = row_values.get("Date", "")
            if date:
                try:
                    date = float(date)
                    date = xlrd.xldate.xldate_as_datetime(date, 0).date()
                except Exception:
                    if date:
                        date = datetime.strptime(date, "%d/%m/%Y").date()
            amount = row_values.get("Amount", "")
            account_analytic = row_values.get("Account Analytic", "")
            log_info = ""
            values.update(
                {
                    "account_asset_ref": convert2str(reference),
                    "account_asset_name": convert2str(name),
                    "asset_date": asset_date or False,
                    "purchase_value": check_number(purchase_value),
                    "profile": convert2str(profile),
                    "date": date or False,
                    "amount": check_number(amount),
                    "account_analytic": convert2str(account_analytic),
                    "log_info": log_info,
                }
            )
        return values

    def button_open_account_asset(self):
        self.ensure_one()
        account_assets = self.mapped("import_line_ids.account_asset_id")
        action = self.env.ref("account_asset_management.account_asset_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "=", account_assets.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_validate(self):
        result = super(AccountAssetLineImport, self).action_validate()
        for line in self.import_line_ids.filtered(
            lambda c: c.state not in ("error", "done")
        ):
            log_info = ""
            if line.account_asset_id and line.date and line.amount:
                same_asset_lines = self.import_line_ids.filtered(
                    lambda c: c.account_asset_id == line.account_asset_id
                )
                if same_asset_lines:
                    if any([line.state == "error" for line in same_asset_lines]):
                        log_info = _(
                            "There are lines with with errors for " + "the same asset."
                        )
                    if round(sum(same_asset_lines.mapped("amount")), 2) != round(
                        line.account_asset_id.depreciation_base, 2
                    ):
                        log_info = _(
                            "The sum of the amount of the same asset has"
                            + " to be the same as the depreciation base amount."
                        )
            if log_info:
                line.log_info = log_info
                line.write(
                    {
                        "log_info": log_info,
                        "state": "error",
                        "action": "nothing",
                    }
                )
        return result


class AccountAssetLineImportLine(models.Model):
    _name = "account.asset.line.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import account asset lines"

    import_id = fields.Many2one(
        comodel_name="account.asset.line.import",
        copy=False,
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
    )
    account_asset_id = fields.Many2one(
        string="Account Asset",
        comodel_name="account.asset",
    )
    account_asset_ref = fields.Char(
        string="Account Asset Ref",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_asset_name = fields.Char(
        string="Account Asset Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    asset_date = fields.Date(
        string="Asset Start Date",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_value = fields.Float(
        string="Purchase Value",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    profile_id = fields.Many2one(
        string="Category",
        comodel_name="account.asset.profile",
    )
    profile = fields.Char(
        string="Category Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date = fields.Date(
        string="Date",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    amount = fields.Float(
        string="Amount",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_analytic = fields.Char(
        string="Account Analytic",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_analytic_id = fields.Many2one(
        string="Account Analytic",
        comodel_name="account.analytic.account",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        profile = account_analytic = False
        account_asset, log_info_account_asset = self._check_account_asset()
        if not account_asset:
            if (
                self.asset_date
                and self.purchase_value
                and (self.profile or self.profile_id)
            ):
                profile, log_info_profile = self._check_profile()
                if log_info_profile:
                    log_infos.append(log_info_profile)
            else:
                log_infos.append(_("Error: Some field is missing to create the asset."))
        if self.account_analytic:
            account_analytic, log_info_account_analytic = self._check_account_analytic()
            if log_info_account_analytic:
                log_infos.append(log_info_account_analytic)
        if log_info_account_asset:
            log_infos.append(log_info_account_asset)
        if (
            account_asset
            and not log_info_account_asset
            and (account_asset.state != "draft")
            and not self.import_id.update_data
        ):
            log_infos.append(_("Error: The asset is not in draft state."))
        if (
            account_asset
            and not log_info_account_asset
            and (account_asset.state == "draft")
            and not self.import_id.update_data
        ):
            account_asset.depreciation_line_ids.filtered(
                lambda c: c.type == "depreciate"
            ).unlink()
        if (
            account_asset
            and self.date
            and account_asset.date_start
            and (account_asset.date_start > self.date)
            and not self.import_id.update_data
        ):
            log_infos.append(
                _("Error: The date can't be before than the asset date start.")
            )
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "account_asset_id": account_asset and account_asset.id,
                "profile_id": profile and profile.id,
                "account_analytic_id": account_analytic and account_analytic.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        log_info = ""
        if self.action == "create" and self.state not in ("error", "done"):
            if not self.account_asset_id:
                account_asset, log_info = self._check_account_asset()
                if not account_asset and not log_info:
                    if self.account_asset_name:
                        account_asset, log_info = self._create_account_asset()
                        self.account_asset_id = account_asset.id
                    else:
                        log_info = _("To create the asset, the name is required.")
            if self.account_asset_id and self.import_id.update_data:
                self._update_account_asset_values()
            if (
                self.account_asset_id
                and self.date
                and self.amount
                and not self.import_id.update_data
            ):
                same_asset_lines = self.import_id.import_line_ids.filtered(
                    lambda c: c.account_asset_id == self.account_asset_id
                )
                if same_asset_lines:
                    if any([line.state == "error" for line in same_asset_lines]):
                        log_info = _(
                            "There are lines with with errors for" + " the same asset."
                        )
                    if round(sum(same_asset_lines.mapped("amount")), 2) != round(
                        self.account_asset_id.depreciation_base, 2
                    ):
                        log_info = _(
                            "The sum of the amount of the same asset has to"
                            + " be the same as the depreciation base amount."
                        )
            if (
                self.account_asset_id
                and self.date
                and self.amount
                and not (log_info)
                and not self.import_id.update_data
            ):
                self._create_account_asset_line()
            state = "error" if log_info else "done"
            update_values.update(
                {
                    "state": state,
                    "log_info": log_info,
                }
            )
        return update_values

    def _check_account_asset(self):
        self.ensure_one()
        log_info = ""
        if self.account_asset_id:
            return self.account_asset_id, log_info
        account_asset_obj = self.env["account.asset"]
        search_domain = [("name", "=", self.account_asset_name)]
        if self.account_asset_ref:
            search_domain = expression.AND(
                [[("code", "=", self.account_asset_ref)], search_domain]
            )
            if self.import_id.search_asset_by_ref:
                search_domain = [("code", "=", self.account_asset_ref)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            account_asset_obj = account_asset_obj.with_company(
                self.import_id.company_id
            )
        assets = account_asset_obj.search(search_domain)
        if not assets:
            assets = False
        elif len(assets) > 1:
            assets = False
            log_info = _("Error: More than one asset found.")
        return assets and assets[:1], log_info

    def _check_account_analytic(self):
        self.ensure_one()
        log_info = ""
        if self.account_analytic_id:
            return self.account_analytic_id, log_info
        account_analytic_obj = self.env["account.analytic.account"]
        search_domain = [("code", "=", self.account_analytic)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            account_analytic_obj = account_analytic_obj.with_company(
                self.import_id.company_id
            )
        account_analytics = account_analytic_obj.search(search_domain)
        if not account_analytics:
            account_analytics = False
            log_info = _("Error: Account analytic not found.")
        elif len(account_analytics) > 1:
            account_analytics = False
            log_info = _("Error: More than one account analytic found.")
        return account_analytics and account_analytics[:1], log_info

    def _check_profile(self):
        self.ensure_one()
        log_info = ""
        if self.profile_id:
            return self.profile_id, log_info
        profile_obj = self.env["account.asset.profile"]
        search_domain = [("name", "=", self.profile)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            profile_obj = profile_obj.with_company(self.import_id.company_id)
        profiles = profile_obj.search(search_domain)
        if not profiles:
            profiles = False
            log_info = _("Error: Profile not found found.")
        elif len(profiles) > 1:
            profiles = False
            log_info = _("Error: More than one profile found.")
        return profiles and profiles[:1], log_info

    def _account_asset_line_vals(self):
        self.ensure_one()
        vals = {
            "line_date": self.date,
            "amount": self.amount,
            "type": "depreciate",
            "asset_id": self.account_asset_id.id,
        }
        today_year = date.today().year
        if self.date and self.date.year < today_year:
            vals.update(
                {
                    "init_entry": True,
                }
            )
        return vals

    def _create_account_asset_line(self):
        self.ensure_one()
        vals = self._account_asset_line_vals()
        asset_line = self.env["account.asset.line"].create(vals)
        return asset_line

    def _account_asset_vals(self):
        self.ensure_one()
        vals = {
            "name": self.account_asset_name,
            "code": self.account_asset_ref,
            "purchase_value": self.purchase_value,
            "date_start": self.asset_date,
            "profile_id": self.profile_id.id,
            "method_time": self.profile_id.method_time,
            "annual_percentage": self.profile_id.annual_percentage,
            "method_period": self.profile_id.method_period,
            "method": self.profile_id.method,
            "prorata": self.profile_id.prorata,
            "days_calc": self.profile_id.days_calc,
            "use_leap_years": self.profile_id.use_leap_years,
            "account_analytic_id": self.account_analytic_id.id
            or self.profile_id.account_analytic_id.id,
        }
        return vals

    def _create_account_asset(self):
        self.ensure_one()
        asset, log_info = self._check_account_asset()
        if not asset and not log_info:
            asset_obj = self.env["account.asset"]
            values = self._account_asset_vals()
            asset = asset_obj.with_company(self.import_id.company_id).create(values)
            log_info = ""
        return asset, log_info

    def _update_account_asset_values(self):
        self.ensure_one()
        self.account_asset_id.write(
            {"account_analytic_id": self.account_analytic_id.id}
        )
