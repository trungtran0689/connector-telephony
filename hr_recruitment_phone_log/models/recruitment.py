# -*- coding: utf-8 -*-
# (c) 2016 credativ ltd. - Ondřej Kuzník
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    phonecall_ids = fields.One2many('crm.phonecall', 'partner_id')
    phonecall_count = fields.Integer(
        compute='_count_phonecalls', string='Number of Phonecalls',
        readonly=True)

    @api.multi
    @api.depends('phonecall_ids')
    def _count_phonecalls(self):
        cpo = self.env['crm.phonecall']
        for partner in self:
            try:
                partner.phonecall_count = cpo.search_count(
                    [('partner_id', 'child_of', partner.id)])
            except:
                partner.phonecall_count = 0
        
