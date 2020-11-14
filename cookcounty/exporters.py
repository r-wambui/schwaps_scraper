import scrapy.exporters


class NoHeaderCsvItemExporter(scrapy.exporters.CsvItemExporter):
    def __init__(self, file, join_multivalued=', ', **kwargs):
        super(NoHeaderCsvItemExporter, self).__init__(
            file=file, include_headers_line=False, join_multivalued=join_multivalued, **kwargs)
