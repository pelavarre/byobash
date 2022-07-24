# byobash > macos

fifteen steps

1

download:  https://github.com/pelavarre/byobash/archive/refs/heads/main.zip

macOS Safari will bring it to you as:  ~/Downloads/byobash-main.zip
<br>
and unzip it for you

2

it should just work

inside the unzipped main folder you'll find our "macos" Folder of Button Files

the Button Files should appear inside your Finder < View > As Icons (⌘1),
laid out like so =>

      i      pi  7  8  9  /
     OVER    e   4  5  6  *
            POW  1  2  3  -
    CLEAR    √   0  .  ,  +

    icons/  README.md  buttonfile.py

3

if you've got the correct layout, but
all the Icons are blank on the Button Files, then i do much wish i knew why,
but i dunno how to make it stop going wrong on you.
i only know how you fix it

how you fix it is

3.1 pick some Button File to fix, such as your 'π' Pi Button File
<br>
3.2 try a Control+Click on that Button File and choose Get Info
<br>
3.3 Get Info will show you the broken Icon in its upper left
<br>
3.4 drag the correct Icon in to place on top of Get Info, from the 'icons/' Folder

you'll need to fix all 19 buttons by hand, one by one,
but Before you agree work that hard, let's show you that your 'π' Pi Button File works

4

Double-Click through the 'π' Pi Button File

when it works, you will see it create a file named '3.142'

but the first time you try Double-Click'ing it,
macOS will block you,
and tell you it's from an Unidentified Developer,
and you'll hit Ok and then you're slap back where you started, ugh

the first time through,
you have to Control+Click on the Button File and choose Open With > Terminal > Open

that's how you get your first '3.142' file

the Finder gave you the Open With > Terminal > Open as a top option,
because we end each of the Button File Names
with the magic Apple File Extension:  .command

5

your macOS Terminal may be flooding your Screen with leftover Windows:
one leftover Window for each time you Double-Click through a Button File

if that's happening to you, then the fix is

    Finder > Go > Utilities (⇧⌘U)
        > Terminal > Preferences > Shell
            > When The Shell Exits = Close If The Shell Exited Cleanly

who was littering your Screen with one more leftover Window,
as often as you pressed a File Button?
it was the "Don't Close The Window" choice

6

once it works, you can make it prettier

you've already fixed the Icon,
but if your Button File is still labeling itself as 'π.command', you can fix that too

go turn on its Control+Click > Get Info > Name & Extension > Hide Extension

this will get it to label itself as 'π'

except that you do also have to turn off
Finder > Preferences > Advanced > Show All Filename Extensions,
if you had turned on that wrinkle - that wrinkle is off by default

7

ok fun you've made 1 Button File work

but to make all 19 Button Files work
you're going to have repeat all these steps another eighteen times

i'm sorry, this is wrong, and
i don't know a good way to make Apple stop hassling you like this

someone should teach me to push these Button Files
out through the Apple macOS App Store, then they really could just plain work

8

me, myself, instead of downloading the Zip,
i tell Homebrew to give me Git inside my macOS Sh Terminal
and then i

    git clone https://github.com/pelavarre/byobash.git
    cd byobash/

that move makes it easy for me to receive Software Updates

    git fetch
    git rebase

this early in the game, you'll want Software Updates,
because we've got plenty of troublesome bugs haunting this work

9

tell us if you succeed?

this is like the Model T days of the Ford motor car

to make your first Button Files work today,
you really have to care, you have to be willing to fiddle

maybe somebody good out there will make it easier for all of us,
or teach me how to make it easier

10

once you have several Button Files working, then you can combine them in demos

like you can get to 'maths.tau' from 'maths.pi'

    Clear  π  2  *

to see what's going on, you'll want to open up another Finder Window,
so that you can see the Finder > View > As List (⌘2) of the 'macos' Folder,
and sort by Last Modified

these are the Files that are Numbers that you calculate with

11

you press the Button Files,
back in your first Finder Window of Finder > View > As Icons (⌘1),
and you can see they create and destroy Number Files

like you can produce the Fibonacci Numbers

    Clear  1 , 2  Over Over +  Over Over +  ...

when you produce them that way,
the two strikes of the Over Button File gives you
two duplicate copies of the two Numbers you started with

    2~
    1~
    2
    1

then the one strike of the + Button File adds the top two Number Files,
and you end up with

    3
    2
    1

as you keep going and going, you get up to

    21
    13
    8
    5
    3
    2
    1

and beyond

12

when things don't just work for you, i'll be curious to see your Sh Terminal

    sw_vers
    python3 -V

me, i've got Oct/2021 Monterey macOS 12 with its Feb/2020 Python 3.8.2,
except usually instead i run an upgraded Jun/2022 Python 3.10.5,
that i took from Python Org > Downloads

13

in early versions
+ the Clear Button File only worked inside Git Clones
+ the , Button File only worked well when pressed after a Digit Button File
+ the Over / * - + Button Files only worked well with 2 or more Number Files present
+ the √ Button File was missing

14

after you download something through Safari,
you can visit Safari > Preferences > Websites > Downloads
and choose Ask or Deny for each website, in place of Allow

those Ask and Deny choices slow or stop more downloads from coming at you later,
wrongly neglecting to wait for your explicit invitation

15

we did get it wrong if we gave you this message
while this much macOS reconfiguration is still too expensive for you

please check back a year from now

we'll move faster if you tell us that you're waiting on our progress

> open https://twitter.com/intent/tweet?text=@PELaVarre


## Copied from

Posted into:  https://github.com/pelavarre/byobash/blob/main/macos#readme
<br>
Copied from:  git clone https://github.com/pelavarre/byobash.git
