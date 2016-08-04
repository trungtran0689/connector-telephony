-- Copyright (C) 2016 Trever L. Adams
-- based on code and ideas by Craig Gowing <craig.gowing@credativ.co.uk>
-- & Alexis de Lattre <alexis.delattre@akretion.com>

-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as
-- published by the Free Software Foundation, either version 3 of the
-- License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

require("xmlrpc.http")

local port=8069;
local server="localhost";
local protocol="https"
local server_string = protocol .. "://" .. server .. ":" .. port

    odoo_type = session:getVariable("direction")
    odoo_src = session:getVariable("caller_id_number")
    odoo_dst = session:getVariable("destination_number")
    odoo_duration = session:getVariable("hangup_time") - session:getVariable("answer_time")
    odoo_duration = session:getVariable("transfer_time") - session:getVariable("answer_time")
    odoo_start = session:getVariable("answered_time")
    odoo_filename = session:getVariable("rec_file")
    odoo_uniqueid = session:getVariable("uuid")
    odoo_arguments = 


local ok, res = xmlrpc.http.call(server_string, options.database, options.userid, options.password,
                'phone.common', 'log_call_and_recording', odoo_type, odoo_src, odoo_dst, odoo_duration, odoo_start, odoo_filename, odoo_uniqueid, arguments)
assert(ok, string.format("XML-RPC call failed on client: %s", tostring(res)))

print("Result: " .. tostring(res))

"""
 Log a call and recording within FreeSWITCH

 This is intended to be called by a hangup handler:

<action application="set" data="session_in_hangup_hook=true"/>
<action application="set" data="api_hangup_hook=luarun freeswitch_logcall.lua ${uuid}"/> 


"""


def main(options, arguments):

    # AGI passes parameters to the script on standard input
    stdinput = {}
    while 1:
        input_line = sys.stdin.readline()
        if not input_line:
            break
        line = input_line.strip()
        try:
            variable, value = line.split(':')
        except:
            break
        if variable[:4] != 'agi_':  # All AGI parameters start with 'agi_'
            stderr_write("bad stdin variable : %s\n" % variable)
            continue
        variable = variable.strip()
        value = value.strip()
        if variable and value:
            stdinput[variable] = value
    stderr_write("full AGI environnement :\n")

    for variable in stdinput.keys():
        stderr_write("%s = %s\n" % (variable, stdinput.get(variable)))

    odoo_type = stdinput['agi_arg_1']
    odoo_src = stdinput['agi_arg_2']
    odoo_dst = stdinput['agi_arg_3']
    odoo_duration = stdinput['agi_arg_4']
    odoo_start = stdinput['agi_arg_5']
    odoo_filename = stdinput['agi_arg_6']
    odoo_uniqueid = stdinput['agi_arg_7']
local start_epoch = tonumber(event:getHeader("variable_start_epoch"))
local answer_epoch = tonumber(event:getHeader("variable_answer_epoch"))
local end_epoch = tonumber(event:getHeader("variable_end_epoch"))

    method = 'log_call_and_recording'

    res = False

    elif options.server:
        proto = options.ssl and 'https' or 'http'
        stdout_write(
            'VERBOSE "Starting %s XML-RPC request on OpenERP %s:%d '
            'database %s user ID %d"\n' % (
                proto, options.server, options.port, options.database,
                options.userid))
        sock = xmlrpclib.ServerProxy(
            '%s://%s:%d/xmlrpc/object'
            % (proto, options.server, options.port))
        try:
            res = sock.execute(
                options.database, options.userid, options.password,
                'phone.common', 'log_call_and_recording', odoo_type, odoo_src, odoo_dst, odoo_duration, odoo_start, odoo_filename, odoo_uniqueid, arguments)
            stdout_write('VERBOSE "Called method %s"\n' % method)
        except Exception, e:
            raise
            stdout_write('VERBOSE "Could not connect to OpenERP in XML-RPC"\n')
        # To simulate a long execution of the XML-RPC request
        # import time
        # time.sleep(5)

    return True

if __name__ == '__main__':
    usage = "Usage: freeswitch_logcall.py [options] login1 login2 login3 ..."
    epilog = "Script written by Craig Gowing based on work by Alexis de Lattre. "
    "Published under the GNU AGPL licence."
    description = "This is an AGI script that sends a query to Odoo. "
    parser = OptionParser(usage=usage, epilog=epilog, description=description)
    for option in options:
        param = option['names']
        del option['names']
        parser.add_option(*param, **option)
    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)
