# stty -a
# stty -ixon
# stty ixon
# stty cols 89
# stty rows 50
#
# echo -n $'\e[8;'$(stty size |cut -d' ' -f1)';101t'  &&: 'one-hundred one (101) cols'
# echo -n $'\e[8;'$(stty size |cut -d' ' -f1)';89t'  &&: 'eighty-nine (89) cols'
#
# echo -n $'\e[8;50;89t'  # revert Terminal to a familiar Window Size
