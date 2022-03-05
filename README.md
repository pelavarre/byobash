# byobash
Type a command line into Bash, but end its verb in ".py" to go with your own defaults and options

## Demo

Got preferences?

Got your own correct opinion on wich defaults, options, examples, and help lines should come to you now, from your own tools inside Bash?

Look here, you can afford to spell out your opinion quickly in simple code. You can roll your own simple accomodations in the workplace, while your workplace is a Shell in a Terminal, such as Linux Bash or Mac Zsh. You can curate the fixes yourself, keep some fixes secret, crowd-source the rest.

For example, you don't have to back off resignedly and put up with such talk-to-the-hand nonsense as

    $ cp
    cp: missing file operand
    Try 'cp --help' for more information
    + exit 1
    $

Telling "cp" to stop forcing you to spell out all its options and arguments looks like this

    $ touch file
    $ cp.py
    + cp -ipR file file~2~
    $

    $ mkdir files
    $ cp.py
    + cp -ipR files/ files~2~/
    $

As another example, telling "ssh" to give you the TL;DR of its Man Page looks like this

    $ man ssh |wc -l
    922
    $ 
    $ ssh.py --h |wc -l
    21
    $ 

And telling "ssh" to give you the better examples looks like this
  
    $ ssh.py --h
    ...
    ssh -t localhost 'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
    ...
    $

You can learn to press <Dot> <Tab> <Return> in place of <Return>, as often as you need a tool to wake up and welcome you competently into your own everyday work. Work once briefly to retune your Bash to receive this signal well, and you'll have Bash itself treating you more kindly, as often you ask for it.

The year 1972 was a long time ago now. You actually don't have to keep it in place to misrule over you.

## Basic install

Add your new executable Python files into your Shell's Path, through some such procedure as

    cd ~/Public/
    git clone https://github.com/pelavarre/byobash.git
    cd byobash/bin/
    export PATH="${PATH:+$PATH:}$PWD"

Or copy the files into some Dir you already keep in your Shell's Path, such as your own "$HOME/bin" if you keep up that tradition.

Back in the day, you had to exit and relaunch your Shell to pick up new executable files, but nowadays almost nobody has to work through that chore manually themselves.

## Advanced install

Your Shell shoves extra hard against you correcting its "builtin" commands.
  
For example, the Linux Bash Shell defines no API to let you fix its "cd" command.
  
To define 'cd.py' to mean fix what's wrong with 'cd', you have to define 'cd.py' as a Shell Alias of a baroque Shell Function that passes your input through a 'mktemp' file, because reasons

    cd ~/Public/
    git clone https://github.com/pelavarre/byobash.git
    source ~/Public/byobash/bin/bashrc.source

It works, but it's not pretty, because Linux Bash and Mac Zsh don't yet do their half of this work. Comments in the source spell out exactly which tests your Shell will fail if you try to do this more simply, before more people show up to teach your Shell to properly welcome such corrections.
