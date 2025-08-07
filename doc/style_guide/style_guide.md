# Style Guide

## General

Stick to PEP8 style guide as much as possible.

## Capitalization

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

## Avoid the use of abbreviations in names as much as possible

While the abbreviation may seem clear at the time of writing, it may not be clear to others later on.  
E.g. ´fi´ could be interpreted as 'file', 'file_info', etc.

| Approved abbreviations | Discouraged abbreviations |
|------------------------|---------------------------|
| app, i, j              | fi, pos, dir, d, f        |

i, j are allowed as loop variables in for loops, but should not be used in other contexts.

## Files en folder variable names

Avoid using `dir, d, fi, f`  
Instead use:

- `file` for files (objects)
- `file_name` for base file names (str)
- `file_path` for full file paths, absolute or relative (str)


- `folder` for folders (objects)
- `folder_name` for base folder names (str)
- `folder_path` for full folder paths, absolute or relative (str)

Use prefixes to make it more specific if required. E.g.:

- `image_file` for image files