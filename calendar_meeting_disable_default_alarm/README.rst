.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

======================================
Calendar Meeting Disable Default Alarm
======================================

Overview
========

The **Calendar Meeting Disable Default Alarm** module extends the default functionality of calendar events in Odoo. This customization allows for more flexible handling of calendar alarms and prevents sending emails to newly added attendees when modifying event details.

The main feature of this module is the disabling of alarm notifications for certain scenarios and modification of attendee notification behavior.

Features
========

- Prevents sending invitation emails to newly added attendees when modifying an event.
- Allows event updates to be handled with specific conditions based on recurrence, time changes, and alarms.
- Customizes how event updates are applied, including the breaking of recurrence and handling of alarms.

Usage
=====

1. **Install the Module**:
   
   - Install the **Calendar Meeting Disable Default Alarm** module from the Apps menu.

2. **Handling Attendee Emails**:
   
   - The module prevents the system from automatically sending invitation emails to newly added attendees when modifying an event. This is achieved by commenting out the part of the code responsible for sending those emails:

     ```python
     # if 'partner_ids' in values:
     #     (current_attendees - previous_attendees)._send_mail_to_attendees('calendar.calendar_template_meeting_invitation')
     ```

3. **Modifying Event Details**:
   
   - When modifying event details (such as start time, partners, or alarms), the system will behave according to specific rules for recurrence and alarm management:
   
     - If updating recurrence settings, certain validations are applied to ensure changes are valid.
   
     - Alarms are handled separately and notifications are sent when appropriate.
   
4. **No Email Notification for Newly Added Attendees**:
   
   - The module ensures that no email notifications are sent to new attendees when an event is modified. Only existing attendees will be notified when their attendance status or event time changes.

5. **Sync Activities and Notify Attendees**:
   
   - Updates to the event time or alarms will trigger notifications if necessary. The system ensures that attendees are notified only if the changes affect them.

Configuration
=============

No additional configuration is required. The module will automatically apply the behavior after installation.

Testing
=======

1. Go to *Calendar* → *Events*.
2. Edit an existing event and add new attendees.
3. Verify that no invitation emails are sent to the newly added attendees.
4. Modify other event details (such as time or alarms) and verify that existing attendees receive appropriate notifications.

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
