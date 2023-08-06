# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src2prod']

package_data = \
{'': ['*']}

install_requires = \
['spkpb>=0.0.10-beta.0,<0.0.11']

setup_kwargs = {
    'name': 'src2prod',
    'version': '0.0.1b0',
    'description': 'This module allows to develop a project within a source folder and to publish the final product in another folder, this last directory being a "thin" version of the source one.',
    'long_description': 'The `Python` module `src2prod`\n==============================\n\n\n> **I beg your pardon for my english...**\n>\n> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.\n\n\nAbout `src2prod`\n----------------\n\nThis module allows to develop a project within a source folder and to publish the final product in another folder, this last directory being a "thin" version of the source one. If you use `git`, this module can talk with it to do a better job. \n\n\n### One example - A `Python` project\n\n#### What we have...\n\nLet\'s consider [`TeXitEasy`](https://github.com/projetmbc/tools-for-latex/tree/master/TeXitEasy)  which had merly the following tree structure on August 9, 2021 (this was the very begining of this project).\n\n~~~\n+ changes\n    + 2021\n        * 08.txt\n    * LICENSE.txt\n    * x-todo-x.txt\n\n+ src\n    * __init__.py\n    * escape.py\n    * LICENSE.txt\n    + tool_config\n        * escape.peuf\n    * tool_debug.py\n    * tool_escape.py\n\n+ tests\n    + escape\n        * escape.peuf\n        * fstringit.peuf\n        * test_fstringit.py\n        * test_escape.py\n* about.peuf\n* pyproject.toml\n* README.md\n~~~\n\n\n#### What we want...\n\nIn the tree above, there are some files just useful for the development of the code.\n\n  1. Names using the pattern `x-...-x` indicate files or folders to be ignored by `git` (there are no such file or folder in the `src` folder but we could imagine using some of them).\n\n  1. Names using the pattern `tool_...` are for files and folders to not copy into the final product, but at the same time to be kept by `git`.\n\n  1. The `README.md` file used for `git` servers must also be used for the final product.\n\n\nThe final product built from the `src` folder must have the following name and structure. \n\n~~~\n+ texiteasy\n    * __init__.py\n    * escape.py\n    * LICENSE.txt\n    * README.md\n~~~\n\n\n#### How to do that?\n\nHere is how to acheive a selective copy of the `src` folder to the `texiteasy` one. We will suppose the use of the `cd` command to go inside the parent folder of `TeXitEasy` before launching the following script where we use instances of `Path` from `pathlib`.\n\n~~~python\nfrom src2prod import *\n\nproject = Project(\n    project = Path(\'TeXitEasy\'),\n    source  = Path(\'src\'),\n    target  = Path(\'texiteasy\'),\n    ignore  = \'\'\'\n        tool_*/\n        tool_*.*\n    \'\'\',\n    usegit = True,\n    readme = Path(\'README.md\')\n)\n\nproject.update()\n~~~\n\nHere are some important points about the code above.\n\n  1. The values of `project`, `source`, `target` and `readme` can also be strings (that will be converted to instances of `Path`).\n\n  1. The argument `readme` is optional contrary to `project`, `source` and `target`.\n\n  1. The rules for the argument `ignore` follow the `gitignore` syntax. You can use this argument even if you don\'t work with `git`.\n\n  1. `usegit = True` asks to ignore files and folders as `git` does. This also implies that there isn\'t any uncommited files in the `src` folder.\n\n  1. Errors and warnings are printed in the terminal and written verbosely in the file `TeXitEasy.src2prod.log`.\n\n\n### All the source files to copy\n\nSometimes the final product is not just a "selective clone" of the `src` folder: for example, it can be a melting of several source files in a single final one (the author of `src2prod` uses this technic to develop his `LaTeX` projects). In such a case, you can use the following method and attribut.\n\n  1. The method `build` just looks for the files to keep for the `texiteasy` folder.\n\n  1. The attribut `lof` is the list of all files to keep in the `src` folder (`lof` is for `list of files`).\n\nHere is an example of code printing the list of only the source files to keep.\n\n~~~python\nfrom src2prod import *\n\nproject = Project(\n    name   = \'TeXitEasy\',\n    source = Path(\'src\'),\n    target = Path(\'texiteasy\'),\n    ignore = \'\'\'\n        tool_*/\n        tool_*.*\n    \'\'\',\n    usegit = True,\n    readme = Path(\'README.md\')\n)\n\nproject.build()\n\nfor f in project.lof:\n    print(f)\n~~~\n\nThis script gives the following output in a terminal. Note that the list doesn\'t contain the path of the `README` file, this last one must be manage by hand (see the methods `check_readme` and `copy_readme` of the class `Project`). \n\n~~~\n/full/path/to/TeXitEasy/src/__init__.py\n/full/path/to/TeXitEasy/src/escape.py\n/full/path/to/TeXitEasy/src/LICENSE.txt\n~~~\n\n\n<!-- :tutorial-START: -->\n<!-- :tutorial-END: -->\n\n\n<!-- :version-START: -->\n<!-- :version-END: -->\n',
    'author': 'Christophe BAL',
    'author_email': None,
    'maintainer': 'Christophe BAL',
    'maintainer_email': None,
    'url': 'https://github.com/projetmbc/tools-for-dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
