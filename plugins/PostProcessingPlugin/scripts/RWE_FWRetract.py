# Copyright (c) 2017 Ruben Dulek
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #To perform the search and replace.

from ..Script import Script

##  Performs a search-and-replace on all g-code.
#
#   Due to technical limitations, the search can't cross the border between
#   layers.
class RWE_FWRetract(Script):
    def getSettingDataString(self):
        return """{
            "name": "RWE FW Retract 1.0.12",
            "key": "RWE_FWRetract",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "retact_travel":
                {
                    "label": "Retact travel",
                    "description": "Travel without any Extrution will be covered by G10 & G11.",
                    "type": "bool",
                    "default_value": true
                },
                "retract_mintravel":
                {
                    "label": "Min travel",
                    "description": "Minimal travel legth to retract.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 1.0
                },
                "retact_switch":
                {
                    "label": "Retact nozzle switch",
                    "description": "Nozzle switch will be covered by G10 S1 & G11.",
                    "type": "bool",
                    "default_value": true
                },
                "retract_length":
                {
                    "label": "Travel Retract length",
                    "description": "Filament legth to retract on travel. 0 := keep FW defaults",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },

                "retract_speed":
                {
                    "label": "Travel Retract speed",
                    "description": "feed speed for retract on travel. 0 := keep FW defaults",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 0.0
                },
                "switch_length":
                {
                    "label": "Switch Retract length",
                    "description": "Filament legth to retract on nozzle switch. 0 := keep FW defaults",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },

                "switch_speed":
                {
                    "label": "Switch Retract speed",
                    "description": "feed speed for retract on nozzle switch. 0 := keep FW defaults",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 0.0
                },
                "fix_single":
                {
                    "label": "Fix for Single Nozzle",
                    "description": "remove all M104 and M109 in printing layers.",
                    "type": "bool",
                    "default_value": false
                },
                "swap_tools":
                {
                    "label": "Swap extruders",
                    "description": "Swap the extruders T0 <-> T1.",
                    "type": "bool",
                    "default_value": false
                },
                "prime_athome":
                {
                    "label": "Prime after home",
                    "description": "Prime the current extruder after homing.",
                    "type": "bool",
                    "default_value": false
                },

                "zoffset":
                {
                    "label": "Z-Offset",
                    "description": "Set the Z-Axis_Offset mm. 0 := keep FW defaults",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "enable_autoretract":
                {
                    "label": "Enable Autoretract",
                    "description": "Enable Firmware Auto-Retraction. [Not Recommended]",
                    "type": "bool",
                    "default_value": false
                },
                "enable_calibration":
                {
                    "label": "Enable Callibration",
                    "description": "Enable the X,Y,Z,E callibration values.",
                    "type": "bool",
                    "default_value": false
                },
                "enable_antiresonance":
                {
                    "label": "Enable AntiResonance",
                    "description": "Enable the anti-resonance values.",
                    "type": "bool",
                    "default_value": false
                },
                "enable_abl":
                {
                    "label": "Enable ABL",
                    "description": "Enable the Auto Bed Leveling.",
                    "type": "bool",
                    "default_value": true
                }
              
            }
        }"""

    def execute(self, data):

        enable_autoretract_flag = self.getSettingValueByKey("enable_autoretract")
        enable_calibration_flag = self.getSettingValueByKey("enable_calibration")
        enable_antiresonance_flag = self.getSettingValueByKey("enable_antiresonance")
        enable_abl_flag = self.getSettingValueByKey("enable_abl")
                        
        fix_single_flag = self.getSettingValueByKey("fix_single")
        retact_travel_flag = self.getSettingValueByKey("retact_travel")
        retract_mintravel_val = self.getSettingValueByKey("retract_mintravel")
        retact_switch_flag = self.getSettingValueByKey("retact_switch")
        retract_length_val = self.getSettingValueByKey("retract_length")
        retract_speed_val = self.getSettingValueByKey("retract_speed")
        switch_length_val = self.getSettingValueByKey("switch_length")
        switch_speed_val = self.getSettingValueByKey("switch_speed")

        swap_tools_flag = self.getSettingValueByKey("swap_tools")
        prime_athome_flag = self.getSettingValueByKey("prime_athome")
        zoffset_val = self.getSettingValueByKey("zoffset")

        fix_m104_regex = re.compile("M104")
        fix_m109_regex = re.compile("M109")

        find_endgcode_regex = re.compile("\n\s*;\s*End of Gcode")

        find_t0_regex = re.compile("\nT0")
        replace_t0_string = "\nG10 S1\nT0\nG11"
        replace_xt0_string = "\nM104 S200\nM109 S200\nG10 S1\nT0\nG11"

        find_t1_regex = re.compile("\nT1")
        replace_t1_string = "\nG10 S1\nT1\nG11 ;"
        replace_xt1_string = "\nM104 S200\nM109 S200\nG10 S1\nT1\nG11"

        find_ta_regex = re.compile("\nTa")
        find_home_regex = re.compile("\nG28")
        find_zoffset_regex = re.compile("\n[;\s]*M851")

        find_autoretract_regex = re.compile("\n\s*M209\s")
        find_noautoretract_regex = re.compile("\n\s*;\s*M209\s")
        replace_autoretract_string = "\n; M209 "
        replace_noautoretract_string = "\nM209 "

        find_calibration_regex = re.compile("\n\s*M92\s")
        find_nocalibration_regex = re.compile("\n\s*;\s*M92\s")
        replace_calibration_string = "\n; M92 "
        replace_nocalibration_string = "\nM92 "

        find_abl_regex = re.compile("\n\s*G29")
        find_noabl_regex = re.compile("\n\s*;\s*G29")
        replace_abl_string = "\n; G29"
        replace_noabl_string = "\nG29"

        find_antiresonance_regex = re.compile("\n\s*(M20[135]\s)")
        find_noantiresonance_regex = re.compile("\n\s*;\s*(M20[135]\s)")
        replace_antiresonance_string = r"\n; \1"
        replace_noantiresonance_string = r"\n\1"

        for layer_number, layer in enumerate(data):

            if layer_number >= 2:
                if fix_single_flag:
                    if layer.contains("; end of g-code"):
                        layer = find_endgcode_regex.sub("\nM104 S0\nM104 T1 S0\n;End of Gcode", layer)                    
                    elif find_endgcode_regex.match(layer) is None:
                        layer = fix_m104_regex.sub( "; M104", layer)
                        layer = fix_m109_regex.sub( "; M109", layer)
                    else:
                        layer = find_endgcode_regex.sub("\nM104 S0\nM104 T1 S0\n;End of Gcode", layer)
                    
                if retact_switch_flag:
                    layer = find_t0_regex.sub( replace_t0_string, layer)
                    layer = find_t1_regex.sub( replace_t1_string, layer)
                   
            else:
                if retact_switch_flag:
                    layer = find_t0_regex.sub( replace_xt0_string, layer)
                    layer = find_t1_regex.sub( replace_xt1_string, layer)           
                if swap_tools_flag:
                    layer = find_t0_regex.sub( "\nTa", layer)
                    layer = find_t1_regex.sub( "\nT0", layer)
                    layer = find_ta_regex.sub( "\nT1", layer)
                if prime_athome_flag:
                    layer = find_home_regex.sub( "\nG28\nG0 X0 Y0 Z15 F1200\nG92 E-35\nG1 E0 F200", layer)
                if zoffset_val != 0.0 :
                    layer = find_zoffset_regex.sub( "\nM851 Z{0};".format(zoffset_val), layer)

                if enable_calibration_flag:
                    if find_nocalibration_regex.match(layer):
                        layer =find_nocalibration_regex.sub(replace_nocalibration_string,layer)
                else:
                    if find_calibration_regex.match(layer):
                        layer =find_calibration_regex.sub(replace_calibration_string,layer)


                if enable_abl_flag:
                    if find_noabl_regex.match(layer):
                        layer =find_noabl_regex.sub(replace_noabl_string,layer)
                else:
                    if find_abl_regex.match(layer):
                        layer =find_abl_regex.sub(replace_abl_string,layer)

                if enable_antiresonance_flag:
                    if find_noantiresonance_regex.match(layer):
                        layer =find_noantiresonance_regex.sub(replace_noantiresonance_string,layer)
                else:
                    if find_antiresonance_regex.match(layer):
                        layer =find_antiresonance_regex.sub(replace_antiresonance_string,layer)

            if enable_autoretract_flag:
                if find_noautoretract_regex.match(layer):
                    layer =find_noautoretract_regex.sub(replace_noautoretract_string,layer)
            else:
                if find_autoretract_regex.match(layer):
                    layer =find_autoretract_regex.sub(replace_autoretract_string,layer)

            if retact_travel_flag:
                layer = layer
            data[layer_number] = layer
        return data
    
       
    
