def get_calendars(p_service_calendar):
    """
    Gets list of all calendars in Google classroom
    Args:
        p_service_calendar: Service object of Google calendar API

    Returns:
        list of all calendars.
    """
    values = p_service_calendar.calendarList().list().execute()
    values = values['items']
    return values


def get_calendar_id(p_name, p_calendars):
    """
    Gets the ID, given a list of calendars
    Args:
        p_name: name of calendar we are looking for (str)
        p_calendars: list of calendars, output of get_calendars

    Returns:
        id of calendar we are looking for (str).  If not found, returns none.
    """
    import re
    # Search for name.  If name is not unique, then may return wrong calendar
    candidate_calendars = []
    for calendar in p_calendars:
        # print(calendar)
        if re.search(p_name, calendar[ 'summary']):
            candidate_calendars.append(calendar)
    if len(candidate_calendars) > 1:
        raise ValueError("The calendar you are looking for is not unique.  Here are candidate calendars: " +
                         str(candidate_calendars))
    elif len(candidate_calendars) == 0:
        raise ValueError("Did not find a calendar with this name in it: " + str(p_name))
    else:
        id = candidate_calendars[0]['id']
        return id

#
#
# def insert_event(request_id, response, exception):
#   if exception is not None:
#     # Do something with the exception
#      pass
#   else:
#     # Do something with the response
#     pass
#
# service = build('calendar', 'v3')
#
# batch = BatchHttpRequest(callback=insert_event)
#
# batch.add(service.events().quickAdd(calendarId="you@domain.com",
#   text="Lunch with Jim on Friday"))
# batch.add(service.events().quickAdd(calendarId="you@domain.com",
#   text="Dinner with Amy on Saturday"))
# batch.add(service.events().quickAdd(calendarId="you@domain.com",
#   text="Breakfast with John on Sunday"))
# batch.execute(http=http)



# After switching to using the new batch API/endpoint (service.new_batch_http_request), following problems have emerged:
# 1. creating a calendar with the new batch API produces calendar invisible to the user
# 2. attempting to add it using calendarList.insert fails with HttpError 404
# 3. when NOT using batch
#     a. created calendars and events show up fine on the user's side
#     b. attempting to access/modify the created calendars with batch fails with HttpError 404
#
# A small code sample that reliably reproduces the issue. The sample should run as-is or with minimal setup, without external dependencies.
#
# from apiclient.discovery import build
# from oauth2client.contrib.appengine import StorageByKeyName
#
# creds = StorageByKeyName(<Class Name>, <Storage Key>, <Property Name>).locked_get()
# http = creds.authorize(httplib2.Http(timeout=15))
# service = build('calendar', 'v3')
#
# # batch call (works fine, but produces calendar invisible to the user and to one-by-one API calls)
# batch = service.new_batch_http_request()
# batch.add(service.calendars().insert(body={'summary': 'Using batch'}, fields='id'), callback=.., request_id=..)
# batch.execute(http=http)
#
# # non-batch call (produces calendar correctly visible to the user but invisible to the batch API calls)
# service.calendars().insert(body={'summary': 'Using one-by-one'}, fields='id').execute(http=http)
