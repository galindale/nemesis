# -*- coding: utf-8 -*-

import json

from bottle import request, abort, route

from nemesis import constants
from nemesis.utils import get_utc_from_str, get_all_dates, get_labels
from nemesis.api.common import authorize
from nemesis.models.users import UserSlack
from nemesis.models.reports import UserStatusReport


@route('/last-reports/<user>/', method='GET')
@authorize(request)
def last_user_reports(user):
    user = UserSlack.get_user(user)
    if user is None:
        abort(404, "User does not exist")
    result = user.serialize()

    query = UserStatusReport.objects.filter(user=user)
    query = query.order_by('reported_at')[0:constants.MAX_LAST_REPORTS]
    result.update({'status_avg': query.average('status')})
    reports = []
    for status in query:
        reports.append(status.serialize())
    result.update({'reports': reports})

    return json.dumps(result)


@route('/last-reports/', method='GET')
@authorize(request)
def last_reports():
    query = UserStatusReport.objects.all()

    reports = []
    for status in query.order_by('-reported_at')[0:constants.MAX_LAST_REPORTS]:
        reports.append(status.serialize(user=True))

    return json.dumps(reports)


@route('/users-reports/', method='GET')
@authorize(request)
def users_reports():
    users = request.query.users.split(',')
    start_date = get_utc_from_str(request.query.start_date)
    end_date = get_utc_from_str(request.query.end_date)
    all_dates = get_all_dates(start_date, end_date)

    users = UserSlack.objects.filter(slack_id__in=users)
    query = UserStatusReport.objects.filter(reported_at__gte=start_date)
    query = query.filter(reported_at__lte=end_date)

    global_reports = {'global_status_avg': query.average('status'), 'users_reports': [], 'labels': get_labels(all_dates)}
    for user in users:
        user_query = query.filter(user=user)
        report = {'user_avg': user_query.average('status'), 'user': user.serialize(), 'reports': []}
        for label in all_dates:
            user_report = UserSlack.get_user_status_from_day(user, label)
            report['reports'].append(user_report.status if user_report is not None else 0)
        global_reports['users_reports'].append(report)

    return json.dumps(global_reports)
