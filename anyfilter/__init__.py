#!/usr/bin/env python

"""
This is the file containing the base Filter class. It should be subclassed
for any filtering needs. See example.py in this folder for a simple use-case.
"""

from datetime import datetime
import os
import json

class Filter(object):

    def __init__(self, uid):

        """
        Initialize the filter. This requires a UID which is used to determine
        which configuration file is to be used. This also requires that the
        FILTER_CONFIG_DIR environment variable be set.

        If the config file is successfully located, it is loaded into
        the namespace as self.config for use by the __call__ method.

        To use the Filter class, subclass it and define a __call__ method.
        The __call__ method should accept an iterable of dictionaries and
        return the same iterable of dictionaries, potentially altered.
        """

        # test that FILTER_CONFIG_DIR exists and is a valid path.
        filter_dir = os.environ.get('FILTER_CONFIG_DIR', '')
        if filter_dir == '':
            raise ValueError("FILTER_CONFIG_DIR must be set.")
        if not os.path.isdir(filter_dir):
            raise ValueError("FILTER_CONFIG_DIR is invalid.")
            
        # this is the key to use to find the config
        config_key = "{0}_{1}.json".format(self.__class__.__name__, uid)
        self.config_file = os.path.join(filter_dir, config_key)

        self.config = self.get_config()

    def get_raw_config(self):

        """
        Grab full JSON file, return empty list if not there.
        """

        if os.path.isfile(self.config_file):

            with open(self.config_file, 'r') as raw:
                raw_json = raw.read()
                try:
                    configs = json.loads(raw_json)
                except ValueError as ex:
                    # config empty or corrupted; return default
                    return []

            return configs

        else:
            return [] 

    def get_config(self):

        """
        Get config dict for instance.
        """

        config_list = self.get_raw_config()

        if len(config_list) == 0:
            config = {}
        else:
            # the config_dict has three keys: 
            #     config: actual config dict
            #     created_date: date config saved
            #     user: user who saved config

            config_list.sort(key=lambda x: x['created_date'])
            config_dict = config_list[-1]
            config = config_dict['config']

        return config

    def save_config(self, user):

        """
        Save the config if it's been changed, or do nothing.
        """

        old_config = self.get_config()

        if self.config == old_config:
            return True

        raw = self.get_raw_config()        

        raw.append({
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': user,
            'config': self.config,
        })

        # write updated config
        with open(self.config_file, 'w') as output:
            output.write(json.dumps(raw))

    def update_config(self, data, user):

        """
        Accepts a HTML form post data and updates the config dict
        using the values parsed from it.
        """

        # This class's name; used to parse POST data.
        class_name = self.__class__.__name__

        # Extract just the keys from the POST that pertain to this filter.
        raw = filter(lambda x: x.startswith(class_name), data)

        # Turn key/value pairs into config dict.
        config = {}
        for x in range(1, (len(raw) / 2) + 1):
            key = data["{0}_key{1}".format(class_name, x)].strip()
            val = data["{0}_val{1}".format(class_name, x)].strip()

            # Ignore empty data.
            if key == '' or val == '':
                continue

            config[key] = val

        self.config = config
        self.save_config(user=user)
