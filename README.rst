.. |af| replace:: AnyFilter

|af| is a simple base class for defining data filters. It provides the
following functionality: 

* stores configurations in JSON
* retains previous versions of configurations with user info and timestamp

The intent is to create a subclass of the ``Filter`` class in any case where custom
code has to be written. This keeps the custom code out of the primary 
workflow and allows ``Filter`` subclasses to be inserted and toggled
as needed.

Benefits of using |af|:

* store configurations outside your application's database
* easily backup and restore configurations
* easily duplicate configurations across servers

Sample usage:

.. literalinclude:: example/example.py

Sample output::

    [{'horse': 'neigh', 'foo': 'bar', 'dog': 'woof', 'cat': 'meow'}]
    [{'equine': 'neigh', 'feline': 'meow', 'canine': 'woof', 'foo': 'bar'}]
