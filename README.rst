.. |af| replace:: AnyFilter

====
|af|
====

|af| is a simple base class for defining data filters. It provides the
following functionality: 

* stores configurations in JSON
* retains previous versions of configurations with user info and timestamp
* isolates custom code

The intent is to create a subclass of the ``Filter`` class in any case where custom
code has to be written. This keeps the custom code out of the primary 
workflow and codebase, and allows ``Filter`` subclasses to be inserted and toggled
as needed, while storing configurations for the filters outside the codebase
and the applications's primary database for portability and ease of maintenance.

Motivation
==========

The problem which led to this solution is the need to consume data from
end users. Usually, and especially when the users are clients, this data can
not be relied upon to meet the input specifications of your system. 

This usually leads one of these sub-optimal solutions:

* Have custom scripts to pre-process data per client
* Adding a bunch of ``if`` statements, or other similar logic to the core product
* Attempting to make transformation scripts generic enough to re-use, thus
  making them less useful for their primary purpose and harder to debug
* Hard-coding data into transformation scripts

There is often a custom transformation per client or project, 
so these solutions do not scale well.

The goals of |af| are:

* Minimize the amount of custom code in the primary codebase
* Store configurations outside the application's database in a portable format
* Allow updates of configuration data without deploying code (privileged users
  may even edit a configuration via some sort of GUI)

Benefits
========

* create pluggable data filters
* store configurations outside your application's database
* easily back up and restore configurations
* easily duplicate configurations across servers

Planned features
================

* Export and import configs
* Convert configs to and from HTML forms for easy front-end functionality
* Easily revert to a prior config
* Comprehensive unit tests

Sample usage
============

.. code-block:: python

    #!/usr/bin/env python

    """
    This is a simple example of the use of the Filter class. In this case, a
    dictionary has some keys renamed. This is a trivial example; filters
    can be as complex as required.
    """

    from anyfilter import Filter

    class NameFilter(Filter):

        """
        A filter that changes the names of dictionary keys. 

        'data' should be an iterable of dictionaries
        """

        def __call__(self, data):
            
            """
            The contents of this function are the least-important part of
            this demo. This is where you custom code will go, doing whatever
            it is you need with whatever config format and content you need.
            """

            for rec in data:

                # The config for this filter is a dictionary where the
                # key is the key name to replace, and the value is the new name.

                # update values in "data" dict
                for key, value in self.config.items():
                    if key in rec:
                        rec[value] = rec[key]
                        del rec[key]
                    
            return data

    if __name__ == '__main__':

        import os # for dealing with the environment variable manually

        # set environment variable for demo purposes
        original_envvar = os.environ.get('FILTER_CONFIG_DIR', '')
        os.environ['FILTER_CONFIG_DIR'] = '/tmp'

        # Instantiate subclass. The only argument is the uid of the subject
        # of the filter. For example, if you need to store different rules
        # per user of your site, you might use the user's primary key here.
        # This allows storage of configs per filter *and* per user.
        name_filter = NameFilter('foo')

        # Set some filter items. This normally won't be a part of the flow.
        # It's here for demo purposes. In normal usage, the config would 
        # already be set and probably rarely updated.
        name_filter.config = {
            'dog': 'canine',
            'cat': 'feline',
            'horse': 'equine',
        }

        name_filter.save_config(user='example')

        data = [{
            'cat': 'meow',
            'dog': 'woof',
            'horse': 'neigh',
            'foo': 'bar',
        }]

        print data # original
        print name_filter(data) # altered

        # Put it back like we found it, just to be good citizens.
        os.environ['FILTER_CONFIG_DIR'] = original_envvar

Sample output
=============

::

    [{'horse': 'neigh', 'foo': 'bar', 'dog': 'woof', 'cat': 'meow'}]
    [{'equine': 'neigh', 'feline': 'meow', 'canine': 'woof', 'foo': 'bar'}]
