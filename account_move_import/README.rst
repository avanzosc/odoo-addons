Account Move Import from CSV file
====================================

Wizard to import account move lines from a CSV file.
The file must have at least 2 columns with "account" and "name" Head Keys.
There are two more columns with 'debit' and 'credit' head keys to add amount.
You can also add a column with key "partner_id" or "partner_ref" or
"partner_name" to add a partner link if you add it you need to add a column
with key "partner_type" defining if it is "customer" or "supplier".
- If the date column is added date_maturity is update in lines.

Credits
=======

Contributors
------------
* Daniel Campos <danielcampos@avanzosc.es>
* Ana Juaristi <ajuaristio@gmail.com>
