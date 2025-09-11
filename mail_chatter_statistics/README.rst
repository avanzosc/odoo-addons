.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=======================
Mail Chatter Statistics
=======================

Overview
========

The **Mail Chatter Statistics** module enhances Odoo's email tracking capabilities by providing features to monitor email opens and clicks. It allows users to track the engagement of their sent emails through unique tracking links embedded in the content.

Features
========

- **Open Tracking**: Records when a recipient opens an email by loading a tracking image.
  
- **Click Tracking**: Monitors when a recipient clicks on links within the email, updating the tracking information accordingly.

- **Integration with Odoo Chatter**: Displays mailing statistics directly within the Odoo message interface.

Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **Sending Emails**:

   - When sending emails through the Odoo mail interface, the tracking functionality is automatically applied.

3. **Viewing Statistics**:

   - Open any message in the Odoo chatter to see the tracking statistics, including open and click rates.

Configuration
=============

No additional configuration is required. The module is ready to use once installed.

Testing
=======

Test the following scenarios:

- **Email Open Tracking**:

  - Send an email and open it to verify that the open is logged correctly.

- **Email Click Tracking**:

  - Click on a link within the email and ensure the click is registered in the tracking information.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/yourusername/yourrepository/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
