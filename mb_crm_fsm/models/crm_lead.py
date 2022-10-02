from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CRMLead(models.Model):
    _inherit = "crm.lead"

    project_ids = fields.One2many('project.project', 'lead_id')
    project_count = fields.Integer(string="Project Count", compute='_compute_project_count')

    def _compute_project_count(self):
        for rec in self:
            rec.project_count = len(self.project_ids)

    def action_view_sale_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.mapped('order_ids').filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    def action_view_fsm(self):
        self.ensure_one()
        view_form_id = self.env.ref('project.edit_project').id
        view_kanban_id = self.env.ref('project.view_project_kanban').id
        action = {
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.project_ids.ids)],
            'view_mode': 'kanban,form',
            'name': _('Projects'),
            'res_model': 'project.project',
        }
        if len(self.project_ids) == 1:
            action.update({'views': [(view_form_id, 'form')], 'res_id': self.project_ids.id})
        else:
            action['views'] = [(view_kanban_id, 'kanban'), (view_form_id, 'form')]
        return action
    
    
    # def action_new_fsm(self):
    #         if not self.lead_id.partner_id:
    #             raise ValidationError(_('Customer is missing on Lead.'))
        # return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")

    #     if not self.partner_id:
    #     else:
    #         return self.action_new_quotation()

    # def action_create_fsm(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
    #     action['context'] = {
    #         'search_default_opportunity_id': self.id,
    #         'default_opportunity_id': self.id,
    #         'search_default_partner_id': self.partner_id.id,
    #         'default_partner_id': self.partner_id.id,
    #         'default_campaign_id': self.campaign_id.id,
    #         'default_medium_id': self.medium_id.id,
    #         'default_origin': self.name,
    #         'default_source_id': self.source_id.id,
    #         'default_company_id': self.company_id.id or self.env.company.id,
    #         'default_tag_ids': [(6, 0, self.tag_ids.ids)]
    #     }
    #     if self.team_id:
    #         action['context']['default_team_id'] = self.team_id.id,
    #     if self.user_id:
    #         action['context']['default_user_id'] = self.user_id.id
    #     return action

class Project(models.Model):
    _inherit = 'project.project'

    lead_id = fields.Many2one('crm.lead')

class ProjectTask(models.Model):
    _inherit = 'project.task'

    lead_id = fields.Many2one('crm.lead')


    def _fsm_create_sale_order(self):
        """ Create the SO from the task, with the 'service product' sales line and link all timesheet to that line it """
        res = super(ProjectTask, self)._fsm_create_sale_order()
        if self.lead_id:
            self.sale_order_id.opportunity_id = self.lead_id.id
        
        return res