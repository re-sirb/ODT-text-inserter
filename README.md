# ODT-text-inserter
This is a simple Python module to insert text into input fields in an odt-document without the overhead of using OpenOffice / LibreOffice / Unified Network Objects (UNO) ...

#Usage

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
