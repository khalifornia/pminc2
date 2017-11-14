
#Used for interpreter/debugger
#change name of spider accordingly

import sys
sys.path.insert(0, "C:/Users/fbgnew/PycharmProjects/fbg/procurematch_era/pminc/scripts")

from scrapy import cmdline
cmdline.execute("scrapy crawl single_contract".split())