# byobash > macos

contents

1 Download<br>
2 It should just work<br>
3 Drag Icons into place<br>
4 Watch it work<br>
5 Stop Litter<br>
6 Hide Filename Extensions<br>
7 Drag Nineteen Icons into place, now and again<br>
8 Subscribe to Software Upgrades, free of charge<br>
9 Catch us up<br>
10 Kick more Buttons into gear<br>
11 Pile up Stacks of Number Files<br>
12 Give us bugs<br>
13 Remember the good times<br>
14 Block extra downloads<br>
15 Hunt up Easter Eggs<br>
16 Wish us well<br>


sixteen steps


## 1 Download

download:  https://github.com/pelavarre/byobash/archive/refs/heads/main.zip

macOS Safari will bring it to you as:  ~/Downloads/byobash-main.zip
<br>
and unzip it for you


## 2 It should just work

inside the unzipped main folder you'll find
our "macos" Calculator Folder of Button Files

the Button Files should appear inside your Finder < View > As Icons (⌘1),
laid out like so =>

      i      π   7  8  9  /
     OVER    e   4  5  6  *
            Y↑X  1  2  3  -
    CLEAR    √   0  .  ,  +

    icons/  README.md  buttonfile.py


## 3 Drag Icons into place

if you've got the correct layout,
but all the Icons are blank on the Button Files,
then i do much wish i knew why, but i dunno how to make it stop going wrong on you

i only know how you fix it

how you fix it is

3.1 pick some Button File to fix, such as your π Pi Button File
<br>
3.2 try a Control+Click on that Button File and choose Get Info
<br>
3.3 Get Info will show you the wrongly blanked-out Icon in its upper left
<br>
3.4 find the correct Icon in our 'macos/icons/' Folder,
and drag it into place on top of the blanked-out Icon inside Get Info

well ouch, you'll need to fix all 19 buttons by hand, one by one by one

but Before you agree work that hard, let's show you that your π Pi Button File works


## 4 Watch it work

Double-Click through your π Pi Button File

when it works, you will see it create a Number File named 3.142

but the first time you try Double-Click'ing your π Pi Button File,
macOS will block you,
and tell you it's from an Unidentified Developer,
and you'll hit Ok and then you're slap back where you started, ugh

this first time through,
you have to Control+Click on the Button File and choose Open With > Terminal > Open

that's how you get your first 3.142 Number File

the Finder gave you the Open With > Terminal > Open as a top option,
because we end each of the Button File Names
with the magic Apple File Extension:  .command


## 5 Stop Litter

next,
your macOS Terminal may be flooding your Screen with leftover Windows:
one leftover Window for each time you Double-Click through a Button File

if that's happening to you, then the fix is

    Finder > Go > Utilities (⇧⌘U)
        > Terminal > Preferences > Shell
            > When The Shell Exits = Close If The Shell Exited Cleanly

we do know who was wrongly littering your Screen with one more leftover Window,
as often as you clicked through a Button File -
it was the "Don't Close The Window" choice there


## 6 Hide Filename Extensions

once it works, next you can make it prettier

like you've already fixed the Icon,
but if your Button File is still labeling itself as 'π.command', you can fix that too

go turn on its Control+Click > Get Info > Name & Extension > Hide Extension

this will get it to label itself as 'π'

except maybe first you have to go turn off
Finder > Preferences > Advanced > Show All Filename Extensions -
that wrinkle is off by default, but maybe you turned it on a while back,
out of a misplaced love for the Microsoft Windows experience?


## 7 Drag Nineteen Icons into place, now and again

ok fun you've made 1 Button File work

but to make all 19 Button Files work
you're going to have repeat all these steps another 18 times

i'm sorry, this is wrong, but
i haven't yet found a good way to make Apple stop hassling you like this

someone should teach me to push these Button Files
out through the Apple macOS App Store, then they really could just plain work

and it's worse than you know,
some macOS Software Upgrades run through and blank all your Icons,
and then you have to come back and set them all up again

this happened to me in Aug/2022, in Apple's Disruptive Upgrade
to macOS Monterey 12.5 from 12.4


## 8 Subscribe to Software Upgrades, free of charge

to set yourself up to take Software Upgrades from us without blanking your Icons,
you can install "Git", which is the most popular Software Upgrade Tool nowadays

certainly, myself, instead of downloading the Zip,
i tell Homebrew to give me Git inside my macOS Sh Terminal
and then i

    git clone https://github.com/pelavarre/byobash.git
    cd byobash/

that move makes it easy for me to receive Software Updates,
as easy as typing out two Lines of chat

    git fetch
    git rebase

this early in the game, you might want more frequent Software Updates -
new features and bugs have been coming fast and often


## 9 Catch us up

tell us if you succeed?

this is like the Model T days of the Ford Motor Car

to make your first macOS Button Files work today,
you really have to care, you have to be willing to fiddle

maybe somebody good out there will make it easier for all of us,
or teach me how to make it easier

somebody could pop up and solve Linux and Windows too, not just macOS where it's easier


## 10 Kick more Buttons into gear

once you have several Button Files working, then you can combine them in demos

like you can get to 'maths.tau' from 'maths.pi'

    Clear  π  2  *

to see what's going on, you might want to open up another Finder Window,
so that you can see the Finder > View > As List (⌘2) of the 'macos' Folder,
and sort by Last Modified

these are the Files that are the Number Files that you're calculating with


## 11 Pile up Stacks of Number Files

when you click through a Button File,
you can see they create and destroy Number Files
in your first Finder Window of Finder > View > As Icons (⌘1) too

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


## 12 Give us bugs

when things don't just work for you, i'd be curious to see your Sh Terminal

    sw_vers
    python3 -V

me, i've got Oct/2021 Monterey macOS 12 with its Feb/2020 Python 3.8.2,
except for me usually i run an upgraded Jun/2022 Python 3.10.5,
that i took from Python Org > Downloads


## 13 Remember the good times

in early versions
+ the Clear Button File only worked inside Git Clones
+ the , Button File only worked well when pressed after a Digit Button File
+ the Over / * - + Button Files only worked well with 2 or more Number Files present
+ the √ and Y↑X Button Files were missing
+ Button Files pressed after . or after . , didn't work so differently as they do now
+ pressing 2 √ gave you just 0.707, not -0.707 0.707 like it does now
+ pressing 0 √ gave you just 0, not 0x0 0 like it does now


## 14 Block extra downloads

after you download something through Safari,
you can go back and visit Safari > Preferences > Websites > Downloads
and choose Ask or Deny for each website, in place of Allow

those Ask and Deny choices slow or stop more downloads from coming at you later,
wrongly neglecting to wait for your explicit invitation

you working through the download of our "byobash-main.zip"
will have opened you up to downloading all of GitHub,
which might often be more than you want


## 15 Hunt up Easter Eggs

this Calculator Folder is a playground, in which we've hidden dozens of Easter Eggs

as the faces of the Button Files, you've been looking at

      i      π   7  8  9  y/x
     yxy     e   4  5  6  y*x
            y↑x  1  2  3  y-x
    clear    √   0  .  ,  y+x

sure you can run your Folder entirely inside this small world

    1 2 ,  # 12
    1 2 , 3 4 +  # 46
    π 2 *  # 6.283 τ Tau
    - 3 . 2 e - 1 , 1 0 *  # 32

but Easter Eggs are hiding in the corners

we hid three Easter Eggs inside the / Slash Button =>

    1 0 /  # Inf
    0 1 -  # -Inf
    0 0 /  # NaN

and pressing Pi after typing a Digit undoes it,
like the Delete Key on a Mac Keyboard

and after Clear or , Comma,
pressing the . Dot Button
opens up the 2nd Folder of visually identical Button Files, and
we've taught 13 Buttons to work differently there

    real,imag  log10  7   8   9    div
        yx       ln   4   5   6    mod
               logyx  1   2   3    neg
      dropx     log2  0  2nd 3rd   pos

and 1 Dot Slash splits an ordinary Python Float into Int and Frac Float

and after Clear or , Comma,
pressing the . Dot Button and then the , Comma Button
opens up the 3rd Folder of visually identical Button Files, and
we've taught 12 Buttons to work differently there

      ___  10**x  7   8   9   1/x
      yxz   e**x  4   5   6   x*x
            base  1   2   3   0-x
    dropyx  2**x  0  2nd 3rd absx

see those Base and Int Buttons?

besides you bringing in ordinary Python Int and Float and Complex to work with you,
you can bring in Modular Int's to work with you

deep inside our Python, a Modular Int is three numbers in one:  bits, base, width

press 16 Base, 10 Base, 8 Base, or 2 Base to convert to Hex, Dec, Oct, or Bin

    0 16 -  16 . , Base  15 +  # 0xFF
    0xFF 10 . , Base  # 0d999
    0d999 8 . , Base  # 0o7777
    0o7777 2 . , Base  # 0b1111_1111_1111

and pushing a Modular Int as Top of Stack
opens up the 4th Folder of visually identical Button Files, and
we've taught 9 Buttons to work differently here

      x&-x  shrink  7  8  9  y^x
      yxy    grow   4  5  6  y&x
              int   1  2  3  y&~x
     clear     ~x   0  .  ,  y|x

press Int, or 0 . , Base,
to convert back to a plain Decimal Int, no longer a Modular Int

    0b1111_1111_1111 0 Base  # 4095

    0 1 -  16 Base  Grow Grow  # 0xFFF

press the Shrink button to delete Digits from left,
no matter if they are Sign Extension Digits or not

    0xFFF Shrink Shrink  # 0xF

press the x&-x button to work with Bitmasks

for example, to pick out the 2 found in 0xC1 inside Bitmask 0x60

   0 √ +  , 96 0 +  193 +  # 0x60 0xC1
   0x60 0xC1 over &  over x&-x  # 0x40 0x20
   0x40 0x20 /  # 2

and then symmetrically, to make 0xC1 again out of stuffing that 2 back into place

   0 √ +  , 129 0 +  96 +  # 0x81 0x60
   0x81 0x60  x&-x  2 swap *  # 0x81 0x40
   0x81 0x40  +  # 0xC1

we hid our last three Easter Eggs inside of 0 √

> 0x0 0 hides at 0 √<br>
> 0x0 alone hides at 0 √ +<br>
> the Hex for X hides at 0 √ + X +<br>

someday we might drop another Button
into the blank cell in our layout, between Clear and Over

someday we might add a row of A B C D E F Buttons, to make keying hex go quicker


## 16 Wish us well

we did get it wrong if we gave you this message
while this much macOS reconfiguration is still too expensive for you

please check back a year from now

but before you go, we'll move faster if you tell us that you're waiting on our progress

> open https://twitter.com/intent/tweet?text=@PELaVarre

got thoughts?


## Copied from

Posted into:  https://github.com/pelavarre/byobash/blob/main/macos#readme
<br>
Copied from:  git clone https://github.com/pelavarre/byobash.git
