# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tlo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tlo',
    'version': '1.0.0',
    'description': 'Reader of binary serialized Type Language Schema',
    'long_description': '## Type Language Object\n\n> Reader of [binary serialized](https://core.telegram.org/mtproto/serialize) Type Language Schema\n\n### Example of result in the end of reading TLO\n\n<center>\n    <img src="https://raw.githubusercontent.com/MarshalX/tlo/main/.github/resources/demo.gif" alt="demo">\n</center>\n\n### Declaimer\n\nThis code has not been tested sufficiently. \nIt\'s a rewritten version of original reader in C++.\nIf you are going to use this for code generation, \nplease do additional tests. \nRecheck my implementation for errors and so on.\n\n### Context\n\nThe [Type Language (TL)](https://core.telegram.org/mtproto/TL) was\ninvented many years ago. It was originally used in [VK](https://vk.com/),\nand now in [Telegram](https://telegram.org). \nThe creators of this language invented and \nwrote all the necessary tools to work with it.\nFor example, a [parser of the language](https://github.com/vysheng/tl-parser)\nand its [binary format](https://core.telegram.org/mtproto/serialize)\nfor serialization was developed.\n\n### What is this for?\n\nTo work with TL Schemes using OOP. To generate the client MTProto code using\nofficial TL parsers and binary formats.\n\nMany Open Source MTProto client use their own implementation of parsers, \nwhich are not ultimatum. They are hardcoded for their minimal task.\n\nHardcode is not the way of Telegram. Official Telegram\'s Open Source projects \ntake the right approach. So, for example, [tdlib](https://github.com/tdlib/td)\ngenerates several interfaces for different languages and this is how it looks:\n\nRaw TL Schema -> Tl Parser -> binary TL Object -> **TLO reader** -> code generator.\n\n| Step name | Description |\n| --------- | ----------- |\n| Raw TL Schema  | Can be founded [here](https://core.telegram.org/schema) and in official Telegram repositories of client ([tdesktop/Telegram/Resources/tl](https://github.com/telegramdesktop/tdesktop/tree/dev/Telegram/Resources/tl), [tdlib/generate/scheme](https://github.com/tdlib/td/tree/master/td/generate/scheme)).  |\n| Tl Parser | Official TL parser written in C++. Now it\'s a part of [tdlib/td/generate/tl-parser](https://github.com/tdlib/td/tree/master/td/generate/tl-parser). In the input it takes raw TL schema file. The output is TLO file. |\n| binary TL Object | The output of Tl Parser. |\n| **TLO reader** | **This repository contains implementation of it in Python and JavaScript.** Reader of binary file. Provide access to combinators, types, functions, arguments and so on via Object Oriented Programming. |\n| code generator | Any code generator. In [tdlib/td/generate](https://github.com/tdlib/td/tree/master/td/generate) there is generator for C++, JNI, .NET and JSON interfaces. |\n\n### Installing\n\n#### For Python\n```bash\npip install tlo\n```\n\n#### ~~For JavaScript~~ Work in progress\n```bash\nnpm install tlo\n```\n\n### Usage\n\nYou can find TLO files for tests [here](https://github.com/MarshalX/tlo/tree/main/tlo_for_tests).\n\n#### Python (3.6+)\n```python\nfrom tlo import read_tl_config_from_file, read_tl_config\n\n\n# use read_tl_config(data) to pass bytes directly\nconfig = read_tl_config_from_file(\'td_api.tlo\')\n```\n\n#### ~~JavaScript~~ Work in progress\n```javascript\nimport {read_tl_config_from_file, read_tl_config} from \'tlo\';\n\n\n// use read_tl_config(data) to pass bytes directly\nconst config = read_tl_config_from_file(\'td_api.tlo\')\n```\n\n### Licence\n\nMIT License\n',
    'author': "Il'ya Semyonov",
    'author_email': 'ilya@marshal.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
