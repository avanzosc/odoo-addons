import logging

import psycopg2
from sshtunnel import SSHTunnelForwarder

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ConnectDbWizard(models.TransientModel):
    _name = "connect.db.wizard"
    _description = "Wizard to connect to remote DB and compare lines"
    remote_host = fields.Char(string="Remote Host")
    remote_port = fields.Integer(string="Remote Port", default=22)
    remote_user = fields.Char(string="Remote User")
    remote_password = fields.Char(string="Remote Password", password=True)
    db_name = fields.Char(string="Database Name")
    db_user = fields.Char(string="DB User")
    db_password = fields.Char(string="DB Password", password=True)
    limit = fields.Integer(string="Limit")
    exclude_currency = fields.Char(string="Exclude Currency")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        params = self.env["ir.config_parameter"].sudo()
        res["remote_host"] = params.get_param(
            "connect_db_wizard.remote_host", default=""
        )
        res["remote_port"] = int(
            params.get_param("connect_db_wizard.remote_port", default="22")
        )
        res["remote_user"] = params.get_param(
            "connect_db_wizard.remote_user", default=""
        )
        res["remote_password"] = params.get_param(
            "connect_db_wizard.remote_password", default=""
        )
        res["db_name"] = params.get_param("connect_db_wizard.db_name", default="")
        res["db_user"] = params.get_param("connect_db_wizard.db_user", default="")
        res["db_password"] = params.get_param(
            "connect_db_wizard.db_password", default=""
        )
        res["limit"] = params.get_param("connect_db_wizard.limit", default="")
        res["exclude_currency"] = params.get_param(
            "connect_db_wizard.exclude_currency", default=""
        )
        return res

    def action_connect_and_fetch(self):
        params_obj = self.env["ir.config_parameter"].sudo()
        params_obj.set_param("connect_db_wizard.remote_host", self.remote_host or "")
        params_obj.set_param("connect_db_wizard.remote_port", self.remote_port or 22)
        params_obj.set_param("connect_db_wizard.remote_user", self.remote_user or "")
        params_obj.set_param(
            "connect_db_wizard.remote_password", self.remote_password or ""
        )
        params_obj.set_param("connect_db_wizard.db_name", self.db_name or "")
        params_obj.set_param("connect_db_wizard.db_user", self.db_user or "")
        params_obj.set_param("connect_db_wizard.db_password", self.db_password or "")
        params_obj.set_param("connect_db_wizard.limit", self.limit or "")
        params_obj.set_param(
            "connect_db_wizard.exclude_currency", self.exclude_currency or ""
        )

        server = None
        conn = None
        try:
            server = SSHTunnelForwarder(
                (self.remote_host, self.remote_port),
                ssh_username=self.remote_user,
                ssh_password=self.remote_password,
                remote_bind_address=("127.0.0.1", 5432),
            )
            server.start()

            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host="127.0.0.1",
                port=server.local_bind_port,
            )
            cursor = conn.cursor()
            query = """
                SELECT
                    id,
                    debit,
                    credit,
                    amount_currency
                FROM
                    account_move_line
                        """
            if self.exclude_currency:
                query += f" WHERE currency_id != (SELECT id FROM res_currency WHERE name = '{self.exclude_currency}')"

            query += " ORDER BY date DESC"

            if self.limit:
                query += f" LIMIT {self.limit};"
            else:
                query += ";"
            cursor.execute(query)
            results = cursor.fetchall()

            _logger.info(f"SELECT query returned {len(results)} rows.")

            cursor.execute(
                """
                SELECT COUNT(*) FROM account_move_line;
            """
            )
            count_result = cursor.fetchone()
            _logger.info(f"COUNT query returned {count_result[0]} rows.")

            cursor.close()
            conn.close()
            server.stop()

            comparison_obj = self.env["account.move.line.comparison"]
            comparison_obj.search([]).unlink()
            records = []
            for res in results:
                data = {
                    "external_id": res[0],
                    "debit": res[1],
                    "credit": res[2],
                    "amount_currency": res[3],
                }
                comparison_record = comparison_obj.new(data)
                comparison_record._compute_is_debit_different()
                comparison_record._compute_is_credit_different()
                comparison_record._compute_is_amount_currency_different()

                if (
                    comparison_record.is_debit_different
                    or comparison_record.is_credit_different
                    or comparison_record.is_amount_currency_different
                ):
                    records.append(data)

            if records:
                comparison_obj.create(records)

            action = self.env.ref(
                "connect_db_wizard.action_account_move_line_comparison_tree"
            ).read()[0]
            return action

        except Exception as e:
            if conn:
                conn.close()
            if server:
                server.stop()
            raise e
