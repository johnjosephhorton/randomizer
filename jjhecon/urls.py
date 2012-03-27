from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    
    (r'^r/?$', 'jjhecon.randomizer.views.json_view'), # deprecate this
    (r'^r/.json/?$', 'jjhecon.randomizer.views.json_view'),
    (r'^r/.html/?$', 'jjhecon.randomizer.views.html_view'),
    (r'^r/(\w+)/?$', 'jjhecon.randomizer.views.visit'),
    (r'^r/a/(\w+)/?$', 'jjhecon.randomizer.views.admin'),
    (r'^wait/?$', 'jjhecon.scheduler.views.wait'),
    (r'^schedule/?$', 'jjhecon.scheduler.views.schedule'),
    (r'^sandbox/?$', 'jjhecon.randomizer.views.sandbox'),
    (r'^s/mturk_iframe/?$', 'jjhecon.scheduler.views.mturk_iframe'),
)