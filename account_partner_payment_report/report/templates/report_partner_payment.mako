## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            .open_invoice_previous_line {
                font-style: italic;
            }

            .clearance_line {
                font-style: italic;
            }
            ${css}
        </style>
        <style type="text/css" media="screen,print">
            .break{
                display: block;
                clear: both;
                page-break-after: always;
            }
        </style>
    </head>
    <body>
    <% template1 = helper.get_mako_template('account_partner_payment_report','report', 'templates', 'partner_payment_inclusion.mako.html') %>
    <% context.lookup.put_template('partner_payment_inclusion.mako.html', template1) %>
        <%setLang(user.lang)%>

        <div class="act_as_table data_table">
            <div class="act_as_row labels">
                <div class="act_as_cell">${_('Chart of Account')}</div>
                <div class="act_as_cell">${_('Fiscal Year')}</div>
                <div class="act_as_cell">
                    %if filter_form(data) == 'filter_date':
                        ${_('Dates Filter')}
                    %else:
                        ${_('Periods Filter')}
                    %endif
                </div>
                <div class="act_as_cell">${_('Clearance Date')}</div>
                <div class="act_as_cell">${_('Accounts Filter')}</div>
                <div class="act_as_cell">${_('Target Moves')}</div>

            </div>
            <div class="act_as_row">
                <div class="act_as_cell">${ chart_account.name }</div>
                <div class="act_as_cell">${ fiscalyear.name if fiscalyear else '-' }</div>
                <div class="act_as_cell">
                    ${_('From:')}
                    %if filter_form(data) == 'filter_date':
                        ${formatLang(start_date, date=True) if start_date else u'' }
                    %else:
                        ${start_period.name if start_period else u''}
                    %endif
                    ${_('To:')}
                    %if filter_form(data) == 'filter_date':
                        ${ formatLang(stop_date, date=True) if stop_date else u'' }
                    %else:
                        ${stop_period.name if stop_period else u'' }
                    %endif
                </div>
                <div class="act_as_cell">${ formatLang(date_until, date=True) }</div>
                <div class="act_as_cell">
                    %if partner_ids:
                        ${_('Custom Filter')}
                    %else:
                        ${ display_partner_account(data) }
                    %endif
                </div>
                <div class="act_as_cell">${ display_target_move(data) }</div>
            </div>
        </div>
        %if objects.filtered(lambda x: ledger_lines[x.id]):
            %for commercial in objects.filtered(lambda x: ledger_lines[x.id]).mapped('user_id'):
                <br/>
                <div class="account_title bg" style="font-size:16px"> ${_('Commercial: ')}${commercial.name}</div>
                %for part in objects.filtered(lambda x: x.user_id.id==commercial.id):
                    <% fl = formatLang %>
                    <%include file="partner_payment_inclusion.mako.html" args="partner=part,formatLang=fl"/>
                %endfor
                %if commercial.id != objects.filtered(lambda x: ledger_lines[x.id]).mapped('user_id')[-1].id:
                    <div class="break"> </div>
                %endif
            %endfor
            %if objects.filtered(lambda x: not x.user_id and ledger_lines[x.id]):
                 %if objects.filtered(lambda x: x.user_id and ledger_lines[x.id]):
                     <div class="break"> </div>
                 %endif
                 </br>
                 <div class="account_title bg" style="font-size:16px"> ${_('No Commercial')}</div>
                 %for part in objects.filtered(lambda x: not x.user_id and ledger_lines[x.id]):
                        <% fl = formatLang %>
                        <%include file="partner_payment_inclusion.mako.html" args="partner=part,formatLang=fl"/>
                 %endfor
             %endif
        %endif
    </body>
</html>
