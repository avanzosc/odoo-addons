# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import base64

from odoo import tools
from odoo.modules import get_module_resource
from odoo.tests import common


class TestWebsiteBlogCharacterization(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestWebsiteBlogCharacterization, cls).setUpClass()
        cls.tag_model = cls.env['blog.tag']
        img_path = get_module_resource(
            'base', 'static/src/img', 'company_image.png')
        with open(img_path, 'rb') as f:
            image = f.read()
        cls.image1 = tools.image_resize_image_big(base64.b64encode(image))
        img_path = get_module_resource('base', 'static/src/img', 'avatar.png')
        with open(img_path, 'rb') as f:
            image = f.read()
        cls.image2 = tools.image_resize_image_big(base64.b64encode(image))

    def test_blog_tag_images(self):
        tag = self.tag_model.create({
            'name': 'Test Tag',
            'image': self.image1,
        })
        self.assertTrue(tag.image_small)
        image1_small = tag.image_small
        tag.write({
            'image': self.image2,
        })
        self.assertTrue(tag.image_medium)
        self.assertNotEquals(tag.image_small, image1_small)
