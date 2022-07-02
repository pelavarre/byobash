# byobash

Type the first Word of any Command Line into your Terminal Shell, and then

1 ) press the 2 keys \<Dot\> \<Tab\> before \<Return\> to show **your own examples** at "verb.py " or

2 ) press the 5 keys \<Dot\> \<Tab\> \<Dash\> \<Dash\> \<H\> before \<Return\> to show **your own notes** at "verb.py --h", or

3 ) press the 4 keys \<Dot\> \<Tab\> \<Dash\> \<Dash\> \<H\> before \<Return\> to run **your own corrections to defaults and behavior** at "verb.py --"

You pressing those two leading 2 keys \<Dot\> \<Tab\> will tell your Terminal to immediately type out the ".py " part for you,
after you set up your Sh Path in this way

## Motivation

Got preferences?

**Got your own correct opinion of
which defaults, options, examples, and help lines
should come work with you now**, for your tools and mine, inside of your Terminal Shell?

Look here, yes you can quickly easily code and ship your own opinion.

You can roll your own good cheap strong accomodations of you in the workplace,
while you work inside some such Terminal Shell as Linux Bash, Mac Zsh, or a Gmail GShell.
You can curate the fixes yourself, keep some fixes secret, crowd-source the rest

## Demo

For example, you can type S S H Dot Tab Return
to get Ssh to give you **better examples**

    $ ssh.py
    ...
    ssh -t localhost 'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
    ...
    $

Likewise, you can type S S H Dot Tab Dash Dash Return
to get Ssh to give you **the TL;DR of its voluminous Man Page**

    $ man ssh |wc -l
    922
    $
    $ ssh.py --h |wc -l
    21
    $

Get it?
The year 1972 was a long time ago now
- you don't actually have to keep it in place in misrule over you

Like you don't have to back off resignedly and
put up with such talk-to-the-hand nonsense as

    $ cp
    cp: missing file operand
    Try 'cp --help' for more information
    + exit 1
    $

Telling Cp to **stop forcing you to spell out all its options and arguments for us**
can look like this

    $ touch file
    $ cp.py --
    + cp -ip file file~
    $

    $ mkdir files/
    $ cp.py --
    + cp -ipR files/ files~/
    $

## Basic install

**Copy the Py files you want into your Shell Path**

Quickest is for you to patch our whole Dir into the far end of your Sh Path, like so

    cd ~/Public/
    git clone https://github.com/pelavarre/byobash.git
    export PATH="${PATH:+$PATH:}$PWD/byobash/bin"

As often as you do know your Sh Path isn't empty, you can say this more simply, like so

    export PATH="$PATH:$HOME/Public/byobash/bin"

You don't need to exit and relaunch your Shell to make these Py files work for you,
just dropping these Py files into your Shell Path is enough

But **when you do want your Shell to make these Py files work for you
as often as you open up a new Terminal window**,
then you can patch your '\~/.bashrc' or '\~/.zshrc' configuration of your Shell, like so

    export PATH="${PATH:+$PATH:}:$HOME/Public/byobash/bin"

If you take our files in a la carte, one by one, then for now you'll also need to take in a copy of our non-executable "byotools.py" file.
If instead you want to embed a copy of that file into the one file you're taking, then you'll have to change one sourceline of it

    - import byotools as byo
    + import __main__ as byo


## Advanced install

Odds on **you've already told your Shell to give some permissions
only to the commands you've placed inside Sh Process Memory**,
while not also giving equally broad permissions to
commands coded more separately, as Files outside of Sh Process Memory.

For example, your 'cd' will change your Working Dir, but your '/usr/bin/cd' won't

    % which -a cd
    cd: shell built-in command
    /usr/bin/cd
    %

So then
if you do want 'cd.py' to change your Sh Working Dir,
if you do want 'echo.py' to fetch your Sh '$?' before your Sh '$?' clears itself,
you've got to install them in some special way, such as

    function cd.py () {
      if [ "$#" = 1 ] && [ "$1" = "--" ]; then
        'cd' ~/Desktop && (dirs -p |head -1)
      else
        'cd' "$(~/Public/byobash/bin/cd.py $@)" && (dirs -p |head -1)
      fi
    }

When you forget how this works, 'bin/cd.py --' will remind you, because there's no other way for it to help you then.
Ditto, 'bin/echo.py --' will tell you how to install it forcefully enough to let it fetch your Sh '$?' before your Sh '$?' clears itself

Technical Note: the specific example of '/usr/bin/cd' arrives by default inside macOS, as part of Apple's effort to follow Posix, but few Linuxes bother to conform so well there

## Copied from

Posted into:  https://github.com/pelavarre/byobash#readme
Copied from:  git clone https://github.com/pelavarre/byobash.git
