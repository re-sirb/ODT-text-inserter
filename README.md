# ODT-text-inserter

This is a simple Python module to insert text into input fields in an odt-document without the overhead of using OpenOffice / LibreOffice / Unified Network Objects (UNO) ...


# Usage

This module can change the content of input fields in your odt-document. It is important to use unique field descriptors! (They must be entered in the *'Reference'* text box when creating the input field).
I personally haven't come across anything to the contrary, but it should be mentioned here that your odt-files have to be UTF-8 encoded for this module to work. Otherwise you would have to add an other encoding function for the strings. You can easily check this in the "manifest.xml" file (you schould see something like <?xml version="1.0" encoding="UTF-8"?>).


```python
from odt_input_fields_mod import odt_input_fields_mod as odt_mod

# this file serves only as a template and will not be modified
fields_mod = odt_mod("test.odt")

print(fields_mod.get_input_field_list())

# replace_field_text ( field_descriptor, new_Text )
fields_mod.replace_field_text(b"X", "Test-1")

#  create a new output file containing the changess
fields_mod.save_changes("out.odt")
```

Have Fun!
