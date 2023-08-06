Behave to Cucumber (Zephyr) formatter
============================

This project converts the behave json reports to a cucumber(like) json file, 
that can be used with Zephyr Scale. The original work can be found here: https://github.com/behalf-oss/behave2cucumber

This script was developed during work on automation tools for Behalf inc. automation team.
The script was developed and tested on Python 2.7, you're welcome to use this script and format it to other python versions.

For easy install use: "pip install behave2cucumberZephyr"

Example of usage:
 .. code-block:: python

    import json
    import behave2cucumberZephyr
    with open('behave_json.json') as behave_json:
        cucumber_json = behave2cucumberZephyr.convert(json.load(behave_json))


Running from bash
-------------------------
Main has been added thanks to @lawnmowerlatte and now you can run:
 .. code-block:: bash
 
   python -m behave2cucumberZephyr


Running tests
-------------------------
To run tests: 
 .. code-block:: bash
    
    ./test_script
