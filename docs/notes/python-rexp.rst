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


Back Reference
--------------

.. code-block:: python

    # compare 'aa', 'bb'
    >>> re.search(r'([a-z])\1$','aa') != None
    True
    >>> re.search(r'([a-z])\1$','bb') != None
    True
    >>> re.search(r'([a-z])\1$','ab') != None
    False

    # compare open tag and close tag
    >>> pattern = r'<([^>]+)>[\s\S]*?</\1>'
    >>> re.search(pattern, '<bold> test </bold>') != None
    True
    >>> re.search(pattern, '<h1> test </h1>') != None
    True
    >>> re.search(pattern, '<bold> test </h1>') != None
    False


Named Grouping ``(?P<name>)``
-----------------------------

.. code-block:: python

    # group reference ``(?P<name>...)``
    >>> pattern = '(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    >>> m = re.search(pattern, '2016-01-01')
    >>> m.group('year')
    '2016'
    >>> m.group('month')
    '01'
    >>> m.group('day')
    '01'

    # back reference ``(?P=name)``
    >>> re.search('^(?P<char>[a-z])(?P=char)','aa')
    <_sre.SRE_Match object at 0x10ae0f288>
