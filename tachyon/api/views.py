# Tachyon OSS Framework
#
# Copyright (c) 2016-2017, see Authors.txt
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
from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json
from collections import OrderedDict

import nfw

from tachyon.api import model
from tachyon.api import api

log = logging.getLogger(__name__)


def get_user_roles(user_id):
    db = nfw.Mysql()
    result = db.execute("SELECT role_id,domain_id" +
                        ",tenant_id FROM user_role" +
                        " WHERE user_id = %s", (user_id,))
    db.commit()
    roles = []
    for r in result:
        role = OrderedDict()
        role['tenant_id'] = r['tenant_id']
        role['tenant_name'] = get_tenant_name(r['tenant_id'])
        role['domain_id'] = r['domain_id']
        role['domain_name'] = get_domain_name(r['domain_id'])
        role['role_id'] = r['role_id']
        role['role_name'] = get_role_name(r['role_id'])
        roles.append(role)
    return roles


def get_domain_id(domain):
    db = nfw.Mysql()
    result = db.execute("SELECT id FROM domain" +
                        " WHERE id = %s OR name = %s",
                        (domain, domain))
    db.commit()
    if len(result) > 0:
        return result[0]['id']
    else:
        return None


def get_domain_name(domain):
    db = nfw.Mysql()
    result = db.execute("SELECT name FROM domain" +
                        " WHERE id = %s OR name = %s",
                        (domain, domain))
    if len(result) > 0:
        return result[0]['name']
    else:
        return None


def get_tenant_id(tenant):
    db = nfw.Mysql()
    result = db.execute("SELECT id FROM tenant" +
                        " WHERE id = %s OR name = %s",
                        (tenant, tenant))
    db.commit()
    if len(result) > 0:
        return result[0]['id']
    else:
        return None


def get_tenant_name(tenant):
    db = nfw.Mysql()
    result = db.execute("SELECT name FROM tenant" +
                        " WHERE id = %s OR name = %s",
                        (tenant, tenant))
    db.commit()
    if len(result) > 0:
        return result[0]['name']
    else:
        return None


def get_role_name(role):
    db = nfw.Mysql()
    result = db.execute("SELECT name FROM role" +
                        " WHERE id = %s OR name = %s",
                        (role, role))
    db.commit()
    if len(result) > 0:
        return result[0]['name']
    else:
        return None


def get_user_domain_admin(user_id, domain_id):
    db = nfw.Mysql()
    result = db.execute("SELECT domain_id,tenant_id" +
                        " FROM user_role WHERE user_id = %s" +
                        " AND domain_id = %s" +
                        " AND tenant_id is NULL",
                        (user_id, domain_id))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return False


def get_user_domains(user_id):
    db = nfw.Mysql()
    sql_domains_result = db.execute("SELECT domain_id,tenant_id" +
                                    " FROM user_role WHERE user_id = %s" +
                                    " GROUP BY domain_id", (user_id,))
    result = []
    for sql_domain in sql_domains_result:
        domain = {}
        domain_id = sql_domain['domain_id']
        sql_domain_name_result = db.execute("SELECT name FROM domain" +
                                            " WHERE id = %s", (domain_id,))
        name = sql_domain_name_result[0]['name']
        domain['domain_id'] = domain_id
        domain['domain_name'] = name
        domain['domain_admin'] = get_user_domain_admin(user_id, domain_id)

        result.append(domain)
    return result


def authenticate_user_domain(user_id, domain_id):
    if domain_id is None:
        return False

    user_domains = get_user_domains(user_id)
    for user_domain in user_domains:
        if user_domain['domain_id'] == domain_id:
            return True
    return False


def authenticate_user_tenant(user_id, domain_id, tenant_id):
    if tenant_id is None:
        return False

    db = nfw.Mysql()
    result = db.execute("SELECT * FROM user_role" +
                        " WHERE user_id = %s AND domain_id = %s" +
                        " AND tenant_id = %s",
                        (user_id, domain_id, tenant_id))
    if len(result) > 0:
        return True

    return False


def get_username(username):
    db = nfw.Mysql()
    result = db.execute("SELECT username FROM user" +
                        " WHERE id = %s OR username = %s",
                        (username, username))
    db.commit()
    if len(result) > 0:
        return result[0]['username']
    else:
        return None


def get_lastlogin(username):
    db = nfw.Mysql()
    result = db.execute("SELECT last_login FROM user" +
                        " WHERE id = %s OR username = %s",
                        (username, username))
    db.commit()
    if len(result) > 0:
        return result[0]['last_login']
    else:
        return None


class Token(nfw.Middleware):
    def pre(self, req, resp):
        tenant = req.headers.get('X-Tenant')
        domain = req.headers.get('X-Domain', 'default')
        domain_id = get_domain_id(domain)
        if tenant is not None:
            tenant_id = get_tenant_id(tenant)
        else:
            tenant_id = None

        req.context['tenant_id'] = None
        req.context['domain_admin'] = False
        req.context['domain_id'] = None
        req.context['login'] = False
        req.context['token'] = None
        req.context['expire'] = None
        req.context['roles'] = []

        resp.headers['Content-Type'] = nfw.APPLICATION_JSON
        token = req.headers.get('X-Auth_Token')
        if token is not None:
            db = nfw.Mysql()
            sql = "SELECT * FROM token where token = %s"
            sql += " AND token_expire > NOW()"
            result = db.execute(sql, (token,))
            db.commit()
            if len(result) > 0:
                user_id = result[0]['user_id']
                req.context['user_id'] = user_id
                req.context['token'] = token

                roles = get_user_roles(user_id)
                req.context['login'] = True
                db.execute("UPDATE token" +
                           " set token_expire =" +
                           " (DATE_ADD(NOW()" +
                           ", INTERVAL 1 HOUR))" +
                           " WHERE token = %s", (token,))
                db.commit()
            else:
                raise nfw.HTTPError(nfw.HTTP_404, 'Authentication failed',
                                    'Token not found or expired')

            if authenticate_user_domain(user_id, domain_id):
                req.context['domain_id'] = domain_id
                req.context['domain_admin'] = get_user_domain_admin(user_id,
                                                                    domain_id)
                if req.context['domain_admin'] is True:
                    req.context['tenant_id'] = tenant_id
                else:
                    if tenant_id is not None:
                        if authenticate_user_tenant(user_id, domain_id,
                                                    tenant_id):
                            req.context['tenant_id'] = tenant_id
                        else:
                            raise nfw.HTTPForbidden("Access Denied", "Invalid"
                                                    + " Tenant")
            else:
                raise nfw.HTTPForbidden("Access Denied", "Invalid Domain")

            for role in roles:
                if (role['domain_id'] == domain_id):
                    if (role['tenant_id'] is None or
                            role['tenant_id'] == tenant_id):
                        role_name = get_role_name(role['role_id'])
                        req.context['roles'].append(role_name)


class Index(nfw.Resource):
    def __init__(self, app):
        app.router.add(nfw.HTTP_GET, '/', self.index, 'tachyon:public')

    def index(self, req, resp):
        resources = {}
        routes = req.router.routes
        site = req.get_app_url()
        for r in routes:
            r_method, r_uri, r_obj, r_name = r
            if req.policy.validate(r_name):
                url = "%s/%s" % (site, r_uri)
                method = {}
                method[r_method] = r_name
                if url in resources:
                    resources[url]['methods'].append(method)
                else:
                    resources[url] = {}
                    resources[url]['methods'] = []
                    resources[url]['methods'].append(method)
        return json.dumps(resources, indent=4)


class Authenticate(nfw.Resource):
    def __init__(self, app):
        app.router.add(nfw.HTTP_POST, '/login', self.post, 'tachyon:public')
        app.router.add(nfw.HTTP_GET, '/login', self.get, 'tachyon:public')

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

        return [token_id, session_expire]

    def get(self, req, resp):
        if 'user_id' in req.context:
            db = nfw.Mysql()
            sql = "SELECT * FROM user"
            sql += " WHERE id = %s"
            result = db.execute(sql, (req.context['user_id'],))
            db.commit()
            if len(result) == 1:
                creds = {}
                user_id = result[0]['id']
                creds['username'] = result[0]['username']
                creds['email'] = result[0]['email']
                creds['token'] = req.context['token']
                sql = "SELECT * FROM token where token = %s"
                token_result = db.execute(sql, (req.context['token'],))
                creds['expire'] = token_result[0]['token_expire'].strftime("%Y/%m/%d %H:%M:%S")
                creds['roles'] = get_user_roles(user_id)
                return json.dumps(creds, indent=4)
        else:
            return "{}"

    def post(self, req, resp):
        db = nfw.Mysql()
        creds = json.loads(req.read())
        usern = creds.get('username', '')
        passw = creds.get('password', '')
        domain = req.headers.get('X-Domain', 'default')
        sql = "DELETE FROM token WHERE token_expire < NOW()"
        db.execute(sql)
        domain_id = get_domain_id(domain)
        sql = "SELECT * FROM user"
        sql += " WHERE username = %s and domain_id = %s"
        result = db.execute(sql, (usern, domain_id))
        db.commit()
        if len(result) == 1:
            if nfw.password.valid(passw, result[0]['password']):
                creds = {}
                user_id = result[0]['id']
                creds['username'] = result[0]['username']
                creds['email'] = result[0]['email']
                token, expire = self._new_token(result[0]['id'])
                creds['token'] = token
                creds['expire'] = expire.strftime("%Y/%m/%d %H:%M:%S")
                creds['roles'] = get_user_roles(user_id)
                return json.dumps(creds, indent=4)
            else:
                raise nfw.HTTPError(nfw.HTTP_404, 'Authentication failed',
                                    'Could not validate username' +
                                    ' and password credentials')
        else:
            raise nfw.HTTPError(nfw.HTTP_404, 'Authentication failed',
                                'Could not validate username' +
                                ' and password credentials')


class Users(nfw.Resource):
    def __init__(self, app):
        app.router.add(nfw.HTTP_GET, '/users', self.get, 'users:view')
        app.router.add(nfw.HTTP_GET, '/users/{id}', self.get, 'users:view')
        app.router.add(nfw.HTTP_POST, '/users', self.post, 'users:admin')
        app.router.add(nfw.HTTP_PUT, '/users/{id}', self.put, 'users:admin')
        app.router.add(nfw.HTTP_DELETE, '/users/{id}', self.delete,
                       'users:admin')

    def get(self, req, resp, id=None):
        return api.get(model.Users, req, resp, id)

    def post(self, req, resp):
        return api.post(model.User, req)

    def put(self, req, resp, id):
        return api.put(model.User, req, id)

    def delete(self, req, resp, id):
        return api.delete(model.User, req, id)
