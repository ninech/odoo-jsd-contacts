from odoo import models, fields

class ResPartner(models.Model):
	_inherit = "res.partner"

	jira_organization_id = fields.Integer('Jira Organization ID', copy=False)
