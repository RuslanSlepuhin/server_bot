import asyncio

from report.reports import Reports

from sites.hh_get_report_links import HhLinks

hh = HhLinks(main_class=None, bot_dict=None, report=Reports())
asyncio.run(hh.get_content(words_pattern=['junior']))