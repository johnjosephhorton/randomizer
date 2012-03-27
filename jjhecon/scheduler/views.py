#!/usr/bin/env python
from jjhecon.randomizer.views import base_url
from datetime import datetime, timedelta 
from urlparse import urlparse, urlunparse, urljoin
from urllib import urlencode
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from jjhecon.randomizer.views import create_hash
from jjhecon.scheduler.models import Counter

time_hash_sep = 'p'
MINUTE_TOLERANCE = 2
PLAYERS_PER_GAME = 2

# TODO: make it work even if JS is disabled?
# make sure that assignmentId is unique.

def make_confirmation_code(ref_dt = datetime.utcnow()):
    """Part common, part time-related, and part unique."""
    common = "jhcw"
    time_related = ref_dt.strftime("%jp%H")
    unique = create_hash(3)
    return time_hash_sep.join([common, time_related, unique])

def encode(key, s):
    encoded_chars = []
    for i in xrange(len(s)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(s[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)

def decode(key, s):
    encoded_chars = []
    for i in xrange(len(s)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(s[i]) - ord(key_c)) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)


def encode_time(dt):
    """for the time being this will be a very weak function"""
    s = time_hash_sep.join(map(str, dt.timetuple()[:6]))
    return s[1:len(s)] + s[0]
    
def decode_time(time_hash):
    h = time_hash
    h = h[len(h)-1] + h[0:(len(h) - 1)]
    timetup = map(int, h.split(time_hash_sep))
    return datetime(*timetup)
    
def within(dt, ref_dt, minutes):
    """returns a bool saying whether the two datetimes are within [minutes] of each other"""
    d = timedelta(minutes = minutes)
    return ref_dt - d <= dt <= ref_dt + d

def revisit_time(now):
    """one hour from now"""
    next_hour = datetime(now.year, now.month, now.day, now.hour) + timedelta(hours = 1)
    return next_hour  

def schedule(request):
    if request.method == 'POST':
        # the person is submitting the completion code. should be simple
        pass
    else:
        # revisit time (UTC) as string
        # time delta
        now = datetime.utcnow()
        next_hour = revisit_time(now) 
        time_hash = encode_time(next_hour)
        seconds_till =  (next_hour - now).seconds
        url = urljoin(base_url, '/s/visit') + "?t=" + time_hash 
        return render_to_response('schedule.html',
                                  {'minutes': MINUTE_TOLERANCE,
                                   'seconds_till': seconds_till,
                                   'url': url})

def scheduled_visit(request):
    time_hash = request.GET['t']
    ref_dt = decode_time(time_hash)
    if within(datetime.utcnow(), ref_dt, MINUTE_TOLERANCE):
        confirmation_code = make_confirmation_code(ref_dt)
        return render_to_response('thanks.html', {'confirmation_code': confirmation_code})
    else:
        return render_to_response('wrong_time.html', {})

def check_conf_code(request):
    # check the counter
    user_count = request.POST['count']
    hit_id = request.POST['hit_id']
    current_count = WaitVisit.all().filter('hit_id =', hit_id).count()
    if current_count - user_count >= (PLAYERS_PER_GAME - 1):
        conf_code = WaitVisit.all().filter('hit_id =', hit_id).filter('assignment_id =', assignment_id).get().confirmation_code
        return HttpResponse(conf_code)
    else:
        return HttpResponse('')

def wait(request): 
    hit_id = request.GET['hitId']
    assignment_id = request.GET['assignmentId']
    previous_visit = WaitVisit.all().filter('hit_id =', hit_id).filter('assignment_id =', assignment_id).get() 
    if not previous_visit:
        # check if assignment ID is unique
        visit = WaitVisit(hit_id = hit_id, 
                          assignment_id = assignment_id,
                          confirmation_code = make_confirmation_code())
        visit.put()
        count = WaitVisit.all().filter('hit_id =', hit_id).count()
        return render_to_response("test.html", {'count': count,
                                                'hit_id': hit_id})
    # handle previous visit!        
        
    