# G-language
G-language is a very simple 'toy' language used to illustrate concepts in the theory of computation.
Although it is mostly used for education it is also still fully functional.

## Syntax
G-language has a very simple definition. It supports variables, expressed generically as V, which can take any value from the naturals; and labels, expressed generically as L, which point to specific lines in a G-program. Building from variables and labels, G-language supports 4 kinds of statements:

* `V++` to increment a variable by 1
* `V--` to decrement a variable by 1
* `skip` as a no-op
* `if V not 0 goto L` to branch to the line with label L specifically if V is not equal to 0

Any line can also start with a label as `[L]` to indicate the location of a specific label.

In G-language, all variables are initialized to 0 by the runtime, and you do not need to worry about declaring variables yourself, as the runtime will handle them internally (more specifically, the compiler will produce a list of all variables your G-program uses and provide it as a directive to the runtime, so it can initialize them before running the program).

Label names cannot be reused. Additionally, a branch to a label which does not exist will cause the program to terminate.

The variable `Y` is used by the runtime as an 'output' register. The program will show the value of Y as output when the program terminates. However, you are still free to use `Y` however you want.

The label `E` is used by the runtime as a termination register. The program will immediately terminate if a branch leads to the label `E`. You cannot create a label `E` yourself as it is reserved by the system.

## Macros
Macros are pieces of code which are reusable and which perform specific functions. G-programs are cumbersome to write and can become very long, and macros provide a way to shorten your G-programs and make them more readable.

For example, the 'sum' macro from the stdlib library provides a way to add together two variables, A and B, and store the result in C:

`sum A B C`

This greatly simplifies this process as you would otherwise need to perform this addition with manual increments, labels, etc.

Macros in the stdlib library (/macros/stdlib/\*.gmacro) are loaded by the compiler by default. Any macros from other libraries (e.g. shorthand, /macros/shorthand/\*.gmacro) must be passed to the compiler as -link arguments (i.e. -link shorthand).

Macro code consists of some directives at the top of the file, then macro code below directives. The minimum definition for a macro would have the `%prefix` directive, but most macros will also have a `%input` directive and some number of `%require` directives.

`%prefix sum` defines the prefix operator used by the macro (e.g. sum in this case)
`%input 3 variable 0 label` defines how many input vars/labels the macro takes
`%require goto` defines a requirement for a different macro (the given requirement is the *prefix* of the macro your macro requires, not its filename, so in this case our macro would have a requirement that unconditional_branch.gmacro was loaded, as that macro uses the prefix `goto`.)

Macro code is written using special variables and labels prefixed with \_. This is because they all get replaced with 'real' variable and label names during the macro expansion step of compilation.

For example take the first couple of lines of assignment.gmacro:

	[_label1] if _V2 not 0 goto _label2
	goto _label3

In this case, \_label1, \_label2, and \_label3 define non-input labels used by the macro, and \_V2 defines the first input variable to the macro. A macro could also use e.g. \_L1 to reference the first input label to the macro, or \_var1 to reference a non-input variable used by the macro. These formats (\_label\*, \_var\*, \_L\*, \_V\*) are required and can't be deviated from much.

## Compilation

An input file (which, by convention, has a .gc extension) can be compiled by running a line like this:

	python precompile.py my_g_program.gc

This will compile the code, and either output a new file named my_g_program.g to the same directory, OR print errors in your code which need to be corrected.

Optionally you can specify the `-debug` flag which will enable debug mode and provide additional logging, or specify the `-debugx` flag which enables debug mode, as well as outputting extra .g# files containing the code at each step of macro expansion.

The compiled code will have an extra `%vars` directive at the top indicating to the runtime what variable names are used in the program. Additionally, if you specified any other `%directives` in your .gc file, they will be passed through unchanged to the .g file. The most useful of these would be e.g. `%specvar X 5`, which allows you to initialize variables to non-zero values at runtime.

## Running

A compiled G-program can be run by:

	python gruntime.py my_g_program.g

The program should be compiled first from source code via the steps above, as writing G-programs directly in compiled form is not easy.