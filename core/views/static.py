import json
import os
import time

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from psutil import Process

from chronam.core.decorator import add_cache_headers
from chronam.core.models import Language


@never_cache
def healthz(request):
    status = {
        "current_time": time.time(),
        "load_average": os.getloadavg(),
        "process_creation_time": Process().create_time(),
    }

    # We don't want to query a large table but we do want to hit the database
    # at last once:
    status["database_has_data"] = Language.objects.count() > 0

    # We'll intentionally touch the storage paths to turn failed network mounts
    # into failed health-checks. This would be less generic if we did an
    # os.path.ismount() tests on the ones which are independent mounts so we're
    # not doing that.
    status["storage"] = {
        k: os.path.isdir(getattr(settings, k))
        for k in ("BATCH_STORAGE", "BIB_STORAGE", "COORD_STORAGE", "OCR_DUMP_STORAGE", "TEMP_STORAGE")
    }

    return HttpResponse(content=json.dumps(status), content_type="application/json")


@add_cache_headers(settings.LONG_TTL_SECONDS, settings.SHARED_CACHE_MAXAGE_SECONDS)
def about(request):
    page_title = "About Chronicling America"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{"label": "About", "href": urlresolvers.reverse("chronam_about"), "active": True}])
    return render_to_response("about.html", dictionary=locals(), context_instance=RequestContext(request))


@add_cache_headers(settings.LONG_TTL_SECONDS, settings.SHARED_CACHE_MAXAGE_SECONDS)
def about_api(request):
    page_title = "About the Site and API"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{"label": "About API", "href": urlresolvers.reverse("chronam_about_api"), "active": True}])
    return render_to_response("about_api.html", dictionary=locals(), context_instance=RequestContext(request))


@add_cache_headers(settings.LONG_TTL_SECONDS, settings.SHARED_CACHE_MAXAGE_SECONDS)
def help(request):
    page_title = "Help"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{"label": "Help", "href": urlresolvers.reverse("chronam_help"), "active": True}])
    return render_to_response("help.html", dictionary=locals(), context_instance=RequestContext(request))


@add_cache_headers(settings.LONG_TTL_SECONDS, settings.SHARED_CACHE_MAXAGE_SECONDS)
def favicon(request):
    return HttpResponseRedirect(static("img-std/fav.ico"))
