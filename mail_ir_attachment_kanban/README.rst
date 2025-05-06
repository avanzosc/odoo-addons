.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=========================
Mail IR Attachment Kanban
=========================

Overview
========

The **Mail IR Attachment Kanban** module enhances the attachment handling in Odoo's Kanban view by displaying additional information in a tooltip when hovering over an attachment card. This information includes the creation date, the user who created it, the last modification date, and the user who last modified the attachment.

Features
========

- Displays a tooltip with the following details when hovering over an attachment card in Kanban view:
  
  - Creation date (`create_date`).
  
  - Creator user (`create_uid`).
  
  - Last modification date (`write_date`).
  
  - Last modifier user (`write_uid`).

- The tooltip is shown below the attachment card for better visibility and user experience.

- Information is dynamically fetched from the `ir.attachment` model via RPC calls when the attachment card is hovered.

Usage
=====

1. **Install the Module**:

   - Install the **Mail IR Attachment Kanban** module from the Apps menu.

2. **Hover Over Attachment Cards**:

   - Navigate to any Kanban view that displays attachments (for example, the *Documents* or *Emails* apps).

   - Hover your mouse over any attachment card to see a tooltip displaying the following information:

     - **Created on**: The date when the attachment was created.

     - **Created by**: The user who created the attachment.

     - **Last modified on**: The date when the attachment was last modified.

     - **Last modified by**: The user who last modified the attachment.

3. **Tooltip Appearance**:

   - The tooltip appears just below the attachment card, and it is styled with a light background, border, and shadow for better readability.

   - The tooltip dynamically adjusts its position to always appear below the attachment card based on the card's position on the screen.

4. **No Manual Configuration**:

   - No additional configuration is required. The module works automatically after installation, enhancing the user experience with attachment details.

Configuration
=============

No additional configuration is required to use this module.

Testing
=======

1. Go to a Kanban view displaying attachments, such as the *Documents* or *Emails* app.

2. Hover over an attachment card.

3. Verify that a tooltip appears displaying the following information:

   - Created date and user.

   - Last modified date and user.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/sale-addons/issues>`_.

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
