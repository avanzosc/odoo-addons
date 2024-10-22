# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models, _
from odoo.tools import pycompat, OrderedSet
from odoo.exceptions import UserError
import re

regex_field_agg = re.compile(r'(\w+)(?::(\w+)(?:\((\w+)\))?)?')
# valid SQL aggregation functions
VALID_AGGREGATE_FUNCTIONS = {
    'array_agg', 'count', 'count_distinct',
    'bool_and', 'bool_or', 'max', 'min', 'avg', 'sum',
}


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_created_date = fields.Datetime(
        string="Product create date", related="product_id.create_date",
        store=True, copy=False)

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None,
                        orderby=False, lazy=True):
        found = False
        if "stock.quant" not in str(self):
            return super(StockQuant, self). _read_group_raw(
                domain, fields, groupby, offset=offset, limit=limit,
                orderby=orderby, lazy=lazy)
        if "stock.quant" in str(self):
            found = True
            if ("to_date" in self.env.context and
                    self.env.context.get("to_date", False)):
                my_domain = [
                    ("in_date", "<=", self.env.context.get("to_date"))]
                domain = my_domain + domain
            if ("from_date" in self.env.context and
                    self.env.context.get("from_date", False)):
                my_domain = [
                    ("in_date", ">=", self.env.context.get("from_date"))]
                domain = my_domain + domain
            if ("('location_id.usage', 'in', ['internal', 'transit'])" not in
                    str(domain)):
                return super(StockQuant, self). _read_group_raw(
                    domain, fields, groupby, offset=offset, limit=limit,
                    orderby=orderby, lazy=lazy)
        self.check_access_rights('read')
        query = self._where_calc(domain)
        fields = fields or [f.name for f in self._fields.values() if f.store]

        groupby = ([groupby] if isinstance(groupby, pycompat.string_types) else
                   list(OrderedSet(groupby)))
        groupby_list = groupby[:1] if lazy else groupby
        annotated_groupbys = [
            self._read_group_process_groupby(gb, query) for gb in groupby_list]
        groupby_fields = [g['field'] for g in annotated_groupbys]
        order = orderby or ','.join([g for g in groupby_list])
        groupby_dict = {gb['groupby']: gb for gb in annotated_groupbys}

        self._apply_ir_rules(query, 'read')
        for gb in groupby_fields:
            if gb not in self._fields:
                raise UserError(_("Unknown field %r in 'groupby'") % gb)
            gb_field = self._fields[gb].base_field
            if not (gb_field.store and gb_field.column_type):
                raise UserError(
                    _("Fields in 'groupby' must be database-persisted fields "
                      "(no computed fields)"))

        aggregated_fields = []
        select_terms = []

        for fspec in fields:
            if fspec == 'sequence':
                continue

            match = regex_field_agg.match(fspec)
            if not match:
                raise UserError(_("Invalid field specification %r.") % fspec)

            name, func, fname = match.groups()
            if func:
                # we have either 'name:func' or 'name:func(fname)'
                fname = fname or name
                field = self._fields[fname]
                if not (field.base_field.store and field.base_field.column_type):
                    raise UserError(_("Cannot aggregate field %r.") % fname)
                if func not in VALID_AGGREGATE_FUNCTIONS:
                    raise UserError(_("Invalid aggregation function %r.") % func)
            else:
                # we have 'name', retrieve the aggregator on the field
                field = self._fields.get(name)
                if not (field and field.base_field.store and
                        field.base_field.column_type and field.group_operator):
                    continue
                func, fname = field.group_operator, name

            if fname in groupby_fields:
                continue
            if name in aggregated_fields:
                raise UserError(_("Output name %r is used twice.") % name)
            aggregated_fields.append(name)

            expr = self._inherits_join_calc(self._table, fname, query)
            if func.lower() == 'count_distinct':
                term = 'COUNT(DISTINCT %s) AS "%s"' % (expr, name)
            else:
                term = '%s(%s) AS "%s"' % (func, expr, name)
            select_terms.append(term)

        for gb in annotated_groupbys:
            select_terms.append('%s as "%s" ' % (gb['qualified_field'], gb['groupby']))

        groupby_terms, orderby_terms = self._read_group_prepare(
            order, aggregated_fields, annotated_groupbys, query)
        from_clause, where_clause, where_clause_params = query.get_sql()
        if (lazy and (len(groupby_fields) >= 2 or not
                      self._context.get('group_by_no_leaf'))):
            count_field = groupby_fields[0] if len(groupby_fields) >= 1 else '_'
        else:
            count_field = '_'
        count_field += '_count'

        prefix_terms = lambda prefix, terms: (prefix + " " + ",".join(terms)) if terms else ''
        prefix_term = lambda prefix, term: ('%s %s' % (prefix, term)) if term else ''

        if found:
            where = prefix_term(
                'WHERE ("stock_quant"."create_date">="stock_quant".'
                '"product_created_date") AND ', where_clause)
        else:
            where = prefix_term('WHERE ', where_clause)

        query = """
            SELECT min("%(table)s".id) AS id,
            count("%(table)s".id) AS "%(count_field)s" %(extra_fields)s
            FROM %(from)s
            %(where)s
            %(groupby)s
            %(orderby)s
            %(limit)s
            %(offset)s
        """ % {
            'table': self._table,
            'count_field': count_field,
            'extra_fields': prefix_terms(',', select_terms),
            'from': from_clause,
            'where': where,
            'groupby': prefix_terms('GROUP BY', groupby_terms),
            'orderby': prefix_terms('ORDER BY', orderby_terms),
            'limit': prefix_term('LIMIT', int(limit) if limit else None),
            'offset': prefix_term('OFFSET', int(offset) if limit else None),
        }

        self._cr.execute(query, where_clause_params)

        fetched_data = self._cr.dictfetchall()

        if not groupby_fields:
            return fetched_data

        self._read_group_resolve_many2one_fields(fetched_data, annotated_groupbys)

        data = [{k: self._read_group_prepare_data(k, v, groupby_dict) for k, v in r.items()} for r in fetched_data]

        if self.env.context.get('fill_temporal') and data:
            data = self._read_group_fill_temporal(data, groupby, aggregated_fields,
                                                  annotated_groupbys)

        result = [self._read_group_format_result(d, annotated_groupbys, groupby, domain) for d in data]

        if lazy:
            # Right now, read_group only fill results in lazy mode (by default).
            # If you need to have the empty groups in 'eager' mode, then the
            # method _read_group_fill_results need to be completely reimplemented
            # in a sane way 
            result = self._read_group_fill_results(
                domain, groupby_fields[0], groupby[len(annotated_groupbys):],
                aggregated_fields, count_field, result, read_group_order=order,
            )
        return result
