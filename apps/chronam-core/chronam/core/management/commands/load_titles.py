import logging

from datetime import datetime

from django.core.management.base import BaseCommand

from chronam.core.title_loader import TitleLoader
from chronam.core.index import index_titles
from chronam.utils import configure_logging
    
configure_logging('load_titles_logging.config', 'load_titles.log')
_logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Load a marcxml file of title records"
    args = '<marcxml file>'

    def handle(self, marc_xml, *args, **options):
        _logger.info("loading marcxml title records from %s" % marc_xml)
        start_time = datetime.now()
        loader = TitleLoader()
        loader.main(marc_xml)
        # need to index any titles that we just created 
        _logger.info("indexing new titles")
        index_titles(since=start_time)
        _logger.info("finished loading marcxml titles from %s" % marc_xml)
