.. raw:: html

   <style> .return {color:green; font-weight:bold} </style>
   <style> .printhl {color:green} </style>
   <style> .magic {color:blue} </style>

.. role:: return
.. role:: printhl
.. role:: magic

And a word without color

#####
USAGE
#####

Substitute python's print
=========================

Import in script.
Supply value for `mark` and/or for any of the custom \*\*kwargs as `described <source-code-doc.html#psprint.printer.PrintSpace.psprint>`__.


.. code-block:: python
   :caption: psprint_basic.py
   :name: basic usage

   from psprint import print

   print('Hello World', mark='info')


Frequently used `mark`\ s
---------------------------

Configure frequently used `mark`\ s in a suitably `located <configure.html#location-of-configuration-files>`__ configuration file.

Marks `cont`, `info`, `act`, `list`, `warn`, `bug`, `err` are pre-configured, but can be overwritten by user configuration.

When using `psprint` as a dependency with custom-defined `mark`\ s, generate a custom ``PrintSpace`` object and use its ``psprint`` method as custom :printhl:`print`


.. code-block:: python
   :caption: __init__.py

   from psprint import init_print

   print = init_print('style.yml').psprint


.. note::

   Linters complain about renaming ``__builtin__.print`` by ``psprint.print``. This prevents redefinition of ``__builtins__``, but that's exactly what we want to do. To silence errors: EITHER

   - Add exception to `pylintrc <http://pylint.pycqa.org/en/latest/user_guide/run.html#command-line-options>`__ OR
   - Be gentle and import 'as `psprint`'

.. tabbed:: pylint exception

   .. code-block:: ini
      :caption: pylintrc
      :name: pylintrc

      [VARIABLES]
      redefining-builtins-modules=psprint

.. tabbed:: import

   .. code-block:: python
      :caption: safe_builtin.py
      :name: safe builtin

      from psprint import print as psprint

.. tabbed:: dependency

   .. code-block:: python
      :caption: safe_init.py

      from psprint import init_print

      psprint = init_print('style.yml').psprint



Formatted string
===================

`psfmt` :return:`return`\ s prefixed args rather than `psprint`\ ing them.



Similar to ``psprint``
------------------------------

.. code-block:: python
   :caption: psfmt.py
   :name: psfmt

   from psprint import psfmt

   fmt_str = psfmt('The Quick Brown Fox', sep='', mark='info', bland=True)
   fmt_list = psfmt('The Quick Brown Fox', mark='info', bland=True)

   print(fmt_str)
   print(*fmt_list)
   print(fmt_list)

.. code-block:: console
   :caption: output
   :name: psfmt output

   [INFORM]  The Quick Brown Fox
   [INFORM]  The Quick Brown Fox
   ['[INFORM]  The Quick Brown Fox']

.. note::

   - Without separator argument `sep`, ``psfmt`` returns a ``list`` of args, prefixed.
     With the separator, ``psfmt`` returns them as ``str``, prefixed and `sep`\ arated.
   - Here, ``print`` is ``__builtins__.print``


Useful with `__format__`
-------------------------

Get fstring to process ``mark``

.. code-block:: python
   :caption: psfmt_format.py
   :name: psfmt for repr

   from psprint import psfmt

   class MyFmtClass():
       """My Test Class with format string"""
       def __init__(self):
           self.attr = 'data\ndata line 1\ndata line 2'

       def __repr__(self) -> str:
           return f'{self:info}'

       def __str__(self) -> str:
           return f'data: {self.attr!s}'

       def __format__(self, spec):
           fmt_out = []
           for line_no, line in enumerate(str(self).split('\n')):
               if line_no == 0:
                   fmt_out.extend(psfmt(line, mark=spec))
               else:
                   fmt_out.extend(psfmt(line, mark='cont'))
           return '\n'.join(fmt_out)


   if __name__ == '__main__':
       myobj = MyFmtClass()
       print(f'{myobj:list}')
       print(repr(myobj))


.. code-block:: console
   :name: output __format__
   :caption: __format__ output

   [LIST]    data: data
             data line 1
             data line 2
   [INFORM]  data: data
             data line 1
             data line 2


Print Iterate
================
- If only one object is supplied as ``*args`` and
  it is an instance of ``Generator``, ``tuple``, ``list`` or ``dict``,
  all its elements are iterated and printed with a key-value structure.
  Prefixes are derived from keys.
- Since a ``set`` is not ordered, it is not iterated.
- For standard ``print`` behaviour of printing :magic:`__repr__`,
  pass the argument's ``repr``

.. code-block:: python
   :caption:  loop_print.py
   :name: loop print

   from psprint import print

   what_a_mess = (k for k in (
                  [],
                  {
                      'a': 1,
                      'b': [2, 'b'],
                      3: {
                          'int': 3,
                          'bool': bin(3),
                          'hex': hex(3)
                      }
                  },
                  {1, 2, 3, 4}
                  ))

   print(what_a_mess, bland=True, mark='info')

   print(repr(what_a_mess), bland=True, mark='info')


.. code-block:: console
   :caption: loop output
   :name: loop output

   [INFORM]  generator:
   [0]         list:
   [1]         dict:
   [a]           1
   [b]           list:
   [0]             2
   [1]             b
   [3]           dict:
   [int]           3
   [bool]          0b11
   [hex]           0x3
   [2]         {1, 2, 3, 4}
   [INFORM]  <generator object <genexpr> at 0x7fa4ea2194a0>

.. warning::

   This may throw a warning about `maximum prefix length <source-code-doc.html#psprint.printer.PrintSpace.pref_max>`__
