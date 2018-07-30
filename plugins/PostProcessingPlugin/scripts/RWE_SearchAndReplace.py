# Copyright (c) 2017 Ruben Dulek
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #To perform the search and replace.

from ..Script import Script

##  Performs a search-and-replace on all g-code.
#
#   Due to technical limitations, the search can't cross the border between
#   layers.
class RWE_SearchAndReplace(Script):
    def getSettingDataString(self):
        return """{
            "name": "RWE Search and Replace",
            "key": "RWE_SearchAndReplace",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "search":
                {
                    "label": "Search",
                    "description": "All occurrences of this text will get replaced by the replacement text.",
                    "type": "str",
                    "default_value": ""
                },
                "replace":
                {
                    "label": "Replace",
                    "description": "The search text will get replaced by this text.",
                    "type": "str",
                    "default_value": ""
                },
                "is_regex":
                {
                    "label": "Use Regular Expressions",
                    "description": "When enabled, the search text will be interpreted as a regular expression.",
                    "type": "bool",
                    "default_value": false
                },
                 "start_layer":
                {
                    "label": "Layer start replace",
                    "description": "Layer to start content replacement.",
                    "type": "int",
                    "default_value": 0
                },
                 "stop_layer":
                {
                    "label": "Layer to stop replace",
                    "description": "layer that indicate to stop content replacement.",
                    "type": "int",
                    "default_value": 10000
                }
            }
        }"""

    def execute(self, data):
        search_string = self.getSettingValueByKey("search")
        search_string = search_string.replace("{NL}","\\n").replace("{CR}","\\r").replace("{TAB}","\\t").replace("{WS}","\\s").replace("{D}","\\d").replace("{W}","\\w").replace("{BS}","\\")
        if not self.getSettingValueByKey("is_regex"):
            search_string = re.escape(search_string) #Need to search for the actual string, not as a regex.
        search_regex = re.compile(search_string)

        replace_string = self.getSettingValueByKey("replace")
        replace_string = replace_string.replace("{NL}","\\n").replace("{CR}","\\r").replace("{TAB}","\\t").replace("{WS}","\\s").replace("{D}","\\d").replace("{W}","\\w").replace("{BS}","\\")
         
        startlayer = self.getSettingValueByKey("start_layer")
        stoplayer = self.getSettingValueByKey("stop_layer")
        for layer_number, layer in enumerate(data):
            if layer_number >= startlayer and layer_number < stoplayer:
                data[layer_number] = re.sub(search_regex, replace_string, layer) #Replace all.
        return data
    
       
    
