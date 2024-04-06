from sites.scraping_hh import HHGetInformation
import asyncio

class HHKzGetInformation(HHGetInformation):

    async def get_content(self, *args, **kwargs):
        self.base_url = "https://hh.kz"
        self.source_title_name = "https://hh.kz"
        self.source_short_name = "HHKZ"
        await super().get_content(*args, **kwargs)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(HHKzGetInformation().get_content())