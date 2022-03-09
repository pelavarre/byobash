# byobash
Type a command line into Bash,
but end its verb in ".py" to go with your own defaults and options

## Demo

Got preferences?

Got your own correct opinion on which defaults, options, examples, and help lines
should come to you now, from your own tools inside Bash?

Look here, you can afford to spell out your opinion quickly in simple code.
You can roll your own simple accomodations in the workplace,
while your workplace is a Shell in a Terminal, such as Linux Bash or Mac Zsh.
You can curate the fixes yourself, keep some fixes secret, crowd-source the rest.

For example, you don't have to back off resignedly and
put up with such talk-to-the-hand nonsense as

    $ cp
    cp: missing file operand
    Try 'cp --help' for more information
    + exit 1
    $

Telling "cp" to stop forcing you to spell out all its options and arguments
looks like this

    $ touch file
    $ cp.py
    + cp -ipR file file~2~
    $

    $ mkdir files
    $ cp.py
    + cp -ipR files/ files~2~/
    $

As another example, telling "ssh" to give you the TL;DR of its Man Page
looks like this

    $ man ssh |wc -l
    922
    $
    $ ssh.py --h |wc -l
    21
    $

And telling "ssh" to give you the better examples
looks like this

    $ ssh.py --h
    ...
    ssh -t localhost 'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
    ...
    $

You can learn to press <Dot> <Tab> <Return> in place of <Return>,
as often as you need a tool to wake up and welcome you competently
into your own everyday work.
Work once briefly to retune your Bash to receive this signal well, and
you'll have Bash itself treating you more kindly, as often you ask for it.

The year 1972 was a long time ago now.
You actually don't have to keep it in place to misrule over you.

## Basic install

Copy the Py files you want into your Shell Path

Like you can patch in the whole directory of ByoBash Py files like so

    cd ~/Public/
    git clone https://github.com/pelavarre/byobash.git
    export PATH="${PATH:+$PATH:}$PWD/byobash/bin"

Any time you know your Shell Path isn't empty, you can get by instead with just

    export PATH="$PATH:$HOME/Public/byobash/bin"

Regrettably,
most of these Py files run well only if you copy the "byotools.py" file in with them.
Tell me if this headache bothers you, we have ways to fix it.

You probably don't need to
exit and relaunch your Shell to pick up new executable files,
just dropping them into your Shell Path should be enough.

## Advanced install

Your Shell shoves extra hard against you correcting its "builtin" commands.

For example, the Linux Bash Shell defines no API to let you fix its "cd" command.

To define 'cd.py' to mean fix what's wrong with 'cd',
you have to define 'cd.py' as a Shell Alias

    cd ~/Public/
    git clone https://github.com/pelavarre/byobash.git
    source <(~/Public/byobash/bin/cat_bashrc_source.py)

This works, but it's not pretty, because
Linux Bash and Mac Zsh don't yet do their half of this work.
Comments in the source spell out exactly which tests your Shell will fail
if you try to do this more simply,
before more people show up to teach your Shell to properly welcome such interventions.

## Prior work

The tech here first came online buried deep inside of
GitHub > PELaVarre > [PyBashish](https://github.com/pelavarre/pybashish)
