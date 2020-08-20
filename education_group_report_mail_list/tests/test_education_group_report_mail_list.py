# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestEducationGroupReportMailListCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestEducationGroupReportMailList(TestEducationGroupReportMailListCommon):

    def test_education_group_report_mail_list(self):
        # test addProgenitorsToList()
        self.assertEquals(len(
            self.mailing_list_student.subscription_contact_ids), 1)
        self.mail_list_wizard_students.addStudentToList(
            self.student_2, self.mailing_list_student)
        self.assertEquals(len(
            self.mailing_list_student.subscription_contact_ids), 2)
        # test addProgenitorsToList()
        self.assertEquals(len(
            self.mailing_list_progenitor.subscription_contact_ids), 1)
        self.mail_list_wizard_students.addStudentToList(
            self.progenitor_2, self.mailing_list_progenitor)
        self.assertEquals(len(
            self.mailing_list_progenitor.subscription_contact_ids), 2)
        # test partnerExistInList()
        self.assertTrue(self.mail_list_wizard_students.partnerExistInList(
            self.student, self.mailing_list_student))
        # test parterExist()
        self.assertTrue(self.mail_list_wizard_students.partnerExist(
            self.student))
        # test button_update_list()
        self.mail_list_wizard_students.button_update_list()
