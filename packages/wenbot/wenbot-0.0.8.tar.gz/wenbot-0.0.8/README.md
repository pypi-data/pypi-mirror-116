# wenbot
Simple bot wrapper of selenium basic functions

Sample code:
```
import wenbot

bot = wenbot.Bot()
bot.play([
    ('open', 'https://www.google.co.nz/'),
    ('text', 'input[name=q]', 'pip wenbot', 'clear, enter'),
])
input('enter to stop browser')
```

# optional proxy support
Requires browsermob-proxy binary, see https://github.com/lightbody/browsermob-proxy/releases.
Requires java to run browsermob-proxy binary.
Default browsermob-proxy binary path is set in `wenbot.browsermob_proxy_bin`.
Requires pypi package *browsermobproxy*, install `pip install browsermob-proxy`.

Sample setup:
- download [browsermob-proxy-2.1.4-bin.zip](https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip)
- `unzip browsermob-proxy-2.1.4-bin.zip` in current directory, it will create folder browsermob-proxy-2.1.4-bin
- make sure `java` works

Sample code:
```
import json
import pydash
import wenbot

bot = wenbot.Bot(proxy=True)
input('enter to print log and stop browser')
# Chrome window shows up.
# After open webpage and operations
har = bot.proxy.har  # this is a property that pulls data from server
# bot.proxy is a browsermobproxy.client.Client object
# see https://browsermob-proxy-py.readthedocs.io/en/stable/client.html
# har is recorded log
with open('/tmp/har.json', 'wt') as f:
    print(json.dumps(har, indent=4, default=str), file=f)

for entry in pydash.get(har, 'log.entries') or []:
    print(pydash.get(entry, "request.url"))
    print(f'    method={pydash.get(entry, "request.method")}')
    print('    Headers')
    for header in pydash.get(entry, 'request.headers') or []:
        print(f'        {header["name"]}: {header["value"]}')
    print(f'    status={pydash.get(entry, "response.status")}')
```

Try sample code and open `/tmp/har.json` see what's HAR structure.

Use `bot.proxy.new_har()` to record new HAR data.

Default only record headers, not content or binary content (in brosermob-proxy terms).


# change history
0.0.8 2021-08-19 add sample code
0.0.7 2021-07-14 bugfix
0.0.6 2021-07-14 replace print with log
0.0.5 2021-07-14 Bumps urllib3 from 1.26.4 to 1.26.5

