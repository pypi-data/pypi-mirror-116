# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kraky']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0', 'websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'kraky',
    'version': '2021.8',
    'description': 'Python asyncio client for Kraken API REST and Kraken Websockets API using httpx and websockets',
    'long_description': '[![Total alerts](https://img.shields.io/lgtm/alerts/g/Atem18/kraky.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Atem18/kraky/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Atem18/kraky.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Atem18/kraky/context:python)\n\n# Kraky\nPython asyncio client for Kraken API REST and Kraken Websockets API using httpx and websockets\n\n## Installation \n    pip install kraky\n\n## Docs\n\n    https://kraky.readthedocs.io/en/latest/\n\n## Usage\n\n### REST\n\n    from kraky import KrakyApiClient\n\n    async def get_web_sockets_token():\n        kraken_api_key = ""\n        kraken_secret = ""\n        kraky_api_client = KrakyApiClient(\n            api_key=kraken_api_key, secret=kraken_secret\n        )\n\n        ws_token = await self.kraky_api_client.get_web_sockets_token()\n        return ws_token\n\n### Websocket\n\n    from kraky import KrakyApiClient, KrakyWsClient\n\n    async def get_ws_token():\n        kraken_api_key = ""\n        kraken_secret = ""\n        kraky_api_client = KrakyApiClient(\n            api_key=kraken_api_key, secret=kraken_secret\n        )\n\n        ws_token = await self.kraky_api_client.get_web_sockets_token()\n        return ws_token\n\n    async def public_handler(self, response):\n        print(response)\n    \n    async def private_handler(self, response):\n        print(response)\n\n    async def main():\n\n        interval = 30\n\n        ws_pairs = ["XBT/USD", "ETH/USD]\n\n        ws_token = get_token()\n\n        kraky_public_ws_client = KrakyWsClient("production")\n        kraky_private_ws_client = KrakyWsClient("production-auth")\n\n        asyncio.create_task(\n            kraky_public_ws_client.connect(\n                public_handler, connection_name="public"\n            )\n        )\n\n        asyncio.create_task(\n            kraky_private_ws_client.connect(\n                private_handler, connection_name="private"\n            )\n        )\n\n        await kraky_public_ws_client.subscribe(\n            {"name": "ohlc", "interval": interval},\n            ws_pairs,\n            connection_name="public",\n        )\n\n        await kraky_private_ws_client.subscribe(\n            {\n                "interval": interval,\n                "token": ws_token,\n                "name": "openOrders",\n            },\n            connection_name="private",\n        )\n\n    if __name__ == "__main__":\n        loop = asyncio.get_event_loop()\n        loop.create_task(main())\n        loop.run_forever()\n\n## Compatibility\n\n- Python 3.7 and above\n\n## Licence\n\nMIT License\n',
    'author': 'Atem18',
    'author_email': 'contact@atemlire.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kraky.readthedocs.io/en/latest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
