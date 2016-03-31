# -*- coding: utf-8 -*-
# (c) 2015 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, exceptions, api, _
import base64
import csv
import cStringIO


class ImportAccountMove(models.TransientModel):
    _name = 'import.account.move'
    _description = 'Import account move'

    def _get_default_journal(self):
        ctx = self._context
        if 'active_id' in ctx:
            account_obj = self.env['account.move']
            account = account_obj.browse(ctx['active_id'])
        return account.journal_id

    data = fields.Binary('File', required=True)
    name = fields.Char('Filename')
    delimeter = fields.Char('Delimeter', default=',',
                            help='Default delimeter is ","')

    def _get_account_from_partner(self, partner_info, search_by, partner_type):
        """ Returns account id from a given partner info
        @param partner_info: Partner to search
        @param search_by: Key to search partner
        @param partner_type: Define if it is customer or supplier
        @return: partner account id or error message
        """
        partner_obj = self.env['res.partner']
        return_data = {'error': _('Partner not found')}
        if partner_info and search_by and partner_type:
            partner = False
            if partner_type == 'customer':
                partner = partner_obj.search(
                    [(search_by, 'like', partner_info),
                     ('customer', '=', True),
                     ('is_company', '=', True)])[:1]
                if partner:
                    return_data = {
                        'partner_id': partner.id,
                        'account_id': partner.property_account_receivable.id}
            elif partner_type == 'supplier':
                partner = partner_obj.search(
                    [(search_by, 'like', partner_info),
                     ('supplier', '=', True),
                     ('is_company', '=', True)])[:1]
                if partner:
                    return_data = {
                        'partner_id': partner.id,
                        'account_id': partner.property_account_payable.id}
        return return_data

    @api.multi
    def action_import_moves(self):
        """Load Account moves data from the CSV file."""
        self.ensure_one()
        ctx = self._context
        acc_move_obj = self.env['account.move']
        account_obj = self.env['account.account']
        acc_move_line_obj = self.env['account.move.line']
        if 'active_id' in ctx:
            account_move = acc_move_obj.browse(ctx['active_id'])
        if not self.data:
            raise exceptions.Warning(_("You need to select a file!"))
        # Decode the file data
        data = base64.b64decode(self.data)
        file_input = cStringIO.StringIO(data)
        file_input.seek(0)
        reader_info = []
        if self.delimeter:
            delimeter = str(self.delimeter)
        else:
            delimeter = ','
        reader = csv.reader(file_input, delimiter=delimeter,
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        keys = reader_info[0]
        # check if keys exist
        if not isinstance(keys, list) or ('name' not in keys or
                                          'account' not in keys):
            raise exceptions.Warning(
                _("Not 'account' or 'partner' keys found"))
        del reader_info[0]
        values = {}
        for i in range(len(reader_info)):
            line = i + 2
            error_message = False
            field = reader_info[i]
            values = dict(zip(keys, field))
            account_id = False
            account_data = {}
            if not values['name']:
                error_message = _('%s Line Error: Not line name defined'
                                  % line)
                account_move.narration = (
                    (account_move.narration or '') + '\n' + error_message)
                continue
            partner_id = False
            if 'partner_type' in values and values['partner_type']:
                if 'partner_ref' in values and values['partner_ref']:
                    account_data = self._get_account_from_partner(
                        values['partner_ref'], 'ref', values['partner_type'])
                elif 'partner_name' in values and values['partner_name']:
                    account_data = self._get_account_from_partner(
                        values['partner_name'], 'name', values['partner_type'])
                elif 'partner_id' in values and values['partner_id']:
                    account_data = self._get_account_from_partner(
                        values['partner_id'], 'id', values['partner_type'])
                if 'error' in account_data:
                    error_message = (_('%s Line Error:' % line) +
                                     account_data['error'])
                else:
                    account_id = account_data['account_id']
                    partner_id = account_data['partner_id']
            if error_message:
                account_move.narration = (
                    (account_move.narration or '') + '\n' + error_message)
                continue
            if 'account' in values and values['account']:
                account = account_obj.search(
                    [('code', '=', values['account'])])[:1]
                if not account and not account_id:
                    error_message = _('%s Line Error: Account not found: %s' %
                                      (line, values['account']))
                    account_move.narration = (
                        (account_move.narration or '') + '\n' + error_message)
                    continue
                if account:
                    account_id = account.id
            if not account_id:
                error_message = _('%s Line Error: Account is empty' % line)
                account_move.narration = (
                    (account_move.narration or '') + '\n' + error_message)
                continue
            debit = 0
            credit = 0
            if 'debit' in values and values['debit']:
                debit = float(values['debit'].replace(',', '.'))
            if 'credit' in values and values['credit']:
                credit = float(values['credit'].replace(',', '.'))
            if debit < 0 or credit < 0:
                error_message = _('%s Line Error: Wrong amount in account: %s'
                                  % (line, values['account']))
                account_move.narration = (
                    (account_move.narration or '') + '\n' + error_message)
                continue
            line_data = {'account_id': account_id,
                         'name': values['name'],
                         'debit': debit,
                         'credit': credit,
                         'period_id': account_move.period_id.id,
                         'move_id': account_move.id,
                         'journal_id': account_move.journal_id.id,
                         'partner_id': partner_id,
                         }
            if 'date' in values and values['date']:
                line_data.update({'date_maturity': values['date']})
            try:
                acc_move_line_obj.create(line_data)
            except:
                error_message = _('%s Line Error: Wrong Line data, Account: %s'
                                  % (line, values['account']))
                account_move.narration = (
                    (account_move.narration or '') + '\n' + error_message)
                continue
