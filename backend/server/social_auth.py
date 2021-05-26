import requests
from django.conf import settings
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.backends.github import GithubOAuth2
from social_core.backends.okta import OktaOAuth2
from social_core.backends.okta_openidconnect import OktaOpenIdConnect


# noinspection PyUnusedLocal
def fetch_github_permissions(strategy, details, user=None, is_new=False, *args, **kwargs):
    org_name = getattr(settings, 'GITHUB_ADMIN_ORG_NAME', '')
    team_name = getattr(settings, 'GITHUB_ADMIN_TEAM_NAME', '')
    if not user or not isinstance(kwargs['backend'], GithubOAuth2) or not org_name or not team_name:
        return

    response = requests.post(
        url='https://api.github.com/graphql',
        headers={
            'Authorization': 'Bearer {}'.format(kwargs['response']['access_token']),
        },
        json={
            'query': '''
                query($userName: String!, $orgName: String!, $teamName: String!) {
                    organization(login: $orgName) {
                        teams(query: $teamName, userLogins: [$userName], first: 1) {
                            nodes {
                                name
                            }
                        }
                    }
                }
            ''',
            'variables': {
                'userName': details['username'],
                'orgName': org_name,
                'teamName': team_name,
            }
        }
    )
    response.raise_for_status()
    response = response.json()

    is_superuser = {'name': team_name} in response['data']['organization']['teams']['nodes']

    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        user.save()


# noinspection PyUnusedLocal
def fetch_azuread_permissions(strategy, details, user=None, is_new=False, *args, **kwargs):
    group_id = getattr(settings, 'AZUREAD_ADMIN_GROUP_ID', '')
    if not user or not isinstance(kwargs['backend'], AzureADTenantOAuth2) or not group_id:
        return

    response = requests.post(
        url='https://graph.microsoft.com/v1.0/me/checkMemberGroups',
        headers={
            'Authorization': 'Bearer {}'.format(kwargs['response']['access_token']),
        },
        json={
            'groupIds': [group_id]
        }
    )
    response.raise_for_status()
    response = response.json()

    is_superuser = group_id in response['value']

    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        user.save()


# noinspection PyUnusedLocal
def fetch_okta_oauth2_permissions(strategy, details, user=None, is_new=False, *args, **kwargs):
    org_url = getattr(settings, 'SOCIAL_AUTH_OKTA_OAUTH2_API_URL', '')
    admin_group_name = getattr(settings, "OKTA_OAUTH2_ADMIN_GROUP_NAME", "")
    if not user or not isinstance(kwargs['backend'], OktaOAuth2):
        return

    # OktaOpenIdConnect inherits `OktaOAuth2`, so we have to explicitly skip OAuth2 trying
    # to fetch permissions when using OIDC backend.
    if isinstance(kwargs['backend'], OktaOpenIdConnect):
        return

    response = requests.post(
        url=f"{org_url}/v1/userinfo",
        headers={
            'Authorization': 'Bearer {}'.format(kwargs['response']['access_token']),
        },
    )
    response.raise_for_status()
    response = response.json()

    is_superuser = admin_group_name in response.get("groups", [])
    is_staff = admin_group_name in response.get("groups", [])

    user_changed = False

    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        user_changed = user_changed or True

    if user.is_staff != is_staff:
        user.is_staff = is_staff
        user_changed = user_changed or True

    if user_changed:
        user.save()


# noinspection PyUnusedLocal
def fetch_okta_openidconnect_permissions(strategy, details, user=None, is_new=False, *args, **kwargs):
    org_url = getattr(settings, 'SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL', '')
    admin_group_name = getattr(settings, "OKTA_OPENIDCONNECT_ADMIN_GROUP_NAME", "")
    if not user or not isinstance(kwargs['backend'], OktaOpenIdConnect):
        return

    response = requests.post(
        url=f"{org_url}/v1/userinfo",
        headers={
            'Authorization': 'Bearer {}'.format(kwargs['response']['access_token']),
        },
    )
    response.raise_for_status()
    response = response.json()

    is_superuser = admin_group_name in response.get("groups", [])
    is_staff = admin_group_name in response.get("groups", [])

    user_changed = False

    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        user_changed = user_changed or True

    if user.is_staff != is_staff:
        user.is_staff = is_staff
        user_changed = user_changed or True

    if user_changed:
        user.save()
