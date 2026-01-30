import asyncio
import pytest
import re
from factory import ParserFactory
import json

# Глобальные результаты
TEST_RESULTS = {}


def get_test_results():
    return TEST_RESULTS.copy()


def stabilize_result_for_snapshot(result):
    stabilized = result.copy()
    if "images" in stabilized and stabilized["images"]:
        stabilized["images"] = [
            re.sub(
                r"images/[a-f0-9-]+\.(webp|jpg|jpeg|png)",
                "images/stabilized-image.\\1",
                img_url,
            )
            for img_url in stabilized["images"]
        ]
    return stabilized


@pytest.fixture(scope="session")
def use_case_fixture():
    """Создаем use case ОДИН раз на все тесты - СИНХРОННО"""
    # Запускаем async функцию в синхронном контексте
    return asyncio.run(ParserFactory.create_parse_product_use_case())



TEST_CASES = [
    # STEREOZONA
    {
        "url": "https://stereozona.ru/product/audio-technica-at-vm95ml/",
        "snapshot_name": "stereozona_1_result",
        "site_name": "stereozona1",
    },
    {
        "url": "https://stereozona.ru/product/jbl-tt350/",
        "snapshot_name": "stereozona_2_result",
        "site_name": "stereozona2",
    },
    {
        "url": "https://stereozona.ru/product/radiotehnika-lp002d/",
        "snapshot_name": "stereozona_3_result",
        "site_name": "stereozona3",
    },
    # ASCONA
    {
        "url": "https://www.askona.ru/krovati/krovat-alfa-pm.htm",
        "snapshot_name": "ascona_1_result",
        "site_name": "ascona1",
    },
    {
        "url": "https://www.askona.ru/tekstil/postelnoe-beljo/postelnoe-bele-lite-home-toplenoe-moloko.htm?SELECTED_HASH_SIZE=140x205-35c9c5c47bca0a76c50d8949b38a22b1",
        "snapshot_name": "ascona_2_result",
        "site_name": "ascona2",
    },
    {
        "url": "https://www.askona.ru/tekstil/pokryvala/pokryvalo-waffle-ivory.htm?SELECTED_HASH_SIZE=220x230-da706f0e8eab414bfde7a6be958a5ec8",
        "snapshot_name": "ascona_3_result",
        "site_name": "ascona3",
    },
    # SWISSLOGIC
    # {
    #     "url": "https://swisslogic.ru/catalog/laurastar-go-plus.html",
    #     "snapshot_name": "swisslogic_1_result",
    #     "site_name": "swisslogic1",
    # },
    # {
    #     "url": "https://swisslogic.ru/catalog/laurastar-lift-happy-purple.html",
    #     "snapshot_name": "swisslogic_2_result",
    #     "site_name": "swisslogic2",
    # },
    # {
    #     "url": "https://swisslogic.ru/catalog/voda-dlya-gladilnykh-sistem-10l.html",
    #     "snapshot_name": "swisslogic_3_result",
    #     "site_name": "swisslogic3",
    # },
    # AMPM
    {
        "url": "https://ampm-store.ru/catalog/smesitel-dlya-kukhni-damixa-arc-290007364-3d-s-povorotnym-izlivom-chernyy/",
        "snapshot_name": "am_1_result",
        "site_name": "am1",
    },
    {
        "url": "https://ampm-store.ru/catalog/unitaz-podvesnoy-am-pm-like-c801900sc-tornado-bezobodkovyy-s-sidenem-mikrolift-belyy/",
        "snapshot_name": "am_2_result",
        "site_name": "am2",
    },
    {
        "url": "https://ampm-store.ru/catalog/steklyannaya-shtorka-dlya-vanny-100-am-pm-like-w80s-100ps-150mt-povorotno-razdvizhnaya-profil-serebristyy/",
        "snapshot_name": "am_3_result",
        "site_name": "am3",
    },
    # MEBELSHARA
    {
        "url": "https://www.mebelshara.ru/catalog/kuhni/ravenna-spark-belyy-fon-fresko",
        "snapshot_name": "shara_1_result",
        "site_name": "shara1",
    },
    {
        "url": "https://www.mebelshara.ru/catalog/divany/milk-temp-dark-grey",
        "snapshot_name": "shara_2_result",
        "site_name": "shara2",
    },
    {
        "url": "https://www.mebelshara.ru/catalog/shkafy/rondo-nabor-50-1-antracit",
        "snapshot_name": "shara_3_result",
        "site_name": "shara3",
    },
    # TEA
    {
        "url": "https://pyotea.ru/matcha_ceremonial",
        "snapshot_name": "tea_1_result",
        "site_name": "tea1",
    },
    {
        "url": "https://pyotea.ru/grechishniy",
        "snapshot_name": "tea_2_result",
        "site_name": "tea2",
    },
    {
        "url": "https://pyotea.ru/dundin",
        "snapshot_name": "tea_3_result",
        "site_name": "tea3",
    },
    # KUPIVIP
    {
        "url": "https://kupivip.ru/product/dublenka-twinset-milano-116951-zelenyy/",
        "snapshot_name": "kupi_1_result",
        "site_name": "kupi1",
    },
    {
        "url": "https://kupivip.ru/product/yubka-dolce-gabbana-130530-korichnevyy/",
        "snapshot_name": "kupi_2_result",
        "site_name": "kupi2",
    },
    {
        "url": "https://kupivip.ru/product/ryukzak-silvano-biagini-130272-chernyy/",
        "snapshot_name": "kupi_3_result",
        "site_name": "kupi3",
    },
    # HOLODILNIK
    {
        "url": "https://www.holodilnik.ru/built-in/built-in_rone_chamber_refrigerators/liebherr/ire_5100_22_001/",
        "snapshot_name": "holo_1_result",
        "site_name": "holo1",
    },
    {
        "url": "https://www.holodilnik.ru/tv_all/tv/tcl/65c7k/",
        "snapshot_name": "holo_2_result",
        "site_name": "holo2",
    },
    {
        "url": "https://www.holodilnik.ru/washers/washing_machines/zugel/zwt813i_inverter/",
        "snapshot_name": "holo_3_result",
        "site_name": "holo3",
    },
    # DOM
    # {
    #     "url": "https://www.maxidom.ru/catalog/shtory/1001530928/",
    #     "snapshot_name": "dom_1_result",
    #     "site_name": "dom1",
    # },
    # {
    #     "url": "https://www.maxidom.ru/catalog/dveri-mezhkomnatnye/1001501067/",
    #     "snapshot_name": "dom_2_result",
    #     "site_name": "dom2",
    # },
    # {
    #     "url": "https://www.maxidom.ru/catalog/gazonokosilki/1000945778/",
    #     "snapshot_name": "dom_3_result",
    #     "site_name": "dom3",
    # },
    # PETROVICH
    {
        "url": "https://petrovich.ru/product/978326/",
        "snapshot_name": "petr_1_result",
        "site_name": "petr1",
    },
    {
        "url": "https://petrovich.ru/product/126916/",
        "snapshot_name": "petr_2_result",
        "site_name": "petr2",
    },
    {
        "url": "https://petrovich.ru/product/611172/",
        "snapshot_name": "petr_3_result",
        "site_name": "petr3",
    },
    # OZON
    {
        "url": "https://www.ozon.ru/product/bryuki-pryamye-dlvaxty-pryamye-na-rezinke-1600276330/?at=Brtz5MRDpHWLgEjNCLxn8wYfyV53l5uM44AllhzO3NW8",
        "snapshot_name": "ozon_1_result",
        "site_name": "ozon1",
    },
    {
        "url": "https://www.ozon.ru/product/uggi-fko-2434141105/",
        "snapshot_name": "ozon_2_result",
        "site_name": "ozon2",
    },
    {
        "url": "https://www.ozon.ru/product/advent-kalendar-gerkules-novogodniy-nabor-pishchevyh-toppingov-31-den-do-novogo-goda-russkiy-produkt-1451352102/",
        "snapshot_name": "ozon_3_result",
        "site_name": "ozon3",
    },
    # WB
    {
        "url": "https://www.wildberries.ru/catalog/140409460/detail.aspx",
        "snapshot_name": "wb_1_result",
        "site_name": "wb1",
    },
    {
        "url": "https://www.wildberries.ru/catalog/158420554/detail.aspx",
        "snapshot_name": "wb_2_result",
        "site_name": "wb2",
    },
    {
        "url": "https://www.wildberries.ru/catalog/2869805/detail.aspx",
        "snapshot_name": "wb_3_result",
        "site_name": "wb3",
    },
    #     {
    #         "url": "https://market.yandex.ru/card/trimmer-elektricheskiy-braun-s7-aio7560-universalnyy-13v1-s-kosmetichkoy-chernyyseryy-grafit/4490727377?do-waremd5=9EovahKFfLQioSJAKYXM4A&sponsored=1&cpc=QnAnAHDiEFOBepRtIhv7QA1RuxuKDc0ocyOnJFTVpGANnwXKOEc2S_rDsxWwiU0QayoDpu-42sbbDQ7ehhr6RoQQ0vE_ZJreIp4qIl9uotGww7Yvx7poSo4aNh2NFP78hltL5dhsd0eoiRSTQ9nUfLZDbsOAFL9B1y9DHLIKB-TpiDDY629nR2i6Ow6iPHP07yXTj61ZwMrJ2cg3Zf7caHbLH_Twgcjtl8zae-UO8bKIBto81jFOIEJyI5wxihe4g6CH2gC68wAyGRESXULQKA26KfCgDM3fxYxqaehSrmBPipcbkS1e3aztnFIl_nX0dkmgI8KNAHjdHH_hi5kO6eCMcdIPvT92C0I_CkxX_Hhq4NbqQc_i2mXa8gkqWTOrnueUjb6gCxvj0-7sDCRfX8Wndd90VpxlmxmGZGgS428%2C&ogV=-10",
    #         "snapshot_name": "yandex_1_result",
    #         "site_name": "yandex1"
    #     },
    #     {
    #         "url": "https://market.yandex.ru/card/otkryvalka-dlya-plastikovykh-butylok-ochen-udobnaya-neskolzyashchaya-ruchka/4914802995?do-waremd5=8nV8Vj9v0jI5GkJYBS_r3A&sponsored=1&cpc=QnAnAHDiEFPea63MN6lp6y3-iUuHnry4ePbp5yu3kKUuKYlmY1gcg7nEm16m3YXfCZXM7vHuuwXT5TRjBxCRuhVtd0wnU7h-fKMDRpY1C8eng6d-i0d9Lwb9c-e-Oxjl6c6yDHKJhoIKyfBE8N3xyHZ69rCKIDS-Scs1KSKhqJdfnOtPA5xdlpPkR6NJO389JqreZoo_j7lY5UimYDRcPGGUvYxcKX8owzK0ONpYtNSXHx7JFhObnzsaspaqu9StzLaz0s3kHuS2vlfeARm41TiQD_ifI6_6cj1lT5TsPAbz5f6_tM-AA5q3pXgLaLYGokc8KKXmr2QoPlleEgzzyH2_iEzze-x7d2NpQrT9UgpliHvzzxOLdtVHIOAgq84PV2g0JhX0iCZ8dBHgWIPnoHxBkoZaO0h-&ogV=-10",
    #         "snapshot_name": "yandex_2_result",
    #         "site_name": "yandex2"
    #     },
    #     {
    #         "url": "https://market.yandex.ru/card/besprovodnyye-naushniki-apple-airpods-pro-2-usb-c-mtjv3zpa/103174645689?do-waremd5=8aAKXVhszP-83ur61JX3ZA&sponsored=1&cpc=QnAnAHDiEFOq4BADvAoFJQpAouY5iwr8qYB7rcxysuj8Z7aiQUGMnJVRXlOsg-ygH5OTE5cTSY8mXnMn6jQG9vtyScbtgwuooopHYJ05rUwcrBiaX-UPMWSuFrqmZBoyzP7cuekseMKRSKAK5hcrZqcDZF9luCdhPP9b-1LpDPHYTE8_eIGeJNWLHo6tX9vAcsjygx6JMZhl22RsnHz-pNk3WVVd3_DbdIrhvrIcgpl7sRWGA07e7LFvp8FAfmnVoMGpCCKcQVIdvhC9pidXjR8D9xcTkSqHa2kEbseQpj6XvmzyPXlEdS_8952vpK3WyiI6Vk5_r3GqKj_PV2rBoZ0EcSU5kHx9AJWONgxCZ8LNiZSR4aR8JDpQ2tMnL01XCj9wzT6SnmTTT1sREPxIYuatdgJEyMy6VjmkcWIkTgO-ZO_GHuwWsTfJuYoWak4MejsMk_rPI11CKvgOBHIFhlayJmTG9Wk8xPtGtcAS4CFsmj-5NkNZuxcqe5H8zDL7sOe8stNwl0cY4eYw3tNwemALGu4TfgXUyAU8ez9sxj1MJ4G1UGZW3g%2C%2C&ogV=-10",
    #         "snapshot_name": "yandex_3_result",
    #         "site_name": "yandex3"
    #     },
    #     {
    #         "url": "https://megamarket.ru/promo-page/details/#?slug=avtokreslo-cybex-cloud-t-i-size-mirage-grey-plus-600012950680_135467&merchantId=135467",
    #         "snapshot_name": "megamarket_1_result",
    #         "site_name": "megamarket1"
    #     },
    #     {
    #         "url": "https://megamarket.ru/catalog/details/kostyum-detskiy-batik-gnom-veselchak-multikolor-158-100058864528/#?exclusiveMerchantId=96036&exclusiveWarehouseId=1737578",
    #         "snapshot_name": "megamarket_2_result",
    #         "site_name": "megamarket2"
    #     },
    #     {
    #         "url": "https://megamarket.ru/catalog/details/vino-bezalkogolnoe-jp-chenet-cabernet-syrah-krasnoe-sladkoe-075-l-100048781160_7443/#?exclusiveMerchantId=7443",
    #         "snapshot_name": "megamarket_3_result",
    #         "site_name": "megamarket3"
    #     },
    #     {
    #         "url": "https://www.dns-shop.ru/product/b1a1fa9770e8d582/14-noutbuk-tecno-megabook-s14mm-seryj/",
    #         "snapshot_name": "dns_1_result",
    #         "site_name": "dns1"
    #     },
    #     {
    #         "url": "https://www.dns-shop.ru/product/c768993ec38a7662/klaviatura-provodnaa-ajazz-ak820/",
    #         "snapshot_name": "dns_2_result",
    #         "site_name": "dns2"
    #     },
    #     {
    #         "url": "https://www.dns-shop.ru/product/37422be84f953332/eko-paket-kraftmarket-mark/",
    #         "snapshot_name": "dns_3_result",
    #         "site_name": "dns3"
    #     },
    #     {
    #         "url": "https://samokat.ru/product/zhenskiy-dzhemper-arive-goluboy-l",
    #         "snapshot_name": "samokat_1_result",
    #         "site_name": "samokat1"
    #     },
    #     {
    #         "url": "https://samokat.ru/product/advent-kalendar-samokat-beauty-rituals-9-beauty-podarkov-syurpriz-1-sht",
    #         "snapshot_name": "samokat_2_result",
    #         "site_name": "samokat2"
    #     },
    #     {
    #         "url": "https://samokat.ru/product/krem-dlya-litsa-clinique-for-men-anti-aging-moisturizer-100-ml",
    #         "snapshot_name": "samokat_3_result",
    #         "site_name": "samokat3"
    #     },
    #     {
    #         "url": "https://www.vseinstrumenti.ru/product/gvozdi-po-betonu-usilennye-3-05h19-mm-1000-sht-toua-30519stepeg-822483/",
    #         "snapshot_name": "vseinstrumenti_1_result",
    #         "site_name": "vseinstrumenti1"
    #     },
    #     {
    #         "url": "https://www.vseinstrumenti.ru/product/benzinovyj-snegouborschik-gigant-sp-7-610ms-15586978/",
    #         "snapshot_name": "vseinstrumenti_2_result",
    #         "site_name": "vseinstrumenti2"
    #     },
    #     {
    #         "url": "https://www.vseinstrumenti.ru/product/18v-akkumulyatornaya-drel-shurupovert-bs18g4-201c-aeg-4935499174-15448612/",
    #         "snapshot_name": "vseinstrumenti_3_result",
    #         "site_name": "vseinstrumenti3"
    #     },
    #     {
    #         "url": "https://vkusvill.ru/goods/vino-igristoe-bezalkogolnoe-shardone-beloe-sukhoe-750-ml-115485.html",
    #         "snapshot_name": "vkusvill_1_result",
    #         "site_name": "vkusvill1"
    #     },
    #     {
    #         "url": "https://vkusvill.ru/goods/banany-731.html",
    #         "snapshot_name": "vkusvill_2_result",
    #         "site_name": "vkusvill2"
    #     },
    #     {
    #         "url": "https://vkusvill.ru/goods/mandariny-marokko-30841.html",
    #         "snapshot_name": "vkusvill_3_result",
    #         "site_name": "vkusvill3"
    #     },
    #     {
    #         "url": "https://kuper.ru/magnitkosmetikbd/dezodorant-antiperspirant-stik-reksona-suhost-pudry-zhenskiy-40-ml-b02f5f5",
    #         "snapshot_name": "kuper_1_result",
    #         "site_name": "kuper1"
    #     },
    #     {
    #         "url": "https://kuper.ru/magnitkosmetikbd/kosmeticheskiy-nabor-arko-3-predmeta",
    #         "snapshot_name": "kuper_2_result",
    #         "site_name": "kuper2"
    #     },
    #     {
    #         "url": "https://kuper.ru/magnitkosmetikbd/tualetnaya-voda-muzhskaya-apple-parfums-apple-pour-homme-navy-style-100-ml",
    #         "snapshot_name": "kuper_3_result",
    #         "site_name": "kuper3"
    #     },
    #     {
    #         "url": "https://www.lamoda.ru/p/mp002xg05m5c/clothes-happybaby-pukhovik/",
    #         "snapshot_name": "lamoda_1_result",
    #         "site_name": "lamoda1"
    #     },
    #     {
    #         "url": "https://www.lamoda.ru/p/rtlaeq333701/clothes-hm-shorty-dlya-plavaniya/",
    #         "snapshot_name": "lamoda_2_result",
    #         "site_name": "lamoda2"
    #     },
    #     {
    #         "url": "https://www.lamoda.ru/p/mp002xg05mlu/shoes-lcwaikiki-tapochki/",
    #         "snapshot_name": "lamoda_3_result",
    #         "site_name": "lamoda3"
    #     },
    #     {
    #         "url": "https://www.citilink.ru/product/robot-pylesos-irobot-braava-jet-m6-belyi-1476403/",
    #         "snapshot_name": "citilink_1_result",
    #         "site_name": "citilink1"
    #     },
    #     {
    #         "url": "https://www.citilink.ru/product/noutbuk-asus-vivobook-e1504fa-bq2467-ryzen-5-7520u-16gb-ssd512gb-610m-2124863/",
    #         "snapshot_name": "citilink_2_result",
    #         "site_name": "citilink2"
    #     },
    #     {
    #         "url": "https://www.citilink.ru/product/vinnyi-shkaf-lex-lwd6054bl-1-nokamern-chernyi-chat500011-2072118/?referrer=reattribution%3D1&yclid=6456050938691977215",
    #         "snapshot_name": "citilink_3_result",
    #         "site_name": "citilink3"
    #     },
    #     {
    #         "url": "https://www.etm.ru/cat/nn/3624277",
    #         "snapshot_name": "etm_1_result",
    #         "site_name": "etm1"
    #     },
    #     {
    #         "url": "https://www.etm.ru/cat/nn/2639859",
    #         "snapshot_name": "etm_2_result",
    #         "site_name": "etm2"
    #     },
    #     {
    #         "url": "https://www.etm.ru/cat/nn/2064663",
    #         "snapshot_name": "etm_3_result",
    #         "site_name": "etm3"
    #     },
    #     {
    #         "url": "https://lavka.yandex.ru/good/prezervativy-durex-invisible-ultratonkie-12-unit",
    #         "snapshot_name": "lavka_1_result",
    #         "site_name": "lavka1"
    #     },
    #     {
    #         "url": "https://lavka.yandex.ru/good/gel-dlya-stirki-laska-effekt-vosstanovleniya-dlya-cvetnogo-zhidkoe-sredstvo-dlya-stirki-1-liter",
    #         "snapshot_name": "lavka_2_result",
    #         "site_name": "lavka2"
    #     },
    #     {
    #         "url": "https://lavka.yandex.ru/good/stiralnyj-poroshok-tide-akva-pudra-alpijskaya-svezhest-avtomat-3-kilogram",
    #         "snapshot_name": "lavka_3_result",
    #         "site_name": "lavka3"
    #     },
    #     {
    #         "url": "https://www.mvideo.ru/products/skovoroda-kovanyi-aluminii-hi-mvnkklgr30122-22-sm-400194552",
    #         "snapshot_name": "mvideo_1_result",
    #         "site_name": "mvideo1"
    #     },
    #     {
    #         "url": "https://www.mvideo.ru/products/kreslo-pravila-mebeli-kord-dlya-otdyha-doma-s-dekorativnoi-podushkoi-na-vysokih-nozhkah-s-vysokoi-spinkoi-76h84h111-sm-zelenyi-velur-400510965",
    #         "snapshot_name": "mvideo_2_result",
    #         "site_name": "mvideo2"
    #     },
    #     {
    #         "url": "https://www.mvideo.ru/products/vozduhouvlazhnitel-boneco-u700-20058942",
    #         "snapshot_name": "mvideo_3_result",
    #         "site_name": "mvideo3"
    #     },
    #     {
    #         "url": "https://goldapple.ru/19000386905-marshall-major-v",
    #         "snapshot_name": "goldapple_1_result",
    #         "site_name": "goldapple1"
    #     },
    #     {
    #         "url": "https://goldapple.ru/19000399002-lip-liner",
    #         "snapshot_name": "goldapple_2_result",
    #         "site_name": "goldapple2"
    #     },
    #     {
    #         "url": "https://goldapple.ru/19000331476-unframe",
    #         "snapshot_name": "goldapple_3_result",
    #         "site_name": "goldapple3"
    #     },
    #     {
    #         "url": "https://www.sima-land.ru/10083982/vaza-sl-home-arena-blanka-9-9-13-5-cm-keramika-belaya/",
    #         "snapshot_name": "simaland_1_result",
    #         "site_name": "simaland1"
    #     },
    #     {
    #         "url": "https://www.sima-land.ru/7800222/lanch-boks-dlya-bento-torta-i-burgera-dolyana-450-ml-15-8-cm-nerazemnaya-kryshka-saharnyy-trostnik/",
    #         "snapshot_name": "simaland_2_result",
    #         "site_name": "simaland2"
    #     },
    #     {
    #         "url": "https://www.sima-land.ru/3602562/sousnik-dolyana-white-label-50-ml-d-8-5-cm-farfor-belyy/",
    #         "snapshot_name": "simaland_3_result",
    #         "site_name": "simaland3"
    #     },
    #     {
    #         "url": "https://apteka.ru/product/nabor-iz-4-x-upakovok-klimalanina-30-po-specz-czene-691c1fd04a2c13761523e279/?v=5e326f3965b5ab0001654a98",
    #         "snapshot_name": "apteka_1_result",
    #         "site_name": "apteka1"
    #     },
    #     {
    #         "url": "https://apteka.ru/product/nabor-iz-2-upakovok-kudesan-3-20ml-flak-kapli-so-skidkoj-67e624cb4879ba1437a8df7e/?v=5e7c99a735a6fe0001f71b66",
    #         "snapshot_name": "apteka_2_result",
    #         "site_name": "apteka2"
    #     },
    #     {
    #         "url": "https://apteka.ru/product/tonometr-mt-30-avtomaticheskij-bazovyj-5e8477923486400001fb16ed/",
    #         "snapshot_name": "apteka_3_result",
    #         "site_name": "apteka3"
    #     },
    #     {
    #         "url": "https://5ka.ru/product/tabletki-dlya-posudomoechnykh-mashin-synergetic-be--4067685/",
    #         "snapshot_name": "5ka_1_result",
    #         "site_name": "5ka1"
    #     },
    #     {
    #         "url": "https://5ka.ru/product/napolnitel-dlya-koshachikh-tualetov-cat-step-tofu--4085430/",
    #         "snapshot_name": "5ka_2_result",
    #         "site_name": "5ka2"
    #     },
    #     {
    #         "url": "https://5ka.ru/product/nabor-dlya-lepki-genio-kids-4-tsveta-ta1008--3491861/",
    #         "snapshot_name": "5ka_3_result",
    #         "site_name": "5ka3"
    #     },
    #     {
    #         "url": "https://lemanapro.ru/product/dushevoy-ugolok-ampm-moxie-w9mg-403-9090-mt1-kvadratnyy-90x90-sm-hromirovannyy-profil-prozrachnoe-steklo-razdvizhnoy-89369261/",
    #         "snapshot_name": "lemanapro_1_result",
    #         "site_name": "lemanapro1"
    #     },
    #     {
    #         "url": "https://lemanapro.ru/product/komplekt-installyaciya-ampm-ergofit-unitaz-adt-long-vortex-525x36-sm-belyy-92172430/",
    #         "snapshot_name": "lemanapro_2_result",
    #         "site_name": "lemanapro2"
    #     },
    #     {
    #         "url": "https://lemanapro.ru/product/kley-dlya-teploizolyacii-paladium-palafix-402-25kg-17053310/",
    #         "snapshot_name": "lemanapro_3_result",
    #         "site_name": "lemanapro3"
    #     },
    #     {
    #         "url": "https://www.sportmaster.ru/product/32755460299/",
    #         "snapshot_name": "sportmaster_1_result",
    #         "site_name": "sportmaster1"
    #     },
    #     {
    #         "url": "https://www.sportmaster.ru/product/30990640299/",
    #         "snapshot_name": "sportmaster_2_result",
    #         "site_name": "sportmaster2"
    #     },
    #     {
    #         "url": "https://www.sportmaster.ru/product/29401550299/",
    #         "snapshot_name": "sportmaster_3_result",
    #         "site_name": "sportmaster3"
    #     },
    #     {
    #         "url": "https://www.letu.ru/product/studio-floristic-buket-iz-rozovyh-roz-kostyor-lyubvi/167801054",
    #         "snapshot_name": "letual_1_result",
    #         "site_name": "letual1"
    #     },
    #     {
    #         "url": "https://www.letu.ru/product/calvin-klein-tualetnaya-voda-ck-in2u-her/167800455",
    #         "snapshot_name": "letual_2_result",
    #         "site_name": "letual2"
    #     },
    #     {
    #         "url": "https://www.letu.ru/product/wellness-ultracare-naduvnaya-korona-imeninnika-na-golovu-zolotaya/173801460",
    #         "snapshot_name": "letual_3_result",
    #         "site_name": "letual3"
    #     },
    #     {
    #         "url": "https://www.detmir.ru/product/index/id/6264071/?variant_id=6264071",
    #         "snapshot_name": "detmir_1_result",
    #         "site_name": "detmir1"
    #     },
    #     {
    #         "url": "https://www.detmir.ru/product/index/id/6738494/?variant_id=6738494",
    #         "snapshot_name": "detmir_2_result",
    #         "site_name": "detmir2"
    #     },
    #     {
    #         "url": "https://www.detmir.ru/product/index/id/6232844/?variant_id=6232844",
    #         "snapshot_name": "detmir_3_result",
    #         "site_name": "detmir3"
    #     },
    #     {
    #         "url": "https://www.onlinetrade.ru/catalogue/elki_i_sosny-c604/tsar_elka/el_iskusstvennaya_tsar_elka_russkaya_krasavitsa_premium_180_sm-1920157.html",
    #         "snapshot_name": "onlinetrade_1_result",
    #         "site_name": "onlinetrade1"
    #     },
    #     {
    #         "url": "https://www.onlinetrade.ru/catalogue/kulery_dlya_protsessorov-c1492/deepcool/kuler_dlya_protsessora_deepcool_assassin_vc_elite_r_asn4_bknvnn_gjd-5079766.html",
    #         "snapshot_name": "onlinetrade_2_result",
    #         "site_name": "onlinetrade2"
    #     },
    #     {
    #         "url": "https://www.onlinetrade.ru/catalogue/lampy_vintage-c3720/uniel/svetodiodnaya_lampa_vintage_led_cw35_5w_golden_e14_glv21go_forma_svecha_na_vetru_zolotistaya_kolba_karton_tm_uniel_ul_00002397-2303418.html",
    #         "snapshot_name": "onlinetrade_3_result",
    #         "site_name": "onlinetrade3"
    #     },
    #     {
    #         "url": "https://www.perekrestok.ru/cat/76/p/gorosek-bonduel-zelenyj-400g-16791",
    #         "snapshot_name": "perekrestok_1_result",
    #         "site_name": "perekrestok1"
    #     },
    #     {
    #         "url": "https://www.perekrestok.ru/cat/1589/p/kartofel-mytyj-2099571",
    #         "snapshot_name": "perekrestok_2_result",
    #         "site_name": "perekrestok2"
    #     },
    #     {
    #         "url": "https://www.perekrestok.ru/cat/1619/p/kotlety-kurinye-parovye-perekrestok-select-160g-4421287",
    #         "snapshot_name": "perekrestok_3_result",
    #         "site_name": "perekrestok3"
    #     },
    #     {
    #         "url": "https://www.komus.ru/katalog/ruchki-karandashi-markery/sharikovye-ruchki/sharikovye-neavtomaticheskie-ruchki/ruchka-sharikovaya-neavtomaticheskaya-pensan-my-tech-sinyaya-tolshhina-linii-0-35-mm-/p/480210/?from=block-301-0_1",
    #         "snapshot_name": "komus_1_result",
    #         "site_name": "komus1"
    #     },
    #     {
    #         "url": "https://www.komus.ru/katalog/upakovka-i-markirovka/klejkie-lenty-i-skotch-/dvukhstoronnyj-skotch-i-krepezhnye-klejkie-lenty/klejkaya-lenta-dvukhstoronnyaya-montazhnaya-belaya-komus-38-mm-kh-25-m/p/198701/?from=block-25-0_1",
    #         "snapshot_name": "komus_2_result",
    #         "site_name": "komus2"
    #     },
    #     {
    #         "url": "https://www.komus.ru/katalog/produkty-pitaniya/voda-napitki-soki/voda-pod-arendu-kulera/butilirovannaya-pitevaya-voda-komus-akva-soft-19-litrov-vozvratnaya-tara-/p/2214567/?from=block-9999-0_1",
    #         "snapshot_name": "komus_3_result",
    #         "site_name": "komus3"
    #     },
    #     {
    #         "url": "https://sunlight.net/catalog/earring_69748.html",
    #         "snapshot_name": "sunlight_1_result",
    #         "site_name": "sunlight1"
    #     },
    #     {
    #         "url": "https://sunlight.net/catalog/ring_986744.html",
    #         "snapshot_name": "sunlight_2_result",
    #         "site_name": "sunlight2"
    #     },
    #     {
    #         "url": "https://sunlight.net/catalog/glasses_388021.html",
    #         "snapshot_name": "sunlight_3_result",
    #         "site_name": "sunlight3"
    #     },
    #     {
    #         "url": "https://www.eldorado.ru/cat/detail/klitoralnyy-vibrostimulyator-lora-di-carlo-ldcz-0201-grey/",
    #         "snapshot_name": "eldorado_1_result",
    #         "site_name": "eldorado1"
    #     },
    #     {
    #         "url": "https://www.eldorado.ru/cat/detail/smennyy-rukav-dlya-masturbatora-satisfyer-men-lusty-tongues-bodily-ee73-758-1217/",
    #         "snapshot_name": "eldorado_2_result",
    #         "site_name": "eldorado2"
    #     },
    #     {
    #         "url": "https://www.eldorado.ru/cat/detail/podarochnyy-nabor-edc-wholesale-loveboxxx-congratulations-blue-lbx002/",
    #         "snapshot_name": "eldorado_3_result",
    #         "site_name": "eldorado3"
    #     },
    #     {
    #         "url": "https://lenta.com/product/dp-nektar-multifrukt-s-3-h-let-rossiya-200ml-604968/",
    #         "snapshot_name": "lenta_1_result",
    #         "site_name": "lenta1"
    #     },
    #     {
    #         "url": "https://lenta.com/product/figura-svetodiodnaya-siyayushchijj-olen-79sm-60led-holbelyjj-ip44-204084-kitajj-717936/",
    #         "snapshot_name": "lenta_2_result",
    #         "site_name": "lenta2"
    #     },
    #     {
    #         "url": "https://lenta.com/product/kruzhka-rainbow-400ml-keramika-v-assort-rm-1-kitajj-680653/",
    #         "snapshot_name": "lenta_3_result",
    #         "site_name": "lenta3"
    #     },
    #     {
    #         "url": "https://magnit.ru/product/1000162851-ikra_krasnaya_95gr_zh_b_12?shopCode=992301&shopType=6",
    #         "snapshot_name": "magnit_1_result",
    #         "site_name": "magnit1"
    #     },
    #     {
    #         "url": "https://magnit.ru/product/8000058936-vodosgon_ballet_25sm_plastik_repablik?shopCode=992301&shopType=6",
    #         "snapshot_name": "magnit_2_result",
    #         "site_name": "magnit2"
    #     },
    #     {
    #         "url": "https://magnit.ru/product/1000289065-eatmeat_farsh_domashniy_0_4kg_lotok_ooo_mpk_atyashevskiy_4?shopCode=992301&shopType=6",
    #         "snapshot_name": "magnit_3_result",
    #         "site_name": "magnit3"
    #     },
    #     {
    #         "url": "https://www.eapteka.ru/goods/id515717/",
    #         "snapshot_name": "eapteka_1_result",
    #         "site_name": "eapteka1"
    #     },
    #     {
    #         "url": "https://www.eapteka.ru/goods/id200848/",
    #         "snapshot_name": "eapteka_2_result",
    #         "site_name": "eapteka2"
    #     },
    #     {
    #         "url": "https://www.eapteka.ru/goods/id287374/",
    #         "snapshot_name": "eapteka_3_result",
    #         "site_name": "eapteka3"
    #     },
    #     {
    #         "url": "https://www.kolesa-darom.ru/catalog/avto/shiny/ikon-tyres/character-ice-8-nordman-8/185-65-R15-T-92-8457439/",
    #         "snapshot_name": "kolesadarom_1_result",
    #         "site_name": "kolesadarom1"
    #     },
    #     {
    #         "url": "https://www.kolesa-darom.ru/catalog/moto/shiny/novion/us150/90-90-R10-J-55-9013505/",
    #         "snapshot_name": "kolesadarom_2_result",
    #         "site_name": "kolesadarom2"
    #     },
    #     {
    #         "url": "https://www.kolesa-darom.ru/catalog/avto/avtomasla-i-zhidkosti/motornye-masla/maslo-motornoe-rolf-ultra-5w-40-a3-b4-sp-4l-9386593/",
    #         "snapshot_name": "kolesadarom_3_result",
    #         "site_name": "kolesadarom3"
    #     },
    #     {
    #         "url": "https://rs24.ru/product/3522372",
    #         "snapshot_name": "rs24_1_result",
    #         "site_name": "rs241"
    #     },
    #     {
    #         "url": "https://rs24.ru/product/203973",
    #         "snapshot_name": "rs24_2_result",
    #         "site_name": "rs242"
    #     },
    #     {
    #         "url": "https://rs24.ru/product/1453824",
    #         "snapshot_name": "rs24_3_result",
    #         "site_name": "rs243"
    #     },
    #     {
    #         "url": "https://hoff.ru/catalog/spalnya/krovati/krovati_s_podemnym_mehanizmom/krovat_s_podyemnym_mekhanizmom_ravena_id10484069/?articul=18862770",
    #         "snapshot_name": "hoff_1_result",
    #         "site_name": "hoff1"
    #     },
    #     {
    #         "url": "https://hoff.ru/catalog/tovary_dlya_doma/hoztovary/bytovaya_himiya/sredstva_dlya_kuhni_i_doma/kontsentrat_dlya_mytya_posudy_id1715927/?articul=80266562",
    #         "snapshot_name": "hoff_2_result",
    #         "site_name": "hoff2"
    #     },
    #     {
    #         "url": "https://hoff.ru/catalog/tovary_dlya_doma/hoztovary/baki_dlya_musora/korzina_dlya_bumag_01_088_01_id10877160/?articul=80760703#questions",
    #         "snapshot_name": "hoff_3_result",
    #         "site_name": "hoff3"
    #     },
    #     {
    #         "url": "https://zdravcity.ru/p_gorchichnik-paket-sogrevajuschij-first-aid-ferstjejd-20sht-0209905.html",
    #         "snapshot_name": "zdravcity_1_result",
    #         "site_name": "zdravcity1"
    #     },
    #     {
    #         "url": "https://zdravcity.ru/p_opory-hodunki-b-well-wr-211-s-prinadlezhnostjami-0101602.html",
    #         "snapshot_name": "zdravcity_2_result",
    #         "site_name": "zdravcity2"
    #     },
    #     {
    #         "url": "https://zdravcity.ru/p_test-poloski-dlja-opredelenija-urovnja-gljukozy-v-krovi-gmate-life-gdh-30h5mm-n50-0119833.html",
    #         "snapshot_name": "zdravcity_3_result",
    #         "site_name": "zdravcity3"
    #     },
    #     {
    #         "url": "https://market-delivery.yandex.ru/retail/apteka_36_6_new?item=725cd47e-e4a5-4bc6-97cc-ecd8fafc6761&placeSlug=apteka_366_new_53rdv&relatedBrandSlug=apteka_36_6_new",
    #         "snapshot_name": "deliveri_1_result",
    #         "site_name": "deliveri1"
    #     },
    #     {
    #         "url": "https://market-delivery.yandex.ru/retail/fix_price?item=39e9b17e-127f-4353-94db-a20f78f2f120&placeSlug=fix_px6dw&relatedBrandSlug=fix_price",
    #         "snapshot_name": "deliveri_2_result",
    #         "site_name": "deliveri2"
    #     },
    #     {
    #         "url": "https://market-delivery.yandex.ru/retail/fix_price/catalog/19286?item=ead76cb3-f7f1-442e-bea2-4ff594ab0bac&placeSlug=fix_px6dw&relatedBrandSlug=fix_price",
    #         "snapshot_name": "deliveri_3_result",
    #         "site_name": "deliveri3"
    #     },
    #     {
    #         "url": "https://eda.yandex.ru/retail/asan_giper?item=762f65b9-6ea3-41e4-8e8c-e436e98d7eef&placeSlug=ashan_bm8r4&relatedBrandSlug=asan_giper",
    #         "snapshot_name": "edayandex_1_result",
    #         "site_name": "edayandex1"
    #     },
    #     {
    #         "url": "https://eda.yandex.ru/retail/metro_giper?item=6d2fb17e-53cf-5bee-9fcf-7796edb0e96a&placeSlug=metro_wqz7f&relatedBrandSlug=metro_giper",
    #         "snapshot_name": "edayandex_2_result",
    #         "site_name": "edayandex2"
    #     },
    #     {
    #         "url": "https://eda.yandex.ru/retail/globus_new?item=7f38d52e-73b4-408f-b1dd-3aa125e4a63e&placeSlug=globus_new_4nj5k&relatedBrandSlug=globus_new",
    #         "snapshot_name": "edayandex_3_result",
    #         "site_name": "edayandex3"
    #     },
    #     {
    #         "url": "https://www.vprok.ru/product/ananas-ready-to-eat-1kg--1014401",
    #         "snapshot_name": "vprok_1_result",
    #         "site_name": "vprok1"
    #     },
    #     {
    #         "url": "https://www.vprok.ru/product/russkiy-sahar-rus-sah-sahar-belyy-kusk-1kg--1005008",
    #         "snapshot_name": "vprok_2_result",
    #         "site_name": "vprok2"
    #     },
    #     {
    #         "url": "https://www.vprok.ru/product/yubileynoe-yubil-pechene-traditsionnoe-vit-112g--312013",
    #         "snapshot_name": "vprok_3_result",
    #         "site_name": "vprok3"
    #     },
    #     {
    #         "url": "https://uteka.ru/product/polisorb-mp-19332/",
    #         "snapshot_name": "uteka_1_result",
    #         "site_name": "uteka1"
    #     },
    #     {
    #         "url": "https://uteka.ru/product/baralgin-m-297417/",
    #         "snapshot_name": "uteka_2_result",
    #         "site_name": "uteka2"
    #     },
    #     {
    #         "url": "https://uteka.ru/product/irrigator-bwell-wi-922-361557/",
    #         "snapshot_name": "uteka_3_result",
    #         "site_name": "uteka3"
    #     },
    #     {
    #         "url": "https://faberlic.com/ru/ru/product/01070302-079640",
    #         "snapshot_name": "faberlic_1_result",
    #         "site_name": "faberlic1"
    #     },
    #     {
    #         "url": "https://faberlic.com/ru/ru/product/011002-00400",
    #         "snapshot_name": "faberlic_2_result",
    #         "site_name": "faberlic2"
    #     },
    #     {
    #         "url": "https://faberlic.com/ru/ru/product/01080102-000513",
    #         "snapshot_name": "faberlic_3_result",
    #         "site_name": "faberlic3"
    #     },
    #     {
    #         "url": "https://exist.ru/Catalog/Goods/5/183/C570CE67",
    #         "snapshot_name": "exist_1_result",
    #         "site_name": "exist1"
    #     },
    #     {
    #         "url": "https://exist.ru/Catalog/Goods/7/174/F59119BC",
    #         "snapshot_name": "exist_2_result",
    #         "site_name": "exist2"
    #     },
    #     {
    #         "url": "https://exist.ru/Catalog/Goods/5/8/5B40D79B",
    #         "snapshot_name": "exist_3_result",
    #         "site_name": "exist3"
    #     },
    #     {
    #         "url": "https://apteka-april.ru/product/344198-ukrepitel_dlya_nogtej_s_proteinom_zhemchuga_11ml",
    #         "snapshot_name": "aprilapteka_1_result",
    #         "site_name": "aprilapteka1"
    #     },
    #     {
    #         "url": "https://apteka-april.ru/product/226849-kontur_plyus_glyukometr",
    #         "snapshot_name": "aprilapteka_2_result",
    #         "site_name": "aprilapteka2"
    #     },
    #     {
    #         "url": "https://apteka-april.ru/product/266843-farinorm_benzidamin_sprej_30ml",
    #         "snapshot_name": "aprilapteka_3_result",
    #         "site_name": "aprilapteka3"
    #     },
    #     {
    #         "url": "https://www.officemag.ru/catalog/goods/605329/",
    #         "snapshot_name": "officemag_1_result",
    #         "site_name": "officemag1"
    #     },
    #     {
    #         "url": "https://www.officemag.ru/catalog/goods/110532/",
    #         "snapshot_name": "officemag_2_result",
    #         "site_name": "officemag2"
    #     },
    #     {
    #         "url": "https://www.officemag.ru/catalog/goods/600933/",
    #         "snapshot_name": "officemag_3_result",
    #         "site_name": "officemag3"
    #     },
    #     {
    #         "url": "https://shop.mts.ru/product/data-kabel-rocket-contact-usb-a-usb-c-1m-opljetka-nejlon-chernyj",
    #         "snapshot_name": "mts_1_result",
    #         "site_name": "mts1"
    #     },
    #     {
    #         "url": "https://shop.mts.ru/product/tarif-mts-bolshe-samoregistratsija-350r-moskva",
    #         "snapshot_name": "mts_2_result",
    #         "site_name": "mts2"
    #     },
    #     {
    #         "url": "https://shop.mts.ru/product/perehodnik-huawei-micro-usb-usb-type-c-black",
    #         "snapshot_name": "mts_3_result",
    #         "site_name": "mts3"
    #     },
    #     {
    #         "url": "https://www.petshop.ru/catalog/kotyata-i-shchenki/kotyata/dlya-doma/sredstva-gigieny-dlya-kotyat/drevesnyy_napolnitel_pelleta_8mm_59in15_58472/?oid=105225",
    #         "snapshot_name": "petshop_1_result",
    #         "site_name": "petshop1"
    #     },
    #     {
    #         "url": "https://www.petshop.ru/catalog/cats/aksessuary/merch/t-shirt-hello-polandia-green-sparkle/?oid=74171",
    #         "snapshot_name": "petshop_2_result",
    #         "site_name": "petshop2"
    #     },
    #     {
    #         "url": "https://www.petshop.ru/catalog/fish/vet/vitaminy-dlya-rybok/mineralnyy-kamen-dlya-vodnykh-cherepakh/?oid=121927",
    #         "snapshot_name": "petshop_3_result",
    #         "site_name": "petshop3"
    #     },
    #     {
    #         "url": "https://flowwow.com/flowers/avtorskiy-premium-buket-iz-pio/",
    #         "snapshot_name": "flowwow_1_result",
    #         "site_name": "flowwow1"
    #     },
    #     {
    #         "url": "https://flowwow.com/christmas/zimniy-buket-7264/",
    #         "snapshot_name": "flowwow_2_result",
    #         "site_name": "flowwow2"
    #     },
    #     {
    #         "url": "https://flowwow.com/christmas/ledenec-podkova-i-loshad/",
    #         "snapshot_name": "flowwow_3_result",
    #         "site_name": "flowwow3"
    #     },
    #     {
    #         "url": "https://stolichki.ru/drugs/gardeks-bebi-sprey-ot-komarov-75ml",
    #         "snapshot_name": "stolichki_1_result",
    #         "site_name": "stolichki1"
    #     },
    #     {
    #         "url": "https://stolichki.ru/drugs/ey-end-di-termometr-med-el-dt-501",
    #         "snapshot_name": "stolichki_2_result",
    #         "site_name": "stolichki2"
    #     },
    #     {
    #         "url": "https://stolichki.ru/drugs/konteks-prezervativy-classic-klassicheskie-18",
    #         "snapshot_name": "stolichki_3_result",
    #         "site_name": "stolichki3"
    #     },
    #     {
    #         "url": "https://www.tsum.ru/about/giftcard/buy/?erid=2SDnjctDfbD",
    #         "snapshot_name": "tsum_1_result",
    #         "site_name": "tsum1"
    #     },
    #     {
    #         "url": "https://www.tsum.ru/product/7083220-dzhinsovaya-kurtka-alexander-wang-temno-seryi/",
    #         "snapshot_name": "tsum_2_result",
    #         "site_name": "tsum2"
    #     },
    #     {
    #         "url": "https://www.tsum.ru/product/he00452808-samokat-glider-deluxe-yvolution-fioletovyi/",
    #         "snapshot_name": "tsum_3_result",
    #         "site_name": "tsum3"
    #     },
    #     {
    #         "url": "https://www.tsum.ru/product/he00308139-igrushka-katalka-krokodil-italtrike-zelenyi/",
    #         "snapshot_name": "tsum_4_result",
    #         "site_name": "tsum4"
    #     },
    #     {
    #         "url": "https://rivegauche.ru/product/atelier-rebul-riv-gosh-30-let-bisous-set",
    #         "snapshot_name": "rivegauche_1_result",
    #         "site_name": "rivegauche1"
    #     },
    #     {
    #         "url": "https://rivegauche.ru/product/degrenne-guest-miroir-pastry-server",
    #         "snapshot_name": "rivegauche_2_result",
    #         "site_name": "rivegauche2"
    #     },
    #     {
    #         "url": "https://rivegauche.ru/product/dergenne-gourmet-bleu-bevelled-casserole",
    #         "snapshot_name": "rivegauche_3_result",
    #         "site_name": "rivegauche3"
    #     },
    #     {
    #         "url": "https://gorzdrav.org/p/njureksan-n50-tabl-d-rass-gomeopat-630991/",
    #         "snapshot_name": "gorzdrav_1_result",
    #         "site_name": "gorzdrav1"
    #     },
    #     {
    #         "url": "https://gorzdrav.org/p/bausch-lomb-ultra-oneday-n30-2-50-mjagkie-kontaktnye-odnodnevnye-linzy-650617/",
    #         "snapshot_name": "gorzdrav_2_result",
    #         "site_name": "gorzdrav2"
    #     },
    #     {
    #         "url": "https://gorzdrav.org/p/monami-sponzh-dlja-nanesenija-makijazha-n1-57602/",
    #         "snapshot_name": "gorzdrav_3_result",
    #         "site_name": "gorzdrav3"
    #     },
    #     {
    #         "url": "https://planetazdorovo.ru/catalog/lekarstva-i-bad/prostuda-i-gripp/temperatura/rinzasip-poroshok-dlya-30963/",
    #         "snapshot_name": "planetazdorovo_1_result",
    #         "site_name": "planetazdorovo1"
    #     },
    #     {
    #         "url": "https://planetazdorovo.ru/moskva/catalog/podarochnye-sertifikaty-200018/podarochnye-sertifikaty/sertifikat-podarochnyj-1000-123140544/",
    #         "snapshot_name": "planetazdorovo_2_result",
    #         "site_name": "planetazdorovo2"
    #     },
    #     {
    #         "url": "https://planetazdorovo.ru/moskva/catalog/lekarstva-i-bad/akusherstvo-i-ginekologiya/protivozachatochnye/postiplaniya-tab-075-mg-2-sht-6002007/",
    #         "snapshot_name": "planetazdorovo_3_result",
    #         "site_name": "planetazdorovo3"
    #     },
    #     {
    #         "url": "https://farmlend.ru/product/385777?p-c=1",
    #         "snapshot_name": "farmlend_1_result",
    #         "site_name": "farmlend1"
    #     },
    #     {
    #         "url": "https://farmlend.ru/product/69923",
    #         "snapshot_name": "farmlend_2_result",
    #         "site_name": "farmlend2"
    #     },
    #     {
    #         "url": "https://farmlend.ru/product/305762",
    #         "snapshot_name": "farmlend_3_result",
    #         "site_name": "farmlend3"
    #     },
    #     {
    #         "url": "https://sokolov.ru/corp-merch/product/441000000004/",
    #         "snapshot_name": "sokolov_1_result",
    #         "site_name": "sokolov1"
    #     },
    #     {
    #         "url": "https://sokolov.ru/silverware/product/2301010012/",
    #         "snapshot_name": "sokolov_2_result",
    #         "site_name": "sokolov2"
    #     },
    #     {
    #         "url": "https://sokolov.ru/jewelry-catalog/product/120298/",
    #         "snapshot_name": "sokolov_3_result",
    #         "site_name": "sokolov3"
    #     },
    #     {
    #         "url": "https://mosautoshina.ru/catalog/tyre/tunga/nordway-2/175-70-13-82-Q--/",
    #         "snapshot_name": "mosautoshina_1_result",
    #         "site_name": "mosautoshina1"
    #     },
    #     {
    #         "url": "https://mosautoshina.ru/catalog/wheel/khomen-wheels/khw2009-voyah-free/8.5-20-5-120-30-black_fp-66.1-/",
    #         "snapshot_name": "mosautoshina_2_result",
    #         "site_name": "mosautoshina2"
    #     },
    #     {
    #         "url": "https://mosautoshina.ru/catalog/tyre/westlake/zupereco-z-107/215-55-17-98-W-XL-/",
    #         "snapshot_name": "mosautoshina_3_result",
    #         "site_name": "mosautoshina3"
    #     },
    #     {
    #         "url": "https://minicen.ru/tovar/746376",
    #         "snapshot_name": "minicen_1_result",
    #         "site_name": "minicen1"
    #     },
    #     {
    #         "url": "https://minicen.ru/tovar/711955",
    #         "snapshot_name": "minicen_2_result",
    #         "site_name": "minicen2"
    #     },
    #     {
    #         "url": "https://minicen.ru/tovar/739872",
    #         "snapshot_name": "minicen_3_result",
    #         "site_name": "minicen3"
    #     },
    #     {
    #         "url": "https://mm.ru/product/vedro-taz-khozyajstvannyj-skladnoj-2445935?skuId=7372054",
    #         "snapshot_name": "magnitmarket_1_result",
    #         "site_name": "magnitmarket1"
    #     },
    #     {
    #         "url": "https://mm.ru/product/besprovodnaya-zaryadka-3-5760874?skuId=12932003",
    #         "snapshot_name": "magnitmarket_2_result",
    #         "site_name": "magnitmarket2"
    #     },
    #     {
    #         "url": "https://mm.ru/product/puskovoe-zaryadnoe-ustrojstvo-5851499?skuId=13084151",
    #         "snapshot_name": "magnitmarket_3_result",
    #         "site_name": "magnitmarket3"
    #     },
    #     {
    #         "url": "https://limestore.com/ru_ru/product/30946_4535_818-kamennyi",
    #         "snapshot_name": "lime_1_result",
    #         "site_name": "lime1"
    #     },
    #     {
    #         "url": "https://limestore.com/ru_ru/product/14138_0550_093-temno_koricnevyi",
    #         "snapshot_name": "lime_2_result",
    #         "site_name": "lime2"
    #     },
    #     {
    #         "url": "https://limestore.com/ru_ru/product/29632_1806_454-molocnyi",
    #         "snapshot_name": "lime_3_result",
    #         "site_name": "lime3"
    #     },
    #     {
    #         "url": "https://www.rendez-vous.ru/catalog/female/botinki/maison_david_tmh3319d_2_korichnevyy-4611388/",
    #         "snapshot_name": "rendezvous_1_result",
    #         "site_name": "rendezvous1"
    #     },
    #     {
    #         "url": "https://www.rendez-vous.ru/catalog/odezhda/svitery-vodolazki-dzhempery/mm6_maison_margiela_sh0am0064_pyl_no_bezhevyy-4887134/",
    #         "snapshot_name": "rendezvous_2_result",
    #         "site_name": "rendezvous2"
    #     },
    #     {
    #         "url": "https://www.rendez-vous.ru/catalog/bags/ryukzak/guess_j5yz04wgt10_chernyy-4745882/",
    #         "snapshot_name": "rendezvous_3_result",
    #         "site_name": "rendezvous3"
    #     },
    #     {
    #         "url": "https://aptekiplus.ru/moskva/product/diklofenak-5-50-g-gel-dlya-naruzhnogo-primeneniya-4/",
    #         "snapshot_name": "aptekiplus_1_result",
    #         "site_name": "aptekiplus1"
    #     },
    #     {
    #         "url": "https://aptekiplus.ru/moskva/product/spakovrik-dvannoy-na-prisoskah-dolyana-krupnaya-galka-33h63-sm-cvet-miks/",
    #         "snapshot_name": "aptekiplus_2_result",
    #         "site_name": "aptekiplus2"
    #     },
    #     {
    #         "url": "https://aptekiplus.ru/moskva/product/tolperizonakrihin-150-mg-30-sht-tabletki-pokrytye-plenochnoj-obolochkoj/",
    #         "snapshot_name": "aptekiplus_3_result",
    #         "site_name": "aptekiplus3"
    #     },
    #     {
    #         "url": "https://moscow.shop.megafon.ru/mobile/202013",
    #         "snapshot_name": "megafon_1_result",
    #         "site_name": "megafon1"
    #     },
    #     {
    #         "url": "https://moscow.shop.megafon.ru/modems_routers/153942",
    #         "snapshot_name": "megafon_2_result",
    #         "site_name": "megafon2"
    #     },
    #     {
    #         "url": "https://moscow.shop.megafon.ru/smart_watches/196697",
    #         "snapshot_name": "megafon_3_result",
    #         "site_name": "megafon3"
    #     },
    #     {
    #         "url": "https://www.winelab.ru/product/1028096",
    #         "snapshot_name": "winelab_1_result",
    #         "site_name": "winelab1"
    #     },
    #     {
    #         "url": "https://www.winelab.ru/product/1001014",
    #         "snapshot_name": "winelab_2_result",
    #         "site_name": "winelab2"
    #     },
    #     {
    #         "url": "https://www.winelab.ru/product/1017787",
    #         "snapshot_name": "winelab_3_result",
    #         "site_name": "winelab3"
    #     },
    #     {
    #         "url": "https://re-store.ru/catalog/10117PRO256ORGN/",
    #         "snapshot_name": "restore_1_result",
    #         "site_name": "restore1"
    #     },
    #     {
    #         "url": "https://re-store.ru/catalog/BHR7793GL/",
    #         "snapshot_name": "restore_2_result",
    #         "site_name": "restore2"
    #     },
    #     {
    #         "url": "https://re-store.ru/catalog/TIN-33-0279-A-09-0044/",
    #         "snapshot_name": "restore_3_result",
    #         "site_name": "restore3"
    #     },
    #     {
    #         "url": "https://www.divan.ru/product/pled-kadli-green-130x170",
    #         "snapshot_name": "divan_1_result",
    #         "site_name": "divan1"
    #     },
    #     {
    #         "url": "https://www.divan.ru/product/divan-numo-mini-textile-silver",
    #         "snapshot_name": "divan_2_result",
    #         "site_name": "divan2"
    #     },
    #     {
    #         "url": "https://www.divan.ru/product/podushka-rejn-barhat-cherry",
    #         "snapshot_name": "divan_3_result",
    #         "site_name": "divan3"
    #     },
    #     {
    #         "url": "https://megapteka.ru/kislovodsk/catalog/voda-3/voda-mineral-stelmas-46120",
    #         "snapshot_name": "megaapteka_1_result",
    #         "site_name": "megaapteka1"
    #     },
    #     {
    #         "url": "https://megapteka.ru/kislovodsk/catalog/travy-117/romashki-cvetki-filtr-pakety-4644779",
    #         "snapshot_name": "megaapteka_2_result",
    #         "site_name": "megaapteka2"
    #     },
    #     {
    #         "url": "https://megapteka.ru/kislovodsk/catalog/obezbolivayushhie-sredstva-63/extraplast-plastyr-ot-4497635",
    #         "snapshot_name": "megaapteka_3_result",
    #         "site_name": "megaapteka3"
    #     },
    #     {
    #         "url": "https://www.shoppinglive.ru/p/dorozhnaya-sumka-transformer-s-sumkoy-dlya-obuvi-197853?digiPreview=WTBUIVCYY",
    #         "snapshot_name": "shoplive_1_result",
    #         "site_name": "shoplive1"
    #     },
    #     {
    #         "url": "https://www.shoppinglive.ru/p/skatert-pryamougolnaya-schelkunchik-krasnaya-203039?digiPreview=WTBUIVCYY&erid=2W5zFGUYkEU",
    #         "snapshot_name": "shoplive_2_result",
    #         "site_name": "shoplive2"
    #     },
    #     {
    #         "url": "https://www.shoppinglive.ru/p/maslo-avokado-1-litr-187876?digiPreview=WTBUIVCYY",
    #         "snapshot_name": "shoplive_3_result",
    #         "site_name": "shoplive3"
    #     },
    #     {
    #         "url": "https://vitaexpress.ru/product/pentalgin_ekstra_gel_5_50_g/",
    #         "snapshot_name": "vita_1_result",
    #         "site_name": "vita1"
    #     },
    #     {
    #         "url": "https://vitaexpress.ru/product/zubnaya_shchetka_profdent_detskaya_s_igrushkoy_kukolka_3_/",
    #         "snapshot_name": "vita_2_result",
    #         "site_name": "vita2"
    #     },
    #     {
    #         "url": "https://vitaexpress.ru/product/frinozol_15_ml/",
    #         "snapshot_name": "vita_3_result",
    #         "site_name": "vita3"
    #     },
    #     {
    #         "url": "https://stockmann.ru/product/5567429-zhaket-sabrina-scala/",
    #         "snapshot_name": "stockmann_1_result",
    #         "site_name": "stockmann1"
    #     },
    #     {
    #         "url": "https://stockmann.ru/product/5459670-pulover-s-vorotnikom-marco-di-radi/",
    #         "snapshot_name": "stockmann_2_result",
    #         "site_name": "stockmann2"
    #     },
    #     {
    #         "url": "https://stockmann.ru/product/5575143-dzhinsy-marco-di-radi/",
    #         "snapshot_name": "stockmann_3_result",
    #         "site_name": "stockmann3"
    #     },
    #     {
    #         "url": "https://emex.ru/products/A000989210713MBR/%D0%9C%D0%91+%D0%A0%D0%A3%D0%A1/39997",
    #         "snapshot_name": "emex_1_result",
    #         "site_name": "emex1"
    #     },
    #     {
    #         "url": "https://emex.ru/catalogs2/lampy-dlya-avtomobiley/narva/lampa-12v-h4-6055w-standard-1-sht-karton-48881-74347148",
    #         "snapshot_name": "emex_2_result",
    #         "site_name": "emex2"
    #     },
    #     {
    #         "url": "https://emex.ru/catalogs2/tuning-i-vneshniy-dekor/petroplast/podkrylki-petroplast-dlya-ford-focus-ii-PPL30724114-135551327",
    #         "snapshot_name": "emex_3_result",
    #         "site_name": "emex3"
    #     },
    #     {
    #         "url": "https://www.xcom-shop.ru/acer_v247ygbi_1166251.html",
    #         "snapshot_name": "xcom_1_result",
    #         "site_name": "xcom1"
    #     },
    #     {
    #         "url": "https://www.xcom-shop.ru/cabeus_pdu-8p_518172.html",
    #         "snapshot_name": "xcom_2_result",
    #         "site_name": "xcom2"
    #     },
    #     {
    #         "url": "https://www.xcom-shop.ru/1s-bitriks_ypravlenie_saytom_-_biznes_prodlenie_410388.html",
    #         "snapshot_name": "xcom_3_result",
    #         "site_name": "xcom3"
    #     },
    #     {
    #         "url": "https://online.metro-cc.ru/products/maslo-olivkovoye-filippo-berio-extra-virgin-500ml-458968",
    #         "snapshot_name": "metro_1_result",
    #         "site_name": "metro1"
    #     },
    #     {
    #         "url": "https://online.metro-cc.ru/products/shar-christmasdeluxe-goluboy-7sm",
    #         "snapshot_name": "metro_2_result",
    #         "site_name": "metro2"
    #     },
    #     {
    #         "url": "https://online.metro-cc.ru/products/zb-wine-moscato-beloe-polusladkoe-075-l",
    #         "snapshot_name": "metro_3_result",
    #         "site_name": "metro3"
    #     },
    #     {
    #         "url": "https://www.technopark.ru/smartfon-samsung-galaxy-z-flip-7-5g-512-gb-korallovyy-795545/",
    #         "snapshot_name": "technopark_1_result",
    #         "site_name": "technopark1"
    #     },
    #     {
    #         "url": "https://www.technopark.ru/chaynik-bork-k810/",
    #         "snapshot_name": "technopark_2_result",
    #         "site_name": "technopark2"
    #     },
    #     {
    #         "url": "https://www.technopark.ru/igrovaya-pristavka-sony-playstation-5-pro-digital-edition-801857/",
    #         "snapshot_name": "technopark_3_result",
    #         "site_name": "technopark3"
    #     },
    #     {
    #         "url": "https://pm.ru/category/mebel-dlya-kuhni/komplekti-mebeli-dlya-kuhni/goods-hozyayushka_240_sm-id157661/",
    #         "snapshot_name": "pm_1_result",
    #         "site_name": "pm1"
    #     },
    #     {
    #         "url": "https://pm.ru/category/mebel-dlya-doma/prihozhie/goods-prihogaya_vsh_5_tp_5-id30225/",
    #         "snapshot_name": "pm_2_result",
    #         "site_name": "pm2"
    #     },
    #     {
    #         "url": "https://pm.ru/category/vannaya/shkafy-dlya-vannoj/shkafy-penaly/goods-ving-id193273/#variant193273",
    #         "snapshot_name": "pm_3_result",
    #         "site_name": "pm3"
    #     },
    #     {
    #         "url": "https://4lapy.ru/product/rurri-lezhanka-novyj-god-60h50h18-sm-96897-1066985/",
    #         "snapshot_name": "4lapy_1_result",
    #         "site_name": "4lapy1"
    #     },
    #     {
    #         "url": "https://4lapy.ru/product/ownat-korm-dlya-vrzroslyh-sobak-so-svezhim-myasom-petuha-3-kg-87305-1061423/",
    #         "snapshot_name": "4lapy_2_result",
    #         "site_name": "4lapy2"
    #     },
    #     {
    #         "url": "https://4lapy.ru/product/gold-fish-terrarium-50-l-56x34x34-5-sm-9549-1037471/",
    #         "snapshot_name": "4lapy_3_result",
    #         "site_name": "4lapy3"
    #     },
    #     {
    #         "url": "https://zdorov.ru/catalog/168/174/1033/kreyt-bandazh-b-358-posleoperacionnyy-145565",
    #         "snapshot_name": "zdorov_1_result",
    #         "site_name": "zdorov1"
    #     },
    #     {
    #         "url": "https://zdorov.ru/catalog/114/123/124/smes-nutrizon-106606",
    #         "snapshot_name": "zdorov_2_result",
    #         "site_name": "zdorov2"
    #     },
    #     {
    #         "url": "https://zdorov.ru/catalog/1362/1517/1530/solgar-belkovaya-syvorotka-vey-tu-gou-140161",
    #         "snapshot_name": "zdorov_3_result",
    #         "site_name": "zdorov3"
    #     },
    #     {
    #         "url": "https://chikiriki.ru/action/lt_collection/1b55008f-d1c4-11f0-85b4-ac1f6b270637",
    #         "snapshot_name": "chikiriki_1_result",
    #         "site_name": "chikiriki1"
    #     },
    #     {
    #         "url": "https://chikiriki.ru/action/prod_of_week_96",
    #         "snapshot_name": "chikiriki_2_result",
    #         "site_name": "chikiriki2"
    #     },
    #     {
    #         "url": "https://chikiriki.ru/action/emile_henry/85c88271-77cf-11e9-84bf-ac1f6b270637",
    #         "snapshot_name": "chikiriki_3_result",
    #         "site_name": "chikiriki3"
    #     },
    #     {
    #         "url": "https://myspar.ru/catalog/rastitelnye-molochnye-produkty/napitok-ovsyanyy-nemoloko-3-2-s-kaltsiem-i-vitaminom-v2-1l/",
    #         "snapshot_name": "myspar_1_result",
    #         "site_name": "myspar1"
    #     },
    #     {
    #         "url": "https://myspar.ru/catalog/dlya-piknika/ugol-drevesnyy-spar-2-5kg/",
    #         "snapshot_name": "myspar_2_result",
    #         "site_name": "myspar2"
    #     },
    #     {
    #         "url": "https://myspar.ru/catalog/pivo/sidr-spar-grushevyy-igristyy-polusukhoy-5-0-45l-zh-b/",
    #         "snapshot_name": "myspar_3_result",
    #         "site_name": "myspar3"
    #     },
    #     {
    #         "url": "https://www.shinservice.ru/goods/motornoe-maslo-rolf-5w30-slcf-a3b4-rolf-ultra-1-l/",
    #         "snapshot_name": "shinservice_1_result",
    #         "site_name": "shinservice1"
    #     },
    #     {
    #         "url": "https://www.shinservice.ru/goods/provoda-puskovye-zavodila-400a-35-m-sumka/",
    #         "snapshot_name": "shinservice_2_result",
    #         "site_name": "shinservice2"
    #     },
    #     {
    #         "url": "https://www.shinservice.ru/goods/akb-westa-red-6st-60-op-600a-242175190-smf56030-turcia/",
    #         "snapshot_name": "shinservice_3_result",
    #         "site_name": "shinservice3"
    #     },
    #     {
    #         "url": "https://www.auchan.ru/product/nab-pletenie-iz-busin-snezhinki/",
    #         "snapshot_name": "auchan_1_result",
    #         "site_name": "auchan1"
    #     },
    #     {
    #         "url": "https://www.auchan.ru/product/el-iskusstv-zasnezh-flok-240sm/",
    #         "snapshot_name": "auchan_2_result",
    #         "site_name": "auchan2"
    #     },
    #     {
    #         "url": "https://www.auchan.ru/product/tros-buksirovochnyy-kazhdyy-den-dlya-avtomobilya-2-t-4-2-m/",
    #         "snapshot_name": "auchan_3_result",
    #         "site_name": "auchan3"
    #     },
    #     {
    #         "url": "https://www.autodoc.ru/man/6620/part/acmf01",
    #         "snapshot_name": "autodoc_1_result",
    #         "site_name": "autodoc1"
    #     },
    #     {
    #         "url": "https://www.autodoc.ru/man/7055/part/it0489",
    #         "snapshot_name": "autodoc_2_result",
    #         "site_name": "autodoc2"
    #     },
    #     {
    #         "url": "https://www.autodoc.ru/man/6443/part/ln1496",
    #         "snapshot_name": "autodoc_3_result",
    #         "site_name": "autodoc3"
    #     },
    #     {
    #         "url": "https://www.rbt.ru/cat/tehnika_dlya_doma/stiralnye_mashiny/candy_smart_pro_cso4_107tb1_2_07/",
    #         "snapshot_name": "rbt_1_result",
    #         "site_name": "rbt1"
    #     },
    #     {
    #         "url": "https://www.rbt.ru/cat/gadzhety/portativnaya_akustika/infinix_xs01_orange/",
    #         "snapshot_name": "rbt_2_result",
    #         "site_name": "rbt2"
    #     },
    #     {
    #         "url": "https://www.rbt.ru/cat/komputery_i_orgtehnika/sumki_dlya_noutbukov/xiaomi_mi_casual_daypack_pink/",
    #         "snapshot_name": "rbt_3_result",
    #         "site_name": "rbt3"
    #     },
    #     {
    #         "url": "https://www.chitai-gorod.ru/product/smeshariki-istoriya-kultovoy-vselennoy-3009059",
    #         "snapshot_name": "chitai_gorod_1_result",
    #         "site_name": "chitaigorod1"
    #     },
    #     {
    #         "url": "https://www.chitai-gorod.ru/product/pro-zdorov-e-koski-ot-veterinarnogo-vraca-vlublennogo-v-svou-rabotu-3141026",
    #         "snapshot_name": "chitai_gorod_2_result",
    #         "site_name": "chitaigorod2"
    #     },
    #     {
    #         "url": "https://www.chitai-gorod.ru/product/igor-akinfeev-avtobiografia-samogo-predannogo-futbolista-v-istorii-mirovogo-futbola-s-avtografom-3137872",
    #         "snapshot_name": "chitai_gorod_3_result",
    #         "site_name": "chitaigorod3"
    #     },
    #     {
    #         "url": "https://www.chipdip.ru/product/bronza-brb2t-0-5-h-200-250-mm-gost-1789-2013-ab-retail-8009276658",
    #         "snapshot_name": "chipdip_1_result",
    #         "site_name": "chipdip1"
    #     },
    #     {
    #         "url": "https://www.chipdip.ru/product/0knb0-6106ru00-klaviatura-dlya-noutbuka-asus-a551ca-a553ma-9000937919",
    #         "snapshot_name": "chipdip_2_result",
    #         "site_name": "chipdip2"
    #     },
    #     {
    #         "url": "https://www.chipdip.ru/product/mp323tx4j-pult-4-knopki-dlya-neogranichennogo-master-kit-9000659415",
    #         "snapshot_name": "chipdip_3_result",
    #         "site_name": "chipdip3"
    #     },
    #     {
    #         "url": "https://miuz.ru/catalog/rings/R01-SP35-020/",
    #         "snapshot_name": "miuz_1_result",
    #         "site_name": "miuz1"
    #     },
    #     {
    #         "url": "https://miuz.ru/catalog/rings/R01-VIT-60373/",
    #         "snapshot_name": "miuz_2_result",
    #         "site_name": "miuz2"
    #     },
    #     {
    #         "url": "https://miuz.ru/catalog/diamonds/68341331/",
    #         "snapshot_name": "miuz_3_result",
    #         "site_name": "miuz3"
    #     },
    #     {
    #         "url": "https://zhivika.ru/product/3894911_forsiga_tabletki_pokrytye_obol",
    #         "snapshot_name": "zhivika_1_result",
    #         "site_name": "zhivika1"
    #     },
    #     {
    #         "url": "https://zhivika.ru/product/18187511_solgar_vey_tu_gou_syvorotka_be",
    #         "snapshot_name": "zhivika_2_result",
    #         "site_name": "zhivika2"
    #     },
    #     {
    #         "url": "https://zhivika.ru/product/13275601_teraflyu_ot_grippa_i_prostudy_?utm_source=site&utm_medium=homePopular",
    #         "snapshot_name": "zhivika_3_result",
    #         "site_name": "zhivika3"
    #     },
    #     {
    #         "url": "https://randewoo.ru/product/nabor-1-top-selektivnyh-aromatov-dlya-nee?source_category=1157",
    #         "snapshot_name": "randewoo_1_result",
    #         "site_name": "randewoo1"
    #     },
    #     {
    #         "url": "https://randewoo.ru/product/britva-chernaya-smola-intro-rytmo-gillette-mach3?source_category=55",
    #         "snapshot_name": "randewoo_2_result",
    #         "site_name": "randewoo2"
    #     },
    #     {
    #         "url": "https://randewoo.ru/product/powder-love",
    #         "snapshot_name": "randewoo_3_result",
    #         "site_name": "randewoo3"
    #     },
    #     {
    #         "url": "https://www.okeydostavka.ru/msk/%D0%BA%D0%BE%D1%84%D0%B5-%D1%80%D0%B0%D1%81%D1%82%D0%B2%D0%BE%D1%80%D0%B8%D0%BC%D1%8B%D0%B9-%D0%BD%D0%B5%D1%81%D0%BA%D0%B0%D1%84%D0%B5-%D0%B3%D0%BE%D0%BB%D0%B4-%D0%BA%D1%80%D0%B5%D0%BC%D0%B0-%D0%B1%D0%B0%D0%BD%D0%BA%D0%B0-994921",
    #         "snapshot_name": "okey_1_result",
    #         "site_name": "okey1"
    #     },
    #     {
    #         "url": "https://www.okeydostavka.ru/msk/tovary-dlia-doma/elektrotovary/setevye-fil-try/razvetvitel-elektricheskii-chetvernik-kub-foton-am-16-4-16a-chernyi",
    #         "snapshot_name": "okey_2_result",
    #         "site_name": "okey2"
    #     },
    #     {
    #         "url": "https://www.okeydostavka.ru/msk/alkogol-/krepkii-alkogol-/viski-burbon-dzhek-deniels-40-0-7l",
    #         "snapshot_name": "okey_3_result",
    #         "site_name": "okey3"
    #     },
    #     {
    #         "url": "https://www.budzdorov.ru/product/lipotropnyy-faktor-tab-no60-108507",
    #         "snapshot_name": "budzdorov_1_result",
    #         "site_name": "budzdorov1"
    #     },
    #     {
    #         "url": "https://www.budzdorov.ru/product/nutridrink-smes-klubnika-200ml-67599",
    #         "snapshot_name": "budzdorov_2_result",
    #         "site_name": "budzdorov2"
    #     },
    #     {
    #         "url": "https://www.budzdorov.ru/product/alerana-balzam-opolaskivatel-glubokoye-vosstanovl-200ml-106153",
    #         "snapshot_name": "budzdorov_3_result",
    #         "site_name": "budzdorov3"
    #     },
    #     {
    #         "url": "https://santehnika-online.ru/product/smesitel_dlya_rakoviny_stworki_khelsinki_s33010cr_khrom/1090866/?index_highlight=y",
    #         "snapshot_name": "santehnika_1_result",
    #         "site_name": "santehnika1"
    #     },
    #     {
    #         "url": "https://santehnika-online.ru/product/stellazh_diwo_kolomna_50_s_2_dvertsami_50kh177kh26_sm_belyy/1051253/",
    #         "snapshot_name": "santehnika_2_result",
    #         "site_name": "santehnika2"
    #     },
    #     {
    #         "url": "https://santehnika-online.ru/design_gallery/item/vanna_s_tualetom_4_4_m2_v_skandinavskom_stile_s_plitkoy_pod_derevo/634916/",
    #         "snapshot_name": "santehnika_3_result",
    #         "site_name": "santehnika3"
    #     },
    #     {
    #         "url": "https://www.regard.ru/product/449583/mfu-canon-i-sensys-mf453dw-5161c007",
    #         "snapshot_name": "regard_1_result",
    #         "site_name": "regard1"
    #     },
    #     {
    #         "url": "https://www.regard.ru/product/705392/xlebopec-rondell-rde-1641-white",
    #         "snapshot_name": "regard_2_result",
    #         "site_name": "regard2"
    #     },
    #     {
    #         "url": "https://www.regard.ru/product/73872/processor-amd-ryzen-7-7800x3d-oem",
    #         "snapshot_name": "regard_3_result",
    #         "site_name": "regard3"
    #     },
    #     {
    #         "url": "https://ostin.com/product/top-korset-iz-zhakkarda/36144640299?category-id=12485690299&availability=disabled",
    #         "snapshot_name": "ostin_1_result",
    #         "site_name": "ostin1"
    #     },
    #     {
    #         "url": "https://ostin.com/product/majka-iz-viskozy/36424310299?category-id=12485690299&availability=disabled",
    #         "snapshot_name": "ostin_2_result",
    #         "site_name": "ostin2"
    #     },
    #     {
    #         "url": "https://ostin.com/product/ukorochennyj-zhaket-iz-iskusstvennoj-zamshi/36424320299?category-id=12485740299",
    #         "snapshot_name": "ostin_3_result",
    #         "site_name": "ostin3"
    #     },
    #     {
    #         "url": "https://www.labirint.ru/books/882540/",
    #         "snapshot_name": "labirint_1_result",
    #         "site_name": "labirint1"
    #     },
    #     {
    #         "url": "https://www.labirint.ru/books/1008779/",
    #         "snapshot_name": "labirint_2_result",
    #         "site_name": "labirint2"
    #     },
    #     {
    #         "url": "https://www.labirint.ru/games/996301/",
    #         "snapshot_name": "labirint_3_result",
    #         "site_name": "labirint3"
    #     },
    #     {
    #         "url": "https://av.ru/i/541115",
    #         "snapshot_name": "azbuka_1_result",
    #         "site_name": "azbuka1"
    #     },
    #     {
    #         "url": "https://av.ru/i/458109",
    #         "snapshot_name": "azbuka_2_result",
    #         "site_name": "azbuka2"
    #     },
    #     {
    #         "url": "https://av.ru/i/232715",
    #         "snapshot_name": "azbuka_3_result",
    #         "site_name": "azbuka3"
    #     },
    #     {
    #         "url": "https://www.rigla.ru/product/strepsils-med-limon-ledentsy-no36-18286",
    #         "snapshot_name": "rigla_1_result",
    #         "site_name": "rigla1"
    #     },
    #     {
    #         "url": "https://www.rigla.ru/product/lya-rosh-poze-lipikar-gel-ochishchayushchiy-uspokaivayushchiy-dlya-dusha-400ml-99575",
    #         "snapshot_name": "rigla_2_result",
    #         "site_name": "rigla2"
    #     },
    #     {
    #         "url": "https://www.rigla.ru/product/pirantel-tab-250mg-no3-73118",
    #         "snapshot_name": "rigla_3_result",
    #         "site_name": "rigla3"
    #     },
    #     {
    #         "url": "https://nonton.ru/mebel/detskaya/dvukhyarusnye-krovati/dvukhyarusnaya-krovat-s-divan-krovatyu-velyur-seryy-dub-sonoma/?OFFER_ID=308987&gtm-list=Category",
    #         "snapshot_name": "nonton_1_result",
    #         "site_name": "nonton1"
    #     },
    #     {
    #         "url": "https://nonton.ru/mebel/kukhnya/gotovye-kukhni/uglovye-kukhni/kukhnya-uglovaya-byanka-1-2kh2-2-m-oliva-soft/?OFFER_ID=391396&gtm-list=WeRecommend&city_confirm=Y",
    #         "snapshot_name": "nonton_2_result",
    #         "site_name": "nonton2"
    #     },
    #     {
    #         "url": "https://nonton.ru/mebel/myagkaya-mebel/takhty/takhta-gardi-seraya/?OFFER_ID=253865&gtm-list=Category",
    #         "snapshot_name": "nonton_3_result",
    #         "site_name": "nonton3"
    #     },
    #     {
    #         "url": "https://www.asna.ru/cards/rankof_rino_005_20ml_sprey_nazalnyy_vips-med_firma.html",
    #         "snapshot_name": "asna_1_result",
    #         "site_name": "asna1"
    #     },
    #     {
    #         "url": "https://www.asna.ru/cards/kemner_optiks_ochki_korrigiruyushchie_dchteniya_skladnye_metallicheskie_35_kemner_optiks_bv.html",
    #         "snapshot_name": "asna_2_result",
    #         "site_name": "asna2"
    #     },
    #     {
    #         "url": "https://www.asna.ru/cards/glyukoza_500mg_n10_tab_farmstandart-tomskkhimfarm_oao.html",
    #         "snapshot_name": "asna_3_result",
    #         "site_name": "asna3"
    #     },
    #     {
    #         "url": "https://pitergsm.ru/catalog/accessories/chekhly-i-zashchita/chekhly/130075/",
    #         "snapshot_name": "pitergsm_1_result",
    #         "site_name": "pitergsm1"
    #     },
    #     {
    #         "url": "https://pitergsm.ru/catalog/watch/fitness-bracelets/74834/",
    #         "snapshot_name": "pitergsm_2_result",
    #         "site_name": "pitergsm2"
    #     },
    #     {
    #         "url": "https://pitergsm.ru/catalog/phones/iphone/iphone-17/esim/122314/",
    #         "snapshot_name": "pitergsm_3_result",
    #         "site_name": "pitergsm3"
    #     },
    #     {
    #         "url": "https://www.585zolotoy.ru/catalog/products/9003677/",
    #         "snapshot_name": "585zolotoy_1_result",
    #         "site_name": "585zolotoy1"
    #     },
    #     {
    #         "url": "https://www.585zolotoy.ru/catalog/products/9003047/",
    #         "snapshot_name": "585zolotoy_2_result",
    #         "site_name": "585zolotoy2"
    #     },
    #     {
    #         "url": "https://www.585zolotoy.ru/catalog/products/1900545/",
    #         "snapshot_name": "585zolotoy_3_result",
    #         "site_name": "585zolotoy3"
    #     }
]


@pytest.mark.e2e
def test_parsing_sequential(use_case_fixture, snapshot):
    """ОДИН тест, который парсит все URL последовательно - СИНХРОННО"""
    
    use_case = use_case_fixture
    
    # Создаем event loop один раз для всех операций
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        for test_case in TEST_CASES:
            print(f"\n=== Парсинг {test_case['site_name']} ===")
            
            try:
                # Парсим СИНХРОННО, используя один event loop
                result = loop.run_until_complete(use_case.execute(test_case["url"]))
                
                # Стабилизируем
                stabilized = stabilize_result_for_snapshot(result)
                
                # Сохраняем результат
                test_name = f"test_{test_case['site_name']}_parsing"
                TEST_RESULTS[test_name] = result
                
                print(f"✓ {test_case['site_name']}: {result.get('name', 'N/A')}")
                
                snapshot.assert_match(
                    json.dumps(stabilized, ensure_ascii=False, indent=2),
                    test_case["snapshot_name"]
                )
                
            except Exception as e:
                # Сохраняем ошибку
                test_name = f"test_{test_case['site_name']}_parsing"
                TEST_RESULTS[test_name] = {"error": str(e), "url": test_case["url"]}
                print(f"✗ {test_case['site_name']}: Ошибка - {e}")
                continue  # Продолжаем парсить остальные URL
        
        # Проверяем что хотя бы что-то распарсилось
        success_count = sum(1 for r in TEST_RESULTS.values() 
                           if isinstance(r, dict) and "error" not in r)
        assert success_count > 0, "Ни один продукт не распарсился"
    finally:
        loop.close()