# -*- coding: utf-8 -*-
{
  'name': 'Jira Service Desk Contacts',
  'depends': [
    'base',
    'contacts',
  ],
  'data': [
    'security/ir.model.access.csv',

    'data/jsd_contacts_view.xml',
    'data/jsd_contacts_menus.xml',
  ],
  'external_dependencies': {
   'python': ['atlassian-python-api'],
  },
  'application': True,
}
