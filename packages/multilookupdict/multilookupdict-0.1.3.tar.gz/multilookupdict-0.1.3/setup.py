# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multilookupdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'multilookupdict',
    'version': '0.1.3',
    'description': 'A dict-like container that allows multiple keys to address the same value.',
    'long_description': '# Multi-Lookup-Dict\n\nA Dict-like container that allows multiple keys to address the same value.\n\n```python\n>>> d = MultiLookupDict()\n>>> d["a_key"] = "some_value"\n>>> d.map_key("a_key", "another_key") # Make "another_key" an alias of "a_key"\n\nImplemented as two dicts:\n    - `MultiLookupDict._data` holds the \'canonical key\' and value\n    - `MultiLookupDict._key_to_canonical_map` maps \'alias keys\' onto canonical keys.\n        (Canonical keys are mapped to themselves in this dict)\n```\nExternally, all keys (canonical and alias) are treated identically,\nand all refer to the same value, unless a key is reassigned to another value using `map_key`.\n\n\nMulti-key lookups and assignments\n---------------------------------\n\nIterables of keys can also be accessed, set, and mapped.\n\n```python\n>>> d = MultiLookupDict()\n>>> d[("key_a", "key_b", "key_c")] = "some_value"\n>>> d["key_a"] == "some_value"\n\nWhere items are accessed with multiple keys, all distinct matching values are returned\nas a list (where multiple keys are requested, the result is always a list, for consistency)\n\n>>> d["key_d"] = "some_other_value" # Add a distinct value\n>>> d[("key_a", "key_b", "key_d")] == ["some_value", "some_other_value"]\n\n\n>>> d.map_key("key_a", ("key_e", "key_f")) # Also do multiple mappings\n```\n\n...\n\nMethods\n-------\n\n__setitem__\n    Sets a key to the value. If a (non-string) iterable is provided\n    as key, each key will be assigned the value.\n__getitem__\n    [As with standard Python dict]\nmap_key\n    Assign the value of one key to another key. Both keys\n    now point to the same value.\nkeys\n    Returns all keys in MultiLookupDict. Returned keys refer to same or different objects.\nall_keys\n    [Same as `keys`]\nvalues\n    [Same as `dict.values`]\nitems\n    Same as `dict.items`, except key part of tuple is a `set` of keys for the corresponding value\npop\n    Same as `dict.pop`. All keys pointing to value are removed.\naliases\n    Returns all aliases of a given key',
    'author': 'Richard Hadden',
    'author_email': 'richard.hadden@oeaw.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richardhadden/multilookupdict',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
