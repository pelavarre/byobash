# how to make Muscle Memory grow well

how do the docs you write invite engineers into developing more muscle memory?

more muscle memory is what they need to keep their attention on what matters more, sure, but
how do your written words help them develop these muscles?

me, i’m pretty happy with what i’ve done lately for Muscle Memory inside of Sh Terminal’s

## the Trick i pulled

our work inside the Sh Terminal we do in a call-and-response style -
we make me type a line of text, then i press the Return key, then the machine answers back

commonly these lines begin with some imperative verb -
like if i say "clear" then that means i'm saying, to the machine, "hey you, clear it for us",
meaning the machine should now wipe its transcript of today's conversation, so it does

## 1 - i bring my own Examples

the trick i pulled was to **mark my words**

now i go ahead and type out the 5 keys C-L-E-A-R, but
then i don't cooperatively press the 1 Return key like normal,
instead i creatively press the 2 keys of Tab and Return

    c l e a r Tab Return

the conventions the machine follows then drive it
to pretend i typed out the 10 keys C-L-E-A-R-Dot-P-Y Space Return, and
there the machine gives me **my own curated list of Examples** i want to remember,
my own examples of commands i often want to speak clearly that start with that verb

    clear.py

for instance the machine will remind me that how i get it to scroll the transcript away,
without destroying the transcript, is for me to type the 8 keys C-L-E-A-R-Space-X Return

    clear -x  # scroll away the Rows on Screen, as if ⌃L pressed in place of ⌘K

bonus included!
the machine reminds me of what i type by putting a copy of it on screen
in a place where a macOS triple click ⌘C ⌘V types it for me -
so in reality i just pick and go -
i don't have to type it out in full and with a machine-like absence of tupos

## 2 - i bring my own Notes

to people in our business, it won't be much surprise
that the machine also keeps it easy for me
to ask instead for **my own curated list of Notes**
that i want me to remember better,
my notes on how i crafted my well-spoken commands,
my notes on what my incisive sentences really mean

specifically, Python people in our business already know
i can press the 5 keys C-L-E-A-R and
then also follow up with the 5 keys Space-Dash-Dash-H Return,
so as to kick my machine's own "Python ArgParse --help" conventions
into telling it to give me my own curated list of Notes

    clear.py --h  # short for clear.py --help

but here's the great trick

## 3 - i bring my own Preferences/ Fixes

what do you think happens when i press the 9 keys C-L-E-A-R-Space-Dash-Dash Return

    clear.py --

my input is just like before, except i skipped the 10th key, the H key, i didn't press it

here's the huge thing

what happens in that corner?

it's a vanishingly small corner,
where we have established zero conventions
to make it meaningful instead of verbose and redundant -
my choice of Easter Eggs for me to hide in that spot is completely up to me,
blank page, green field, limitlessly creative options

because reasons, put in place back in about 1972

## 3.1 - how they accidentally gave me a room of my own

specifically,
in the grammar of these conversations i hold with the machine,
that special "--" mark divides Adverbs from Nouns

it's a bit of punctuation that works like a radio operator
saying "Over" to mark the end of their turn speaking -
that "--" mark means a mix of Adverbs and Nouns came before it,
but now only Nouns will follow -
so if they sound like Adverbs you'll be hearing them correctly
only if you take them as Nouns anyhow

well the huge lever hidden in this small mark
is that i can give out this conventional promise,
that for sure i'll follow up after this special mark with only Nouns, and then
i can choose to decline to deliver

i can show up with literally nothing after that "--" mark -
i can choose to break my promise

## 3.2 - who designs the interior of my room? i do

when youibetray and surprise a machine with that kind of ju-jitsu,
then sure in theory there's no telling what it will do -
we can't say what a machine does
when i give it surprise new input that we've never tested (
not till after i hire me into that PhD i should be doing )

but this particular theory of fear is zero problem in practice

practically speaking, odds on, it was i myself who wrote our "clear.py" program,
it was only someone else who wrote and forgot to test the "clear" program

so, fair enough, i admit, i can't tell you what happens if i risk saying

    clear --

but i know i can myself drop whatever helps me into when i say

    clear.py --

what happens there is a default just obscure enough,
slipped just far enough off the beaten path,
that they've practically always left it undefined

## 3.3 - they didn't tell me, they just gave me, this place for me

pratically nobody defines 'clear --' to do anything different than 'clear' does,
which opens up a wide space for me to work,
grants me a fierce indepedence

i can afford to drop my own Examples into 'clear.py',
my own Notes into 'clear.py --h',
and **my own Preferences/ Fixes** into 'clear.py --'

the File System keeps it all organised for me

i've written 89 of these Py Files of Examples + Notes + Preferences/ Fixes so far,
with no end in sight -
all the imperative words i work come to me
with poor examples or zero, poor notes, and
wrong choices held over these last fifty years

we can stop it, and we can stop it now,
because here i can afford to do the work myself, alone at my own desk

having read this far, now you can do it too

## 4 - please try it, you'll love it

like for, me, what helps me best, is for 'clear.py --' to Always mean

    echo -ne '\e[H\e[2J\e[3J'

this H 2J 3J Escape Sequence
works the same as ⌘K when i run Ubuntu Linux inside a Mac Ssh Terminal,
but our Ubuntu people forgot to distribute it correctly
until Apr/2020 Focal Ubuntu Linux 20.04

so while i'm working back with
Apr/2018 Bionic Ubuntu Linux 18.04 and
Apr/2016 Xenial Ubuntu Linux and so on

it's so very nice, it feels so very good,
for me to have a Clear Command that works, there too

i just have to make it myself, or help along the distribution of it in some other way -
because people, oh well

please try it, i hope you'll love it, i know you might, i know i do
