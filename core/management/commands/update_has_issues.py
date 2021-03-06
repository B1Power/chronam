from __future__ import absolute_import, print_function

from chronam.core import models as m

from . import LoggingCommand


class Command(LoggingCommand):
    help = "Updates the Title.has_issues property appropriately"  # NOQA: A003

    def handle(self, *args, **options):
        q = m.Title.objects.filter(pk__in=m.Issue.objects.values("title"))
        q = q.distinct()
        for t in q:
            self.stdout.write(u"%s has issues" % t)
            t.has_issues = True
            t.save()
