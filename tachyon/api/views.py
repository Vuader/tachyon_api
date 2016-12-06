# Tachyon OSS Framework
#
# Copyright (c) 2016, see Authors.txt
# All rights reserved.
#
# LICENSE: (BSD3-Clause)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENTSHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import logging
import sys
import json

import nfw

log = logging.getLogger(__name__)

class Token(nfw.Middleware):
    def pre(self, req, resp):
        resp.headers['Content-Type'] = nfw.APPLICATION_JSON
        token = req.headers.get('X-Auth_Token')
        if token is not None:
            db = nfw.Mysql()
            sql = "SELECT * FROM token where token = %s AND token_expire > NOW()"
            result = db.execute(sql, (token,))
            if len(result) > 0:
                pass
            else:
                raise nfw.HTTPError(nfw.HTTP_404,'Authentication failed', 'Token not found or expired')

class Authenticate(nfw.Resource):
    def __init__(self, app):
        app.router.add(nfw.HTTP_POST, '/login', self.login, 'API:LOGIN')

    def _new_token(self, user_id, expire=1):
        db = nfw.Mysql()
        token_id = nfw.utils.random_id(64)

        db.execute("UPDATE user set last_login = now()" +
                   "  WHERE id = %s", (user_id,))

        db.execute("INSERT INTO token" +
                   " (id,user_id,token,token_expire)" +
                   " VALUES (uuid(),%s, %s, DATE_ADD(NOW()" +
                   ", INTERVAL %s HOUR))",
                   (user_id, token_id, expire))

        result = db.execute("SELECT token_expire" +
                            " FROM token WHERE token = %s",
                            (token_id,))

        session_expire = result[0]['token_expire']

        db.commit()

        return [ token_id, session_expire ]

    def login(self, req, resp):
        db = nfw.Mysql()
        creds = json.loads(req.read())
        usern = creds.get('username','')
        passw = creds.get('password','')
        domain = creds.get('domain','default')
        sql = "DELETE FROM token WHERE token_expire < NOW()"
        db.execute(sql)
        sql = "SELECT * FROM user"
        sql += " WHERE username = %s"
        result = db.execute(sql, (usern,))
        if len(result) == 1:
            if nfw.password.valid(passw, result[0]['password']):
                creds = {}
                creds['username'] = result[0]['username']
                creds['email'] = result[0]['email']
                token, expire = self._new_token(result[0]['id'])
                creds['token'] = token
                creds['expire'] = expire.strftime("%Y/%m/%d %H:%M:%S")
                return json.dumps(creds,indent=4)
            else:
                raise nfw.HTTPError(nfw.HTTP_404,'Authentication failed','Could not validate username and password credentials')
        else:
            raise nfw.HTTPError(nfw.HTTP_404,'Authentication failed','Could not validate username and password credentials')

