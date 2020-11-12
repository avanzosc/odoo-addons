
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date, datetime, timedelta


class PortalFilters(CustomerPortal):

    # Recalculates pager values by request params
    def recalculatePager(self, pager, **kw):
        if len(kw) == 0:
            return pager
        if '?' not in pager['page']['url']:
            synbol = '?'
        else:
            synbol = ''
        page_filter = ''
        for key, value in kw.items():
            if key == 'customer':
                page_filter += '&customer=' + str(value)
            if key == 'date_type':
                page_filter += '&date_type=' + str(value)
            if key == 'date':
                page_filter += '&date=' + str(value)
            if key == 'date_from':
                page_filter += '&date_from=' + str(value)
            if key == 'date_to':
                page_filter += '&date_to=' + str(value)
            if key == 'state':
                page_filter += '&state=' + str(value)
            if key == 'customer_search':
                page_filter += '&customer_search=' + str(value)
        pager['page']['url'] = pager['page']['url'] + synbol + page_filter
        pager['page_start']['url'] = pager['page_start'][
            'url'] + synbol + page_filter
        pager['page_previous']['url'] = pager['page_previous'][
            'url'] + synbol + page_filter
        pager['page_next']['url'] = pager['page_next'][
            'url'] + synbol + page_filter
        pager['page_end']['url'] = pager['page_end'][
            'url'] + synbol + page_filter
        for page in pager['pages']:
            page['url'] = page['url'] + synbol + page_filter
        return pager

    # Checks if a date is contained in a range of dates
    def filter_by_days(self, total_days, check_date):
        first_day = date.today() - timedelta(days=total_days.days)
        for i in range(total_days.days + 1):
            day = first_day + timedelta(days=i)
            if day == check_date:
                return True
        return False

    # Returns object date
    def get_object_date(self, model_object, **kw):
        if model_object.__class__.__name__ == 'account.invoice':
            if 'date_type' not in kw.keys():
                invoice_date = model_object.date_invoice
            else:
                if kw.get('date_type') != 'Date invoice':
                    invoice_date = model_object.date_invoice
                else:
                    invoice_date = model_object.date_due
            return invoice_date
        elif model_object.__class__.__name__ == 'sale.order':
            if model_object.date_order:
                return date(model_object.date_order.year,
                            model_object.date_order.month,
                            model_object.date_order.day)
            else:
                return False
        elif model_object.__class__.__name__ == 'stock.picking':
            if 'date_type' not in kw.keys():
                stock_date = model_object.scheduled_date
            else:
                if kw.get('date_type') != 'Scheduled date':
                    stock_date = model_object.date_done
                else:
                    stock_date = model_object.scheduled_date
            if stock_date:
                return date(stock_date.year,
                            stock_date.month,
                            stock_date.day)
            else:
                return False
        elif model_object.__class__.__name__ == 'crm.claim':
            if 'date_type' not in kw.keys():
                claim_date = model_object.date
            else:
                if kw.get('date_type') != 'Claim date':
                    claim_date = model_object.date_deadline
                else:
                    claim_date = model_object.date
            if claim_date:
                return date(claim_date.year,
                            claim_date.month,
                            claim_date.day)
            else:
                return False
        elif model_object.__class__.__name__ == 'crm.lead':
            if 'date_type' not in kw.keys():
                lead_date = model_object.date
            else:
                if kw.get('date_type') != 'Create date':
                    lead_date = model_object.date_deadline
                else:
                    lead_date = model_object.create_date
            if lead_date:
                return date(lead_date.year,
                            lead_date.month,
                            lead_date.day)
            else:
                return False
        else:
            return False

    # Returns object state
    def get_object_state(self, model_object):
        if model_object.__class__.__name__ == 'account.invoice':
            return model_object.state
        elif model_object.__class__.__name__ == 'stock.picking':
            return model_object.state
        elif model_object.__class__.__name__ == 'crm.claim':
            if model_object.stage_id.id == 1:
                return 'new'
            elif model_object.stage_id.id == 2:
                return 'in_progress'
            elif model_object.stage_id.id == 3:
                return 'settled'
            elif model_object.stage_id.id == 4:
                return 'rejected'
        elif model_object.__class__.__name__ == 'crm.lead':
            if model_object.stage_id.id == 1:
                return 'new'
            elif model_object.stage_id.id == 2:
                return 'qualified'
            elif model_object.stage_id.id == 3:
                return 'proposition'
            elif model_object.stage_id.id == 4:
                return 'won'

    # Get partners data for partner filter
    def get_partners_by_connected_user(self, model_element):
        # partner = request.env.user.partner_id
        partner_customers = []
        partner = request.env.user.partner_id
        model_object_ids = []
        if request.env.user._is_superuser() or request.env.user._is_admin():
            # admin
            model_object_ids = request.env[model_element].sudo().search([])
        else:
            # if request.env.user.has_group('base.group_user'):
            if request.env.user.is_commercial != 'no':
                # commercial
                partner_ids = request.env['res.partner'].sudo().search(
                    [('user_id.partner_id', '=', partner.id)])
                partner_list_ids = []
                for p in partner_ids:
                    partner_list_ids.append(p.id)
                partner_list_ids.append(partner.id)
                set(partner_list_ids)
                if not model_element == 'stock.picking':
                    model_object_ids = request.env[
                        model_element].sudo().search(
                            ['|', ('partner_id', 'in', partner_list_ids),
                             ('user_id', '=', request.env.user.id)])
                else:
                    model_object_ids = request.env[
                        model_element].sudo().search(
                            [('partner_id', 'in', partner_list_ids)])
            else:
                # user
                model_object_ids = request.env[model_element].sudo().search(
                    [('partner_id', '=', partner.id)])
        for model_obj in model_object_ids:
            partner_customers.append(model_obj.partner_id)
        values = {'partners': partner_customers,
                  'model_objs': model_object_ids}
        return values

    # Get domain str for object query
    def get_domain_by_connected_user(self, date_begin, date_end,
                                     model_element):
        partner = request.env.user.partner_id
        partner_user = request.env.user
        domain = []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]
        if not partner_user._is_superuser() and not partner_user._is_admin():
            # if request.env.user.has_group('base.group_user'):
            if request.env.user.is_commercial != 'no':
                # commercial
                partner_ids = request.env['res.partner'].sudo().search(
                    [('user_id.partner_id', '=', partner.id)])
                partner_list_ids = []
                for p in partner_ids:
                    partner_list_ids.append(p.id)
                partner_list_ids.append(partner.id)
                set(partner_list_ids)
                if not model_element == 'stock.picking':
                    domain += ['|', ('partner_id', 'in', partner_list_ids),
                               ('user_id', '=', request.env.user.id)]
                else:
                    domain += [('partner_id', 'in', partner_list_ids)]
            else:
                # user
                domain += [('partner_id', '=', partner.id)]
        return domain

    # Return filtered data
    def filter_data(self, domain, model_element, **kw):
        # Prepare params
        model_object_ids = list(
            request.env[model_element].sudo().search(domain))
        week_days = date.today() - (date.today() - timedelta(days=7))
        month_days = date.today() - date(int(datetime.now().year),
                                         int(datetime.now().month), 1)
        year_days = date.today() - date(int(datetime.now().year), 1, 1)
        # Filter data
        if 'customer' in kw.keys() and kw.get('customer') != 'All customers':
            for model_obj in model_object_ids.copy():
                if int(kw.get('customer')) != model_obj.partner_id.id:
                    model_object_ids.remove(model_obj)
        if 'customer_search' in kw.keys() and kw.get('customer_search') != '':
            for model_obj in model_object_ids.copy():
                customer_name = model_obj.partner_id.name
                if not customer_name:
                    customer_name = ''
                else:
                    customer_name = customer_name.lower()
                if kw.get('customer_search').lower() not in customer_name:
                    model_object_ids.remove(model_obj)
        if 'state' in kw.keys() and kw.get('state') != 'All states':
            for model_obj in model_object_ids.copy():
                obj_state = self.get_object_state(model_obj)
                if kw.get('state') != obj_state:
                    model_object_ids.remove(model_obj)
        if 'date' in kw.keys() and kw.get('date') != 'All dates':
            for model_obj in model_object_ids.copy():
                obj_date = self.get_object_date(model_obj, **kw)
                if not obj_date:
                    model_object_ids.remove(model_obj)
                    continue
                if kw.get('date') == 'Today':
                    if obj_date != date.today():
                        model_object_ids.remove(model_obj)
                elif kw.get('date') == 'Last week':
                    search = self.filter_by_days(week_days, obj_date)
                    if not search:
                        model_object_ids.remove(model_obj)
                elif kw.get('date') == 'This month':
                    search = self.filter_by_days(month_days, obj_date)
                    if not search:
                        model_object_ids.remove(model_obj)
                elif kw.get('date') == 'This year':
                    search = self.filter_by_days(year_days, obj_date)
                    if not search:
                        model_object_ids.remove(model_obj)
        if 'date_from' in kw.keys() and 'date_to' in kw.keys():
            date_from = kw.get('date_from').split('-')
            date_from = date(int(date_from[0]), int(date_from[1]),
                             int(date_from[2]))
            date_to = kw.get('date_to').split('-')
            date_to = date(int(date_to[0]), int(date_to[1]),
                           int(date_to[2]))
            for model_obj in model_object_ids.copy():
                obj_date = self.get_object_date(model_obj, **kw)
                if not obj_date:
                    model_object_ids.remove(model_obj)
                    continue
                if not date_from <= obj_date <= date_to:
                    model_object_ids.remove(model_obj)
        else:
            if 'date_from' in kw.keys():
                date_from = kw.get('date_from').split('-')
                date_from = date(int(date_from[0]), int(date_from[1]),
                                 int(date_from[2]))
                for model_obj in model_object_ids.copy():
                    obj_date = self.get_object_date(model_obj, **kw)
                    if not obj_date:
                        model_object_ids.remove(model_obj)
                        continue
                    if obj_date < date_from:
                        model_object_ids.remove(model_obj)
            if 'date_to' in kw.keys():
                date_to = kw.get('date_to').split('-')
                date_to = date(int(date_to[0]), int(date_to[1]),
                               int(date_to[2]))
                for model_obj in model_object_ids.copy():
                    obj_date = self.get_object_date(model_obj, **kw)
                    if not obj_date:
                        model_object_ids.remove(model_obj)
                        continue
                    if obj_date > date_to:
                        model_object_ids.remove(model_obj)
        return model_object_ids
