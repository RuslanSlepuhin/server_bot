from sites.scraping_hh import HHGetInformation

class HHKzGetInformation(HHGetInformation):

    async def get_content(self, *args, **kwargs):
        self.base_url = "https://hh.kz"
        self.source_title_name = "https://hh.kz"
        self.source_short_name = "HHKZ"
        await super().get_content(*args, **kwargs)

