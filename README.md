# Programming Studio 2 (COSC2804) - Assignment 2
**Student number:** \*\*\*Please place your student number here\*\*\*

This is the README file for Assignment 2 in Programming Studio 2 (COSC2804).

The LC-3 virtual machine contained herein is a fork of [this publically available repo](https://github.com/mhashim6/LC3-Virtual-Machine). The original VM has been modified to enable communication with Minecraft, via the mcpp library.

In contrast to Assignment 1, **you should not modify the VM in any way**. The only files that you should edit are the *.asm files, problem_15.txt, and this README.md file (by adding your student number above).

To build the VM, run `make`.

To test an assembly program:
* Launch a Spigot server and join it, per the [instructions on Canvas](https://rmit.instructure.com/courses/123553/pages/getting-started-with-minecraft++-and-elci?module_item_id=5509058).
* Assemble the .asm file via laser.
* Run `./lc3 program_name.obj`.
