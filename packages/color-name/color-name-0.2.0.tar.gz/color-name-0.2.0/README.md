Color-name
==========

Color-name converts RGB values to English names. 

`pip install color-name`

Example Usage
=============

```python
    >>>import colorname
    >>>colorname.get_color_name(255, 0, 0)
    'red'
    >>>colorname.get_color_name(129, 128, 128)
    'gray'
    >>> while colorname.get_pixel_color_name(600, 800) != 'white':
    ...     pass
    ...
```

Versioning
----------

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see [releases](https://github.com/tvanderplas/color-name/releases). 

Authors
-------

* **Tim Vanderplas** - *Initial work* - [tvanderplas](https://github.com/tvanderplas)
