from sites.scraping_hh import HHGetInformation


class HhLinks(HHGetInformation):
    async def get_content_from_link(self, return_raw_dictionary=False):
        self.found_by_link = 0
        for link in self.list_links:
            await self.report.collect_parser_links(link)
        pass


