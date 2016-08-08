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


class FreeSWITCHServer(models.Model):
    _inherit = "freeswitch.server"

    ucp_url = fields.Char(
        string='Script to download FreeSWITCH recordings', required=False,
        default="https://localhost/get_file?filename={odoo_filename}",
        help="Macros allowed: {odoo_type} (inbound, outbound), {odoo_src}"
        "(source phon number}, {odoo_dst} (destination number), "
        "{odoo_duration} (length of call), {odoo_start} (start time of call "
        "in seconds since epoch), {odoo_filename} (file name on server), "
        "{odoo_uniqueid} (FreeSWITCH UUID of call).")


class PhoneCommon(models.AbstractModel):
    _inherit = 'phone.common'

    @api.model
    def _get_ucp_url(self, users):
        fs_server = users[0].freeswitch_server_id
        return fs_server.ucp_url
