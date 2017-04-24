# -*- coding: utf-8 -*-
# (c) 2016 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, exceptions, api, _
import base64
import csv
import cStringIO


class ImportAccountMove(models.TransientModel):
    _name = 'import.account.move'
    _description = 'Import account move'

    data = fields.Binary('File', required=True)
    name = fields.Char('Filename')
    delimeter = fields.Char('Delimeter', default=',',
                            help='Default delimeter is ","')

    def _get_account_from_partner(self, partner_info, search_by, operator,
                                  partner_type):
        """ Returns account id from a given partner info
        @param partner_info: Partner to search
        @param search_by: Key to search partner
        @param operator: Operator for the search
        @param partner_type: Define if it is customer or supplier
        @return: partner account id or error message
        """
        partner_obj = self.env['res.partner']
        return_data = {'error': _('Partner not found')}
        if partner_info and search_by and partner_type:
            if partner_type == 'customer':
                partner = partner_obj.search(
                    [(search_by, operator, partner_info),
                     ('customer', '=', True),
                     ('is_company', '=', True)])[:1]
                if partner:
                    return_data = {
                        'partner_id': partner.id,
                        'account_id': partner.property_account_receivable.id}
            elif partner_type == 'supplier':
                partner = partner_obj.search(
                    [(search_by, operator, partner_info),
                     ('supplier', '=', True),
                     ('is_company', '=', True)])[:1]
                if partner:
                    return_data = {
                        'partner_id': partner.id,
                        'account_id': partner.property_account_payable.id}
        return return_data

    def _check_error_data(self, values):
        account_data = {}
        if not values['name']:
            account_data = {'error': _(u'Not line name defined')}
            return account_data
        account_obj = self.env['account.account']
        currency_obj = self.env['res.currency']
        if 'partner_type' in values and values['partner_type']:
            if 'partner_ref' in values and values['partner_ref']:
                account_data = self._get_account_from_partner(
                    values['partner_ref'], 'ref', 'like',
                    values['partner_type'])
            elif 'partner_name' in values and values['partner_name']:
                account_data = self._get_account_from_partner(
                    values['partner_name'], 'name', 'like',
                    values['partner_type'])
            elif 'partner_id' in values and values['partner_id']:
                account_data = self._get_account_from_partner(
                    values['partner_id'], 'id', '=', values['partner_type'])
        if not account_data:
            account = False
            if 'account' in values and values['account']:
                account = account_obj.search(
                    [('code', '=', values['account'])])[:1]
            account_data = account and {'account_id': account.id} or \
                {'error': _(u'Account not found')}
        if 'error' not in account_data:
            debit = credit = 0
            if 'debit' in values and values['debit']:
                account_data['debit'] = debit = float(
                    values['debit'].replace(',', '.'))
            if 'credit' in values and values['credit']:
                account_data['credit'] = credit = float(
                    values['credit'].replace(',', '.'))
            if debit < 0 or credit < 0:
                account_data = {'error': _("Wrong amount in account")}
                return account_data
            if ('currency' in values and values['currency'] and
                    'amount_currency' in values and values['amount_currency']):
                currency_id = currency_obj.search(
                    [('name', 'ilike', values['currency'])])[:1]
                if currency_id:
                    account_data['currency_id'] = currency_id.id
                    account_data['amount_currency'] = float(
                        values['amount_currency'].replace(',', '.'))
                else:
                    account_data = {'error': _("Wrong currency code")}
                    return account_data
        return account_data

    @api.multi
    def action_import_moves(self):
        """Load Account moves data from the CSV file."""
        ctx = self.env.context
        acc_move_obj = self.env['account.move']
        acc_move_line_obj = self.env['account.move.line']
        if 'active_id' in ctx:
            account_move = acc_move_obj.browse(ctx['active_id'])
        else:
            raise exceptions.Warning(_("You need to select an account move"))
        # Decode the file data
        data = base64.b64decode(self.data)
        file_input = cStringIO.StringIO(data)
        file_input.seek(0)
        reader_info = []
        delimeter = self.delimeter and str(self.delimeter) or ','
        reader = csv.reader(file_input, delimiter=delimeter,
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        keys = [x.lower() for x in reader_info[0]]
        # check if keys exist
        if not isinstance(keys, list) or 'name' not in keys:
            raise exceptions.Warning(
                _("Not 'account' or 'partner' keys found"))
        del reader_info[0]
        values = {}
        account_move.narration = "No errors found"
        final_error_msg = u"Error Log:"
        for i in range(len(reader_info)):
            line = i + 1
            error_message = account_id = False
            field = reader_info[i]
            values = dict(zip(keys, field))
            account_data = {}
            partner_id = False
            account_data = self._check_error_data(values)
            if 'error' in account_data:
                error_message = u"{}. {} {}".format(
                    line, _(u'Line Error:'), account_data['error'])
            else:
                account_id = account_data['account_id']
                if 'partner_id' in account_data:
                    partner_id = account_data['partner_id']
            if error_message:
                final_error_msg = u"{} \n {}".format(
                    final_error_msg, error_message)
                continue
            line_data = {
                'account_id': account_id,
                'name': values['name'],
                'debit': account_data.get('debit', 0),
                'credit': account_data.get('credit', 0),
                'period_id': account_move.period_id.id,
                'move_id': account_move.id,
                'journal_id': account_move.journal_id.id,
                'partner_id': partner_id,
                'currency_id': account_data.get('currency_id', False),
                'amount_currency': account_data.get('amount_currency', False)
                }
            if 'date' in values and values['date']:
                line_data.update({'date_maturity': values['date']})
            try:
                acc_move_line_obj.create(line_data)
            except Exception as error:
                self._cr.commit()
                raise exceptions.Warning(u"Line Error:{} \n {}".format(
                    line, error.message or error.value))
        account_move.narration = (final_error_msg == u"Error Log:" and
                                  u'No errors found' or final_error_msg)
