# -*- coding: utf-8 -*-

import pytz
import json

from datetime import datetime

from slackclient import SlackClient
from bottle import get, request, abort

from nemesis import constants
from nemesis.config import options
from nemesis.models import UserSlack, UserStatusReport


client_id = '155087779333.156380766404'
client_secret = '450fe2b89e125113a82e13af8b2b2af9'
oauth_scope = 'admin'


def authorize(request):
    def check_token(api_func):
        def wrapper(**kwds):
            auth_token = request.headers.get('Token')
            print(auth_token)
            if auth_token is not None:
                res = SlackClient(auth_token).api_call("users.identity", scope="identity.basic")
                print(res)
                if res['ok'] is False:
                    abort(401, "Not authorized")
                return api_func(**kwds)
            else:
                abort(401, "Not authorized")
        return wrapper
    return check_token


@get("/begin_auth")
def pre_install():
    return '<a href="https://slack.com/oauth/authorize?scope=identity.basic&client_id=155087779333.156380766404"><img alt="Sign in with Slack" height="40" width="172" src="https://platform.slack-edge.com/img/sign_in_with_slack.png" srcset="https://platform.slack-edge.com/img/sign_in_with_slack.png 1x, https://platform.slack-edge.com/img/sign_in_with_slack@2x.png 2x" /></a>'


@get("/auth-token/")
def auth_token():

    auth_code = request.query.code

    slack_client = SlackClient("")
    auth_response = slack_client.api_call(
        "oauth.access",
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code
    )

    return json.dumps(auth_response)


@get('/last-reports/')
@get('/last-reports/<user>/')
@authorize(request)
def last_reports(user=None):
    query = UserStatusReport.objects.all()
    if user is not None:
        user = UserSlack.get_user(user)
        if user is None:
            return json.dumps([])
        query = query.filter(user=user)

    reports = []
    for status in query.order_by('-reported_at')[0:constants.MAX_LAST_REPORTS]:
        reports.append(status.serialize())

    return json.dumps(reports)


def get_utc_from_str(dt_str):
    dt = datetime.strptime(dt_str, '%d-%m-%Y')
    current_tz = pytz.timezone(options.nemesis_timezone)
    return current_tz.localize(dt)


@get('/users-reports/')
def users_reports():
    users = request.query.users.split(',')
    start_date = get_utc_from_str(request.query.start_date)
    end_date = get_utc_from_str(request.query.end_date)

    users = UserSlack.objects.filter(slack_id__in=users)
    query = UserStatusReport.objects.filter(reported_at__gte=start_date)
    query = query.filter(reported_at__lte=end_date)

    global_reports = {'global_status_avg': query.average('status'), 'users_reports': []}
    for user in users:
        query = query.filter(user=user)
        report = {'user_avg': query.average('status'), 'reports': []}
        for user_report in query.filter(user=user).order_by('-reported_at'):
            report['reports'].append(user_report.serialize())
        global_reports['users_reports'].append(report)

    return json.dumps(global_reports)
