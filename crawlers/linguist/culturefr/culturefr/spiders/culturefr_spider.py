import scrapy

from culturefr.items import CulFrItem

class culturefrSpider(scrapy.spiders.CrawlSpider):
    name = "culturefr"

    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.culture.fr',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Cookie': 'JSESSIONID=0000yhwhUcEw3_22J8G-wv8AJKp:17ce3jce0; WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=pco79X70sLRn64aWGIeArIFdQ0c%3D%0A%3B2017-11-21+07%3A18%3A25.272_1511248705139-793450_10151_-1002%2C44%2CGBP_10151; WC_ACTIVEPOINTER=44%2C10151; WC_USERACTIVITY_-1002=-1002%2C10151%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cm%2BgDwz%2B%2FRY8zvKqZ0DffWVy7jUeBC1QlMMAdItOjo9LMMsCHDFo%2B9M0IL6hi5nIHn7ckczF2a5Y5hQAEBZk9cMt1HJfmQ6D5zzYeCD8tU%2F1fK5U%2Bk7VOPgJ4Z9XmosJEnBTCLto%2FS0hbgJE8a96LKaq6%2Bpbn0WEDaT9EBWnrIx358Rvolsm6Bqt297%2B0cDpoxUzJ2Zws1017LL250OsvyA%3D%3D; WC_GENERIC_ACTIVITYDATA=[114397727425%3Atrue%3Afalse%3A0%3ALyLiqyJ%2FWQfkz0myNqP5aGawatU%3D][com.pf.commerce.context.entitlement.PFEntitlementContext|10504%2610504%26null%26null%2610503%26null%26true%26false%26true%26null%26null%26null][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.pf.commerce.checkout.context.PFCheckoutStubContext|null][com.ibm.commerce.context.globalization.GlobalizationContext|44%26GBP%2644%26GBP][com.pf.commerce.punchout.businesscontext.PunchoutContext|null%26false%26false%26false%26false%26null][com.pf.commerce.ibuy.businesscontext.IBuyContext|null%26null%26false%26null%26null%26null%26null%26null%26false%26null][com.pf.commerce.context.generic.PFGenericContext|null][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.base.BaseContext|10151%26-1002%26-1002%26-1][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null][com.ibm.commerce.context.entitlement.EntitlementContext|10504%2610504%26null%26-2000%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|1511248705139-793450][com.ibm.commerce.catalog.businesscontext.CatalogContext|15001%26null%26false%26false%26false][com.ibm.commerce.context.ExternalCartContext|null][com.pf.commerce.cms.preview.context.CMSPreviewContext|contentStoreKey%253Dlocal]; ecommerce=!NLenDdLQFX7Au3fPJjYExyJUMpzrp9a8KE35uWiSF8OGs8fN1AE5jrg+D0JRmIJDRsDfL1uzb1GB3wA=; TS01764c4c=0114f16688178eab7f28ce1df683bd2dc93d8712c54bdc571e5ba725440ac407487f2fa8dba61bce592ea0b4fafd37b2c1029b5998e35a304e2ac47eb7ac4e3d1d8bafa1ca7d7ec1395261c9ade2c08aa3f75164122c7453d909bb1faa139cd37e8307f94c2b3a7eca2e70690090bd18ca1367894b8b4503adb538ad8fce37cc5561c43fcde41c99be51d2c8c8c0ff760252bbb614ff16e75f9c37a4ea6d4138a7534fd97b; TS01764c4c_28=012999ca9fae237a956f15fc1676c71ddcbf1795d6206097305617f351c2059f0ab25362a3b99469db6ecbd2a732825ecd54b91dbe; _gat=1; _ga=GA1.2.1588063891.1511248707; _gid=GA1.2.1975707125.1511248707; _gat_globalTracker=1; AMCVS_106315F354E6D5430A4C98A4%40AdobeOrg=1; AMCV_106315F354E6D5430A4C98A4%40AdobeOrg=2121618341%7CMCIDTS%7C17492%7CMCMID%7C46493241841194068262558362732145556967%7CMCAAMLH-1511853507%7C11%7CMCAAMB-1511853507%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1511255907s%7CNONE%7CMCAID%7CNONE; PF_LOOKAHEAD_10151=true; ak_bmsc=CDEF26B6059B3DB55652DAE90A3E96F6173B9755767F000042D3135A8C719E4B~plpY2lztvrT1iCIcVwp+BKPK0UvWRKKrWXtC8G40wg0Ld03CNoz8Mrkepo8kvG3T4D8JhCVhhOpOAObx088PsgwRN7lwTLEyYkMzbJLIO1ADMZlqOdLWRbie10OkiCoxyI13qJBSXBOr5qAAfWDEM+aWRJO4Qy/rEqMR2KjvBPUdlxNbga00j3q14wq8JUQW2SmRwbs2a4TgGPsWtoaWoh2s+fphTf7Oa/c8gPrp7qO8hAoYTqJ1NcfiJZWEab/FTv; s_cc=true; _uetsid=_uet781b3c95; mbox=session#1b2f93bc483042ef8f379b21d4b24e87#1511250569|PC#1b2f93bc483042ef8f379b21d4b24e87.22_23#1574493509; check=true; __hstc=234022017.61a4bd7cff672fa54b46bfa7bc4c512e.1511248709483.1511248709483.1511248709483.1; __hssrc=1; __hssc=234022017.1.1511248709484; hubspotutk=61a4bd7cff672fa54b46bfa7bc4c512e; bn_u=6927000838294904423; bm_sv=408EBFC582EF7D8E356A62242BB9CD2B~DASyDJpvXa3P54NbFvuFXFNUHq8oAwO0qSatbnEhEni8q9dtkHoe1ySmS7TjbnzMfsh7Eg1L9TsH9X+LFVchaV8Ri3V/Rj2Hd00Hy99TCSSNH+B5e60AQzy/bBZELxTxAsMkHaYsiBXjyuOjUwmWB6fkRoi/AnOIwsW8TwH3yzk=',
            'Connection': 'keep-alive',
        }

    def start_requests(self):
        start_url = 'http://www.culture.fr/franceterme/result?francetermeSearchTerme='
        '&francetermeSearchDomaine=13'
        '&francetermeSearchSubmit=rechercher'
        '&action=search'

        yield scrapy.Request(url=start_url, headers=self.headers,
                             callback=self.parse, meta={'recnt': 0})

    def reform(self, _str):
        result = _str.split(',')[0]

        result = result.replace("  ", "")
        result = result.replace("\t", "")
        result = result.replace("\n", "")

        if result.endswith(" "):
            result = result[:-1]

        return result

    def get_item(self, word_item, _url):
        cfi = CulFrItem()
        cfi['word_name'] = self.reform(word_item.xpath('h3//text()')[0].extract())

        date_gras = word_item.xpath('span//text()').extract()[1]
        cfi['journal_official_du'] = date_gras

        cfi['source'] = _url

        dt_list = word_item.xpath('dl/dt')

        for dt in dt_list:
            dt_name = dt.xpath('text()').extract()[0]

            dd = dt.xpath('following-sibling::dd//text()')[0].extract()
            dd_value = self.reform(dd)

            if 'Domaine' in dt_name:
                cfi['domain'] = dd_value

            if 'Synonyme' in dt_name:
                cfi['synonyme'] = dd_value

            if 'Définition' in dt_name:
                cfi['definition'] = dd_value

            if 'Note' in dt_name:
                cfi['note'] = dd_value

            if 'Voir aussi' in dt_name:
                cfi['voir_aussi'] = dd_value

            if 'Équivalent étranger' in dt_name:
                cfi['equivalent'] = dd_value

        return cfi

    def parse(self, response):
        word_list = response.xpath('//div[@id="detail"]')

        recnt = response.meta['recnt']

        if not word_list and recnt < 3:
            scrapy.Request(url=response.url, headers=self.headers,
                           callback=self.parse, meta={'recnt': recnt+1})

        for word_item in word_list:
            result = self.get_item(word_item, response.url)

            yield result


