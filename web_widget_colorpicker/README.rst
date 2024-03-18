Color Picker widget for Odoo web client
================================


Features
========

Now only in RGBA code.


* Display the color on form view when you are not editing it

  |form_view_no_edit|

* Display the color on form view when you editing it

  |form_view_edit|

Usage
=====

You need to declare a char.

    colorpicker = fields.Char(
        string="Color Picker",
    )


In the view declaration,

    ...
    <field name="arch" type="xml">
        <form string="View name">
            ...
            <field name="colorpicker" widget="colorpicker"/>
            ...
        </form>
    </field>
    ...


