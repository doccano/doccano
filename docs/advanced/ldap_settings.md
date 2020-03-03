# LDAP setup for doccano

This document aims to instruct how to setup LDAP for doccano.

## Set environment variables

In general, the variable AUTH_LDAP_SERVER_URI is the variable that determines whether LDAP authentication is activated.

If AUTH_LDAP_SERVER_URI is defined, than 'django_auth_ldap.backend.LDAPBackend' is added to AUTHENTICATION_BACKENDS. The standard django user authentication is also still available to assign permissions to individual users or add users to groups within Django.

AUTH_LDAP_SERVER_URI defines the URI of the LDAP server.
AUTH_LDAP_BIND_DN is the distinguished name to use when binding to the LDAP server (with AUTH_LDAP_BIND_PASSWORD). Use the empty string for an anonymous bind.
AUTH_LDAP_USER_DN_TEMPLATE is a string template that describes any user’s distinguished name based on the username. This must contain the placeholder **%(user)s**.
AUTH_LDAP_USER_ATTR_MAP is a mapping from User field names to LDAP attribute names. A users’s User object will be populated from his LDAP attributes at login.

## Example configuration

```
AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"
AUTH_LDAP_BIND_DN = "cn=django-agent,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "yoursecretpassword"
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=users,dc=example,dc=com'
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
```

## Run server

```bash
python manage.py runserver
```

Your LDAP login is now part of doccano's login page with its fields for username and password. As defined the provided username will be used for the LDAP user template.

## Additional sources for configuration

* <https://django-auth-ldap.readthedocs.io>
* <https://www.python-ldap.org>
