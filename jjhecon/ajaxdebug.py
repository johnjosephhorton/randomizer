from django.conf import settings
from django.http import HttpResponseServerError

class SimpleExceptionResponse:
    def process_exception(self, request, exception):
        if settings.DEBUG:
            #if request.is_ajax():
            import sys, traceback
            (exc_type, exc_info, tb) = sys.exc_info()
            response = "%s<br>\n" % exc_type.__name__
            response += "%s<br>\n\n" % exc_info
            response += "TRACEBACK:<br>\n"    
            for tb in traceback.format_tb(tb):
                response += "%s<br>\n" % tb
            return HttpResponseServerError(response)