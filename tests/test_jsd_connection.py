from odoo.tests.common import TransactionCase

class TestJSDConnection(TransactionCase):
    def setUp(self):
        super(TestJSDConnection, self).setUp()
        self.connection = self.env["jsd.contacts.connection"].create(
            {"name": __file__, 'username': 'api', 'password': 'test123'}
        )

    def test_org_name_from_template(self):
        self.connection.organization_name_template = "$id: $name"
        name = self.connection._org_name_from_template({'id': 1, 'name': 'Company'})
        self.assertEqual(name, '1: Company')


# /entrypoint.sh -d odoo -u jsd_contacts --test-enable --log-level test --stop-after-init
