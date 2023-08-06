import sys
import asyncio
import urllib.parse
from uuid import uuid4

import httpx
import found
from found import nstore
from found import bstore
from loguru import logger as log

try:
    import ujson as json
except ImportError:
    import json


# XXX: https://github.com/Delgan/loguru
log.debug("That's it, beautiful and simple logging!")


async def get(http, url, params=None):
    response = await http.get(url, params=params)
    if response.status_code == 200:
        return response.content

    log.error("http get failed with url and reponse: {} {}", url, response)
    return None



def make_timestamper():
    import time
    start_monotonic = time.monotonic()
    start = time.time()
    loop = asyncio.get_event_loop()

    def timestamp():
        # Wanna be faster than datetime.now().timestamp()
        # approximation of current epoch time.
        out = start + loop.time() - start_monotonic
        out = int(out)
        return out

    return timestamp


async def wikimedia_titles(http, wiki="https://en.wikipedia.org/"):
    log.debug('Started generating asynchronously wiki titles at {}', wiki)
    # XXX: https://www.mediawiki.org/wiki/API:Allpages#Python
    url = "{}/w/api.php".format(wiki)
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "apfilterredir": "nonredirects",
        "apfrom": "",
    }

    for i in range(50):
        content = await get(http, url, params=params)
        if content is None:
            continue
        content = json.loads(content)

        for page in content["query"]["allpages"]:
            yield page["title"]
        try:
            apcontinue = content['continue']['apcontinue']
        except KeyError:
            return
        else:
            params["apfrom"] = apcontinue


async def wikimedia_html(http, wiki="https://en.wikipedia.org/", title="Apple"):
    # e.g. https://en.wikipedia.org/api/rest_v1/page/html/Apple
    url = "{}/api/rest_v1/page/html/{}".format(wiki, urllib.parse.quote(title))
    out = await get(http, url)
    return wiki, title, out


async def save(tx, data, blob, doc):
    uid = uuid4()
    doc['html'] = await bstore.get_or_create(tx, blob, doc['html'])

    for key, value in doc.items():
        nstore.add(tx, data, uid, key, value)

    return uid


WIKIS = (
    "https://en.wikipedia.org/",
    "https://fr.wikipedia.org/",
    "https://en.wiktionary.org/",
    "https://fr.wiktionary.org/",
)

async def chunks(iterable, size):
    # chunk async generator https://stackoverflow.com/a/22045226
    while True:
        out = list()
        for _ in range(size):
            try:
                item = await iterable.__anext__()
            except StopAsyncIteration:
                yield out
                return
            else:
                out.append(item)
        yield out


async def main():
    # logging
    log.remove()
    log.add(sys.stderr, enqueue=True)

    # singleton
    timestamper = make_timestamper()
    database = await found.open()
    data = nstore.make('data', ('sourcery-data',), 3)
    blob = bstore.make('blob', ('sourcery-blob',))

    async with httpx.AsyncClient() as http:
        for wiki in WIKIS:
            log.info('Getting started with wiki at {}', wiki)
            # Polite limit @ https://en.wikipedia.org/api/rest_v1/
            async for chunk in chunks(wikimedia_titles(http, wiki), 200):
                log.info('iterate')
                coroutines = (wikimedia_html(http, wiki, title) for title in chunk)
                items = await asyncio.gather(*coroutines, return_exceptions=True)
                for item in items:
                    if isinstance(item, Exception):
                        msg = "Failed to fetch html on `{}` with `{}`"
                        log.error(msg, wiki, item)
                        continue
                    wiki, title, html = item
                    if html is None:
                        continue
                    log.debug(
                        "Fetch `{}` at `{}` with length {}",
                        title,
                        wiki,
                        len(html)
                    )

                    doc = dict(
                        wiki=wiki,
                        title=title,
                        html=html,
                        timestamp=timestamper(),
                    )

                    await found.transactional(database, save, data, blob, doc)


if __name__ == "__main__":
    asyncio.run(main())
