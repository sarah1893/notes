====================================
Python Regular Expression cheatsheet
====================================

Compare HTML tags
-----------------

+------------+--------------+--------------+
| tag type   | format       | example      |
+============+==============+==============+
| all tag    | <[^>]+>      | <br />, <a>  |
+------------+--------------+--------------+
| open tag   | <[^/>][^>]*> | <a>, <table> |
+------------+--------------+--------------+
| close tag  | </[^>]+>     | </p>, </a>   |
+------------+--------------+--------------+
| self close | <[^/>]+/>    | <br />       |
+------------+--------------+--------------+


.. code-block:: python

    # open tag
    >>> re.search('<[^/>][^>]*>', '<table>') != None
    True
    >>> re.search('<[^/>][^>]*>', '<a href="#label">') != None
    True
    >>> re.search('<[^/>][^>]*>', '<img src="/img">') != None
    True
    >>> re.search('<[^/>][^>]*>', '</table>') != None
    False

    # close tag
    >>> re.search('</[^>]+>', '</table>') != None
    True

    # self close
    >>> re.search('<[^/>]+/>', '<br />') != None
    True

``re.findall()`` match string 
-----------------------------

.. code-block:: python

    # split all string
    >>> re.findall('[\w]+', source)
    ['Hello', 'World', 'Ker', 'HAHA']

    # parsing python.org website
    >>> import urllib
    >>> import re
    >>> s = urllib.urlopen('https://www.python.org')
    >>> html = s.read()
    >>> s.close()
    >>> print "open tags"
    open tags
    >>> re.findall('<[^/>][^>]*>', html)[0:2]
    ['<!doctype html>', '<!--[if lt IE 7]>']
    >>> print "close tags"
    close tags
    >>> re.findall('</[^>]+>', html)[0:2]
    ['</script>', '</title>']
    >>> print "self-closing tags"

Group Comparison
----------------

.. code-block:: python

    # (...) group a regular expression
    >>> m = re.search(r'(\d{4})-(\d{2})-(\d{2})', '2016-01-01')
    >>> m
    <_sre.SRE_Match object; span=(0, 10), match='2016-01-01'>
    >>> m.groups()
    ('2016', '01', '01')
    >>> m.group()
    '2016-01-01'
    >>> m.group(1)
    '2016'
    >>> m.group(2)
    '01'
    >>> m.group(3)
    '01'

    # Nesting groups
    >>> m = re.search(r'(((\d{4})-\d{2})-\d{2})', '2016-01-01')
    >>> m.groups()
    ('2016-01-01', '2016-01', '2016')
    >>> m.group()
    '2016-01-01'
    >>> m.group(1)
    '2016-01-01'
    >>> m.group(2)
    '2016-01'
    >>> m.group(3)
    '2016'
