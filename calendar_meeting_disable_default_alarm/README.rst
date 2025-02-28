.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

======================================
Calendar Meeting Disable Default Alarm
======================================

Overview
========

The **Calendar Meeting Disable Default Alarm** module extends the default functionality of calendar events in Odoo. This customization provides more flexibility in handling calendar alarms and attendee notifications by using context flags to control behavior, specifically preventing the sending of emails to newly added attendees when modifying event details.

The main feature of this module is the dynamic management of alarm notifications and attendee email notifications through the use of context and the `super()` method.

Features
========

- Prevents sending invitation emails to newly added attendees when modifying an event by leveraging context flags.
- Allows for event updates to be applied under specific conditions based on recurrence, time changes, and alarm notifications.
- Customizes how event updates are processed, including controlling notifications based on context variables.

Usage
=====

1. **Install the Module**:
   
   - Install the **Calendar Meeting Disable Default Alarm** module from the Apps menu.

2. **Handling Attendee Emails**:
   
   - The module prevents the automatic sending of invitation emails to newly added attendees when an event is modified. This behavior is controlled by setting the context variable `no_mail_to_attendees`:

     ```python
     self = self.with_context(no_mail_to_attendees=True)
     ```

   - The context flag `no_mail_to_attendees` ensures that newly added attendees are not notified, while the existing ones will still receive the appropriate updates.

3. **Modifying Event Details**:
   
   - When event details (such as start time, attendees, or alarms) are modified, the system checks the context for any specific flags and adjusts behavior accordingly.
   
   - The recurrence and alarm settings are handled properly, with email notifications sent only when necessary.

4. **Context-Based Notification Control**:
   
   - By setting the context variable `no_mail_to_attendees`, the system ensures that no invitation emails are sent to new attendees when modifying an event. Only existing attendees are notified if the changes impact them.

5. **Sync Activities and Notify Attendees**:
   
   - Changes to event time or alarms will trigger notifications if needed. The system uses the context to control which attendees receive updates, ensuring minimal disruption.

Configuration
=============

No additional configuration is required. The module will automatically apply the modified behavior after installation.

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
