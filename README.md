# Algorithmic Composition

Final project for Deep Listening (ARTS-4410) at RPI in Summer 2019

In this project, I wanted to use algorithmic composition to create classical
piano music by chopping up existing pieces by famous composers. I did this with
the help of the [piano-midi.de](http://www.piano-midi.de) dataset, a collection
of hundreds of classical compositions by composers such as Mozart, Bach,
Beethoven, and more, in MIDI format. I fetched all of these MIDI files then
created a program that parses a user-defined subset of this data using
[python-midi](https://github.com/vishnubob/python-midi) and successively chooses
random tracks to splice together chunks of 20-50 notes. To keep things flowing
organically, tracks are spliced together only at places where the pitches match
up.

