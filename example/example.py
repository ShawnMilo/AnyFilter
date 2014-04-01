#!/usr/bin/env python

"""
This is a simple example of the use of the Filter class. In this case, a
dictionary has some keys renamed.
"""

from anyfilter import Filter

class NameFilter(Filter):

    """
    A filter that changes the names of dictionary keys.

    'data' should be an iterable of dictionaries
    """

    def __call__(self, data):

        for rec in data:

            # The config for this filter is a dictionary where the
            # key is the key name to replace, and the value is the new name.

            # update values in "data" dict
            for key, value in self.config.items():
                if key in rec:
                    rec[value] = rec[key]
                    del rec[key]

        return data

def main():

    """
    Sample usage.
    """

    import os # for dealing with the environment variable manually

    # set environment variable for demo purposes
    original_envvar = os.environ.get('FILTER_CONFIG_DIR', '')
    os.environ['FILTER_CONFIG_DIR'] = '/tmp'

    # instantiate subclass
    name_filter = NameFilter('foo')

    # Set some filter items. This will only update the config the first time
    # this is run.
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

if __name__ == '__main__':

    main()
