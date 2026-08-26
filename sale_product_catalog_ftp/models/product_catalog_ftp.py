# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import ftplib
import os

from odoo import fields, models

FTP_TIMEOUT = 30


class ProductCatalogFtp(models.Model):
    _name = "product.catalog.ftp"
    _description = "Product Catalog FTP upload"

    active = fields.Boolean(default=True)
    catalog_id = fields.Many2one(
        comodel_name="product.catalog",
        string="Product Catalog",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        ondelete="cascade",
    )
    ftp_server = fields.Char()
    ftp_user = fields.Char()
    ftp_password = fields.Char()
    ftp_folder = fields.Char(default="/")
    ftp_error = fields.Text(readonly=True)

    _sql_constraints = [
        (
            "catalog_partner_uniq",
            "unique (catalog_id,partner_id)",
            "There is already an FTP upload defined for this catalog and customer.",
        )
    ]

    def _get_local_folder(self):
        self.ensure_one()

        params = self.env["ir.config_parameter"].sudo()
        folder_name = params.get_param(
            "sale_product_catalog_ftp.base_ftp_folder", default="ftp_catalog"
        )

        local_folder = os.path.join(
            os.path.expanduser("~/"),
            folder_name,
            str(self.partner_id.id),
            str(self.catalog_id.id),
        )

        if not os.path.exists(local_folder):
            os.makedirs(local_folder)
        return local_folder

    def _get_datas_fname(self):
        self.ensure_one()
        return "catalog_{}.xlsx".format(self.catalog_id.name.replace(" ", "_"))

    def empty_local_folder(self):
        for record in self:
            local_folder = record._get_local_folder()
            for file_name in os.listdir(local_folder):
                file_path = os.path.join(local_folder, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def upload_file(self, filename):
        self.ensure_one()
        ftp_error = ""
        datas_fname = self._get_datas_fname()
        try:
            ftp_server = ftplib.FTP(
                self.ftp_server, self.ftp_user, self.ftp_password, timeout=FTP_TIMEOUT
            )
            with open(filename, "rb") as file:
                server_filename = os.path.join(self.ftp_folder or "/", datas_fname)
                ftp_server.storbinary(f"STOR {server_filename}", file)
            ftp_server.quit()
        except Exception as e:
            ftp_error = str(e)
        self.write({"ftp_error": ftp_error})
        return True

    def remove_ftp_file(self):
        self.ensure_one()
        ftp_error = ""
        datas_fname = self._get_datas_fname()
        server_filename = os.path.join(self.ftp_folder or "/", datas_fname)
        try:
            ftp_server = ftplib.FTP(
                self.ftp_server, self.ftp_user, self.ftp_password, timeout=FTP_TIMEOUT
            )
            ftp_server.delete(server_filename)
            ftp_server.quit()
        except Exception as e:
            ftp_error = str(e)
        self.write({"ftp_error": ftp_error})
        return True

    def create_catalog(self):
        self.ensure_one()

        local_folder = self._get_local_folder()
        self.empty_local_folder()

        datas_fname = self._get_datas_fname()
        filename = os.path.join(local_folder, datas_fname)

        render_data = {
            "partner_id": self.partner_id.id,
            "catalog_id": self.catalog_id.id,
        }
        data, _report_type = self.env["ir.actions.report"]._render(
            "sale_product_catalog_ftp.product_catalog_xlsx_report",
            self.catalog_id.ids,
            data=render_data,
        )

        with open(filename, "wb") as xlsx_file:
            xlsx_file.write(data)

        if self.ftp_server and self.ftp_user and self.ftp_password:
            self.upload_file(filename)
        return True

    def write(self, values):
        deactivating_or_reassigning = (
            ("active" in values and not values["active"])
            or "partner_id" in values
            or "catalog_id" in values
        )
        if deactivating_or_reassigning:
            for record in self:
                record.empty_local_folder()
                record.remove_ftp_file()
        return super().write(values)

    def unlink(self):
        for record in self:
            record.empty_local_folder()
            record.remove_ftp_file()
        return super().unlink()

    def _create_catalog_file_cron(self):
        for upload_catalog in self.search([]):
            upload_catalog.create_catalog()
