from odoo import fields, models, _
from odoo.exceptions import UserError
from atlassian import ServiceDesk
from requests.exceptions import HTTPError
from ast import literal_eval
from string import Template

import logging

_logger = logging.getLogger(__name__)

class JSDConnection(models.Model):
    _name = "jsd.contacts.connection"
    _description = "Holds Jira Service Desk Instance Configuration."

    active = fields.Boolean('Active', default=False)
    name = fields.Char('Instance Name', required=True)
    url = fields.Char('API URL', required=True,
                      default='https://<hostname>', help="The API URL")
    username = fields.Char('Username', required=True, copy=False)
    password = fields.Char('Password', required=True, copy=False)
    service_desk_id = fields.Integer('Service Desk ID', required=True)

    organizations_domain = fields.Char('Organization Domain', default='[]', required=True)
    organization_name_template = fields.Char('Organization Name Template', default='$name',
        help='A Python string template with attributes of the partner object.', required=True)

    def action_check_connection(self):
        """ Calls the Jira API and checks for the validity of the given params.
        """
        self.ensure_one()

        _logger.debug("Calling URL {0}".format(self.url))
        sd = self._get_jira_service_desk_connection()
        try:
            sd_info = sd.get_info()
        except HTTPError as err:
            _logger.debug("Connection error {0}".format(err))
            raise UserError(err) # TODO: just show message, not user error

        message = "The connection was successful! Service Desk version {0}".format(sd_info['version'])
        # TODO: Replace with a proper dialog
        raise UserError(message)

    def action_sync_organizations(self):
        jsd = self._get_jira_service_desk_connection()

        for connection in self:
            _logger.debug('Starting Jira contact sync for connection %s.', connection.name)
            domain = connection._parse_organizations_domain()
            for contact in self.env['res.partner'].search(domain):
                if contact.jira_organization_id:
                    continue
                organization = jsd.create_organization(connection._org_name_from_template(contact))
                jsd.add_organization(connection.service_desk_id, organization['id'])
                contact.write({'jira_organization_id': organization['id']})

    def _get_jira_service_desk_connection(self):
        return ServiceDesk(url=self.url, username=self.username, password=self.password)

    def _parse_organizations_domain(self):
        self.ensure_one()
        try:
            organizations_domain = literal_eval(self.organizations_domain)
        except Exception:
            organizations_domain = [('id', 'in', [])]
        return organizations_domain

    def _org_name_from_template(self, contact):
        return Template(self.organization_name_template).substitute(contact)
