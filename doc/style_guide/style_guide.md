# Style Guide

PyQt are automatically generated python bindings for the C++ Qt framework.  
In the C++ API camelCase is used.  
As a consequence, PyQt has camelCase bindings...

Any code added to this repository should follow the python PEP8 style guide.  
Some examples:

- classes should be named using CamelCase
- functions and variables should be named using snake_case
- constants should be named using ALL_CAPS_WITH_UNDERSCORES
- use 4 spaces for indentation
- use spaces around operators and after commas

There is one exception to this rule:

- When overriding or interacting with Qt API methods, one must follow camelCase.
