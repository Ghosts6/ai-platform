from django.shortcuts import redirect
from django.conf import settings
from O365 import Account
from profiles.models import O365Token
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.http import HttpResponse

@login_required
def microsoft_login(request):
    credentials = (settings.MS_CLIENT_ID, settings.MS_CLIENT_SECRET)
    account = Account(credentials, tenant_id=settings.MS_TENANT_ID, auth_flow_type='web')
    url, state = account.get_authorization_url(
        requested_scopes=['offline_access', 'User.Read', 'Calendars.ReadWrite', 'Mail.ReadWrite'],
        redirect_uri=settings.MS_REDIRECT_URI
    )
    request.session['ms_auth_state'] = state
    return redirect(url)

@login_required
def microsoft_callback(request):
    credentials = (settings.MS_CLIENT_ID, settings.MS_CLIENT_SECRET)
    account = Account(credentials, tenant_id=settings.MS_TENANT_ID, auth_flow_type='web')
    state = request.session.pop('ms_auth_state', None)
    
    # The library expects the full callback URL
    callback_url = request.build_absolute_uri()

    if not state or state != request.GET.get('state'):
        return redirect('ms_auth:error')

    if account.authenticate(callback=callback_url):
        token = account.connection.get_session().token
        expiry_time = timezone.now() + datetime.timedelta(seconds=token['expires_in'])

        O365Token.objects.update_or_create(
            user=request.user,
            defaults={
                'access_token': token['access_token'],
                'refresh_token': token.get('refresh_token'),
                'token_expiry': expiry_time
            }
        )
        return redirect('/') 
    else:
        return redirect('ms_auth:error')

def error(request):
    return HttpResponse("Authentication Error")
