# byobash

Type a command line into Bash,
but end the verb in ".py" to get your own defaults and options,
and end the verb in ".py --" to get your own corrections to its meaning

Odds on you'll see the verb end in ".py"
if you try pressing  \<Dot\> \<Tab\> \<Return\> in place of \<Return\>,
so you shouldn't have to press the P and the Y

## Demo

Got preferences?

Got your own correct opinion on which defaults, options, examples, and help lines
should come to you now, from your own tools inside Bash?

Look, here you can quickly easily code your opinion.
You can roll your own simple accomodations of you in the workplace,
while your workplace is a Shell in a Terminal,
such as Linux Bash or Mac Zsh or GMail's GCloud Bash inside your Browser.
You can curate the fixes yourself, keep some fixes secret, crowd-source the rest

For example, you can type S S H and then Dot Tab Return
to get Ssh to give you better examples

    $ ssh.py
    ssh.py --help  &&: show this help message and exit
    ssh -t localhost 'cd /usr/bin/ && bash -i'  &&: Ssh to your choice of Cd
    ...
    $

Likewise, you can type S S H Space Dash Dash H Return
to get Ssh to give you the TL;DR of its voluminous Man Page

    $ man ssh |wc -l
    922
    $
    $ ssh.py --h |wc -l
    21
    $

The year 1972 was a long time ago now
- you don't actually have to keep it in place in misrule over you

For example, iyou don't have to back off resignedly and
put up with such talk-to-the-hand nonsense as

    $ cp
    cp: missing file operand
    Try 'cp --help' for more information
    + exit 1
    $

Telling Cp to stop forcing you to spell out all its options and arguments for us
can look like this

    $ touch file
    $ cp.py --
    + cp -ip file file~
    $

    $ mkdir files
    $ cp.py --
    + cp -ipR files/ files~/
    $

## Basic install

Copy the Py files you want into your Shell Path

Like you can patch in our whole Dir into your Path, like so

    cd ~/Public/
    git clone https://github.com/pelavarre/byobash.git
    export PATH="${PATH:+$PATH:}$PWD/byobash/bin"

When you do know your Shell Path isn't empty, you can say this more simply, like so

    export PATH="$PATH:$HOME/Public/byobash/bin"

You don't need to exit and relaunch your Shell to make these Py files work for you,
just dropping these Py files into your Shell Path is enough

When you want your Shell to make these Py files work for you
as often as you open up a new Terminal window,
you can patch your '~/.bashrc' or '~/.zshrc' configuration of your Shell, like so

    export PATH="${PATH:+$PATH:}:$HOME/Public/byobash/bin"

## Advanced install

Odds on you've told your Shell to give some permissions
only to commands coded inside Process Memory,
not also to commands coded as Files outside of Process Memory.

For example, your 'cd' will change your Working Dir, but your '/usr/bin/cd' won't

    % which -a cd
    cd: shell built-in command
    /usr/bin/cd
    %

So then if you then do want 'cd.py' to change your Working Dir,
you've got to install 'cd.py' in some special way, such as

    function cd.py () { cd "$(~/Public/pybashish/bin/cd.py bin)"; }

## Copied from

Copied from:  git clone https://github.com/pelavarre/pybashish.git
