# Mac Expand rudely takes a Parm of '-' as meaning read a File named '-'

# echo $'\xCF\x80' |cat -tv |expand  # expand: stdin: Illegal byte sequence
# echo $'\xCF\x4D\x2D' |expand  # expand: stdin: Illegal byte sequence

# print("\N{Greek Small Letter Pi}".encode())  # b'\xcf\x80'
# print("\N{No-Break Space}".encode())  # b'\xc2\xa0'

# quirks:
#   goes well with:  unexpand.py

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/expand.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
