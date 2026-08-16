#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Jul 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Some description of the ``Debug`` module.
"""

#// IMPORT


#// GLOBAL VARIABLES


#// LOGIC
class MyClass:
    """
    Some class description 2.

    § title : Test - Overwrite cmd ¶
    """

    my_attribute = "Some value"
    """Some attribute description."""

    """
    The escape maker is not escaping properly. It look's like the escaping is happening to late:
        • search a valid command
        • find the command name and the provided arguments (split by : in this case)
        • search the keywords (split by = in this case)
        • escaping the remaining text
    
    § title : /§escaped text ¶
    """

    """
    It's need to create a script to extract the default registered commands and to refactor them.
    """


#// RUN
if __name__ == "__main__":
    pass
