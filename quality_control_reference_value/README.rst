.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===============================
Quality Control Reference Value
===============================

- Adds `reference` field to `qc.test.question`, `qc.inspection.line` and `qc.inspection`.
- Automatically populates the `reference` field in inspection lines when creating an inspection from a test.
- Updates tree and form views to display the `reference` field.

Configuration
=============

In **Settings > Quality Control** the following parameters can be configured:

- **Default Unit**: unit of measure applied by default to new quantitative test questions.
- **Base Tolerance**: value used to compute the min/max range from a reference value (default: 0.2).
- **Default Type**: default question type when creating a new test question (default: Quantitative).

Usage
=====

When adding a question (`qc.test.question`) to a test:

- New questions default to type **Quantitative**.
- Changing the type to *Quantitative* automatically copies the default unit of measure from settings.
- Setting the **Reference** field automatically computes:

  - **Min** = Reference − Base Tolerance
  - **Max** = Reference + Base Tolerance

- The question list (`test_lines`) is editable inline directly from the test form.
- Each row has a button to open the full question form in a popup.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



