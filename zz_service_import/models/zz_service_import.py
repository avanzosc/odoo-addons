# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
import base64
import tempfile


try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None


class zzServiceImport(models.Model):
    _name = 'zz.service.import'
    _description = 'ZZ service import'

    filename = fields.Char(string='Filename')
    data = fields.Binary(string='File', required=True)
    file_date = fields.Date(
        string="File Import Date", required=True,
        default=fields.Date.context_today)
    zz_import_lines = fields.One2many(
        comodel_name='zz.service.line.import',
        inverse_name='zz_import_id', string='ZZ Service Import Lines')

    partners_percent_ok = fields.Float()
    partners_percent_error = fields.Float()

    messages_ok = fields.Char()
    messages_error = fields.Char()

    def check_number(self, number):
        try:
            if isinstance(number, int) or isinstance(number, float):
                return number
        except ValueError:
            return 0

    def clear_messages(self):
        self.messages_ok = ''
        self.messages_error = ''

    def action_charge_zz(self):
        for rows in self.zz_import_lines:
            rows.unlink()
        self.partners_percent_ok = 0
        self.partners_percent_error = 0
        self.clear_messages()

        file = base64.decodestring(self.data)
        (fileno, fp_name) = tempfile.mkstemp('.xls', 'odoo_')
        outFile = open(fp_name, 'wb')
        outFile.write(file)
        outFile.close()

        reader = xlrd.open_workbook(fp_name)
        sheet = reader.sheet_by_index(0)
        ctx = self.env.context
        write_line = self.env['zz.service.line.import']

        keys = ['p_shelf', 'p_ref', 'p_name', 'p_pk', 'p_ck',
                'p_nk', 'p_bk', 'p_ak', 'p_qty']
        reader.nrow = 10
        for counter in range(2, sheet.nrows-1):
            rowValues = sheet.row_values(counter+1, 0, 9)
            values = dict(zip(keys, rowValues))
            line_data = {
                'zz_import_id': self.id,
                'shelf_number': self.check_number(values['p_shelf']),
                'partner_ref': values['p_ref'],
                'partner_name': values['p_name'],
                'p': self.check_number(values['p_pk']),
                'c': self.check_number(values['p_ck']),
                'n': self.check_number(values['p_nk']),
                'b': self.check_number(values['p_bk']),
                'a': self.check_number(values['p_ak']),
                'quantity': self.check_number(values['p_qty']),
                }
            try:
                write_line.create(line_data)
            except Exception as error:
                self.messages_error = 'Data upload error!'
        self.messages_ok = 'Data upload success!'

    def action_validate_zz(self):
        counter = -1
        self.clear_messages()

        for fila in self.zz_import_lines:
            counter = counter + 1
            if not(fila.partner_ref or fila.partner_ref.strip()):
                fila.state = 'error'
                fila.log_info = 'Error: The parter reference cannot be empty'
            elif not(fila.partner_name or fila.partner_name.strip()):
                if fila.partner_ref == 'TOTAL' and counter == len(self.zz_import_lines)-1:
                    fila.state = 'pass'
                    fila.log_info = 'Pass: Correct total data'
                else:
                    fila.state = 'error'
                    fila.log_info = 'Error: The parter name cannot be empty'
            else:
                val = self.check_partner(fila.partner_ref, fila.partner_name)
                if val == 0:
                    fila.state = 'warn'
                    fila.log_info = 'Warning: Partner Reference does not exist'
                elif val == 1:
                    fila.state = 'warn'
                    fila.log_info = 'Warning: Partner Reference exists, but not partner Name'
                elif val == 2:
                    fila.state = 'warn'
                    fila.log_info = 'Warning: Partner Reference and Name are not from the same partner'
                else:
                    self.show_id(fila.partner_ref, fila)
                    fila.state = 'pass'
                    fila.log_info = 'Pass: Correct data'
        self.partners_count()
        if self.partners_percent_ok == 100:
            self.messages_ok = 'Data validation completed!'
        else:
            self.messages_error = 'Data validation not completed!'

    def show_id(self, partner_ref, fila):
        all_partners = self.env['res.partner']
        partner_data = all_partners.search([('ref', '=', partner_ref)], limit=1)
        fila.identificator = partner_data.id

    def check_partner(self, partner_ref, partner_name):
        all_partners = self.env['res.partner']
        partner_for_ref = all_partners.search([('ref', '=', partner_ref)], limit=1)
        if partner_for_ref:
            partner_for_name = all_partners.search([('name', '=', partner_name)], limit=1)
            if partner_for_name:
                if partner_for_name.ref == partner_for_ref.ref:
                    return 3  # Ref and name of the same user in BD
                else:
                    return 2  # Ref and name but not of the same user in BD
            else:
                return 1  # Ref in BD but not name
        else:
            return 0  # Ref not in BD

    def partners_count(self):
        count_ok = 0
        count_error = 0

        for fila in self.zz_import_lines:
            if fila.state == 'pass':
                count_ok = count_ok + 1
            elif fila.state == 'warn' or fila.state == 'error':
                count_error = count_error + 1
        self.partners_percent_ok = (count_ok * 100)/(len(self.zz_import_lines))
        self.partners_percent_error = (count_error * 100)/(len(self.zz_import_lines))

    def action_show_partners_ok(self):
        self.partners_count()

    def action_show_partners_error(self):
        self.partners_count()

    def document_validated(self):
        for fila in self.zz_import_lines:
            if fila.state == '2validate' or fila.state == 'error' or fila.state == 'warn':
                return False
        self.partners_percent_ok = 100
        self.partners_percent_error = 0
        return True

    def action_process_zz(self):
        self.clear_messages()
        if not self.document_validated():
            self.messages_error = 'Full document is not validated!'
        else:
            for fila in self.zz_import_lines:
                partner = self.env['res.partner']
                data_partner = partner.search([('ref', '=', fila.partner_ref),
                                               ('name', '=', fila.partner_name)],
                                               limit=1)
                if data_partner:
                    data_partner.write(
                        {'shelf_number': fila.shelf_number,
                         'p': fila.p,
                         'c': fila.c,
                         'n': fila.n,
                         'b': fila.b,
                         'a': fila.a,
                         'quantity': fila.quantity,
                         }
                        )
            self.messages_ok = 'Data stored!'


class partnerZZServiceLineImport(models.Model):
    _name = 'zz.service.line.import'
    _description = 'ZZ service line import'

    zz_import_id = fields.Many2one(comodel_name='zz.service.import',
                                   string='ZZ Service Import', ondelete='cascade', required=True)

    shelf_number = fields.Integer(string='Numero de balda')
    partner_ref = fields.Char(string='Numero de trabajador')
    partner_name = fields.Char(string='Nombre y apellido')
    p = fields.Integer(string='P')
    c = fields.Integer(string='C')
    n = fields.Integer(string='N')
    b = fields.Integer(string='B')
    a = fields.Integer(string='A')
    quantity = fields.Float(string='Importe')
    identificator = fields.Char(string='Partner id')
    partner = fields.Many2one('res.partner', string='Partner')
    log_info = fields.Text(string='Log Info')
    state = fields.Selection([
        ('2validate', 'To validate'),
        ('pass', 'Validated'),
        ('error', 'Error'),
        ('warn', 'Warning')],
        string='State', default='2validate'
    )
