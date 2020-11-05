# PyTin2

## Why PyTin2?

The first idea to create this clicker came from playing metin2. 
I noticed that many simple tasks, such as buying and opening clams or
reading books, scrolls and others are quite time-consuming and can 
easily be automated. So I decided to develop my own clicker, which will
help me with those things. 
Currently the program handles the events of pressing left or right mouse buttons
(selected number of times) and moving the cursor to the given location

In the future it will be possible to handle "drags" and inserting time delays.
And who knows what more?

## How To Install

Soo, at first you need to install Python version 3.7.x or later. 
You can simply achive that by visiting: https://www.python.org/

Then you need to install pip (if it did not install with python automatically)

If pip is installed you need to manually install two packages that are used in 
mya script: 

PyAutoGUI==0.9.52

pynput==1.6.8


To do that, you need to open windows cmmand line
 (click windows key + R, write "cmd" and press enter)
and write down:

```sh
pip install PyAutoGUI 
```
(press enter)

```sh
pip install pynput 
```
(press enter)

or easier way just download "requirements.txt"
right click in the directory where you put this file
open windows command line there and write down:

```sh
pip install -r requirements.txt 
```

it will work same way as installing them one by one


## How To Run Program


Okay, so when you finally install python and all required dependencies
you can run PyTin2 script using windows command line.

It's very important to remember that, if your program in which you will use
this clicker is running as an administrator, you need to run cmd as an administrator
as well. Otherwise, clicker will move your mouse around, but won't simulate left or right click
inside of the program.

To run PyTin2, you need to open your command line in directory, where the script is placed.
To simply do that, you can just right click in the directory where the script is located, and press
"run windows command line here" / "run powershell here" / or something simillar.

Then in your "terminal" simply write (remember to add extension or it won't work):

```sh
python PyTin2.py 
```

You can use "tab key" on your keyboard to autofill commands.

## Release History

* 1.0.0 (05.11.2020)
    * First release

## Meta

Kamil Graczyk - [@Twitter](https://twitter.com/xor_toja) - graczyk53@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/xorToja](https://github.com/xorToja)

## Contributing

See ``CONTRIBUTION`` for more information.
