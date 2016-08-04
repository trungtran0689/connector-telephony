# -*- coding: utf-8 -*-
##############################################################################
#
#    Phone Log-call module for Odoo/OpenERP
#    Copyright (C) 2016 credativ Ltd (<http://credativ.co.uk>).
#    Copyright (C) 2016 Trever L. Adams
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import logging


logger = logging.getLogger(__name__)


class CrmPhonecall(models.Model):
    _inherit = "crm.phonecall"

    recording_id = fields.Many2one('ir.attachment', string='Call Recording', readonly=True)


class PhoneCommon(models.AbstractModel):
    _inherit = 'phone.common'

    @api.model
    def log_call_and_recording(self, odoo_type, odoo_src, odoo_dst, odoo_duration, odoo_start, odoo_filename, odoo_uniqueid, context=None):
        phonecall_obj = self.pool.get('crm.phonecall')
        attach_obj = self.pool.get('ir.attachment')

        caller_user, caller_external = odoo_type == 'incoming' and (odoo_dst, odoo_src) or (odoo_src, odoo_dst)

        call_name_prefix = odoo_type == 'incoming' and "Call from %s" or "Call to %s"

        phonecall_data = {
            'partner_phone': caller_external,
            'name': call_name_prefix % (caller_external,),
            'opportunity_id': False,
            'partner_id': False,
            'duration': int(odoo_duration) / 60.0,
            'state': 'done',
            'start_time': odoo_start,
        }

        r = self.get_record_from_phone_number(caller_external)
        if r[0] == 'res.partner':
            phonecall_data['partner_id'] = r[1]
            if r[2]:
                phonecall_data['name'] = call_name_prefix % (r[2],)
        elif r[0] == 'crm.lead':
            phonecall_data['opportunity_id'] = r[1]
            if r[2]:
                phonecall_data['name'] = call_name_prefix % (r[2],)

        users = self.env['res.users'].search(
            [('login', 'in', caller_user)])
        if not users:
            users = self.env['res.users'].search(
                [('internal_number', 'in', caller_user)])

        if users:
            phonecall_data['user_id'] = users[0]

        phonecall_id = phonecall_obj.create(phonecall_data, context=context)

        if odoo_filename:
            params = self.pool.get('ir.config_parameter')
# FIXME: Need to add an option to FreeSWITCH and Asterisk Click2Dial to have this option and use that.
#            base_url = params.get_param('crm.voip.ucp_url', default='http://localhost/ucp?quietmode=1&module=cdr&command=download&msgid={odoo_uniqueid}&type=download&format=wav&ext={caller_user}')
            base_url = "http://localhost/getsomefile"
            ir_attachment_data = {
                    'res_model': 'crm.phonecall',
                    'res_id': phonecall_id,
                    'name': phonecall_data['name'],
                    'type': 'url',
                    'url': base_url.format(caller_user=caller_user, odoo_uniqueid=odoo_uniqueid.replace('.', '_'), odoo_filename=odoo_filename),
                    'datas_fname': odoo_filename,
            }
            attach_id = attach_obj.create(ir_attachment_data, context=context)
            phonecall_obj.write([phonecall_id], {'recording_id': attach_id}, context=context)

        return True
