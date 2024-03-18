import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    def test_open_url(self):
        # wait till page loaded
        code = """
            setTimeout(function () {
                console.log('ok');
            }, 3000);
        """
        link = "/web/login"
        self.phantom_js(link, code, "", login="admin")
