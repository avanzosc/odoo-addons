.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

================================
Mail Mail Correct Mail Server ID
================================

Overview
========

The **Mail Mail Correct Mail Server ID** module ensures that outgoing emails use the correct mail server based on the company. This is particularly useful in multi-company environments where each company has its own SMTP configuration.

Features
========

- **Automatic Mail Server Selection**:

  - When an email (`mail.mail`) is created, the module assigns the correct mail server (`ir.mail_server`) based on the company.

- **Improved Multi-Company Support**:

  - Ensures that each company's emails are sent using the appropriate mail server.

Usage
=====

1. **Install the Module**:

   - Install the **Mail Mail Correct Mail Server ID** module from the Apps menu.

2. **Configure Mail Servers**:

   - Go to *Settings* → *Technical* → *Email* → *Outgoing Mail Servers*.

   - Assign a mail server to each company.

3. **Send Emails**:

   - When an email is created, the system will automatically select the mail server linked to the email’s company.


Testing
=======

1. Ensure that each company has at least one outgoing mail server configured.
2. Create an email (`mail.mail`) under different companies.
3. Verify that the correct mail server is assigned to each email.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions or support, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
