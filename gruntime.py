import re
import sys

# the actual runtime for executing a compiled .g file.
# this steals some code from precompile.py since the language is p simple
# this can only run 'pure' g code (i.e. statements from 1 of the 5 possible types)
# so no macros are expected to be present in these files.
# there is allotment for specific directives (e.g. %vars)
# but these must all be present in the header of the compiled file.

variables = {}
debug = False
step = False

def run_program(program):
	global variables
	gc = 0
	pc = 0
	# possible stmt in a program:
	# V++
	# V--
	# if V not 0 goto L
	# skip
	# any content after a semicolon ; should be ignored
	inc_checker = re.compile(r'[A-Za-z]+[0-9]*\+\+$')
	dec_checker = re.compile(r'[A-Za-z]+[0-9]*\-\-$')
	while True:
		stmt = program[pc]
		if debug:
			print(variables)
			print(str(gc) + ": (pc " + str(pc) + ") - " + stmt)
			print()
		if step:
			print("State: " + str(variables))
			print("Next instruction: " + stmt)
			input("Enter to proceed")
			print()
		# tokenize the statement
		stmt_tokens = stmt.split(' ')
		stmt_tokens = [token for token in stmt_tokens if token.strip() != ""]
		# start with the first token in the list.
		first = stmt_tokens[0]
		if inc_checker.match(first):
			# match an increment operation, V++.
			# make sure no other tokens exist after first.
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(pc+1)+": Too many tokens")
				print(stmt)
				exit(-1)
			# grab the variable name
			var = first.replace("++", "")
			# increment the variable
			variables[var] += 1
		elif dec_checker.match(first):
			# match a decrement operation, V--.
			# make sure no other tokens exist after first.
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(pc+1)+": Too many tokens")
				print(stmt)
				exit(-1)
			# grab the variable name
			var = first.replace("--", "")
			# decrement the variable, clamped to 0
			variables[var] = max(0, variables[var]-1)
		elif first == "if":
			# if statement (conditional branch) has a very specific structure.
			# if V not 0 goto L
			# check remaining tokens... structure is very firm so we don't need to 
			# be too concerned about looping over the tokens, just check the
			# exact matching structure.
			# check for wrong count of tokens
			if len(stmt_tokens) < 6:
				print("Error on line "+str(pc+1)+": Not enough tokens")
				print(stmt)
				exit(-1)
			# check for too many tokens (not in a comment)
			if len(stmt_tokens) > 6 and stmt_tokens[6].strip() != ";":
				print("Error on line "+str(pc+1)+": Too many tokens")
				print(stmt)
				exit(-1)
			# get the V from the statement
			var_compare = stmt_tokens[1]
			# check for bad setup of the rest of the statement
			if not stmt_tokens[2] == "not" or not stmt_tokens[3] == "0" or not stmt_tokens[4] == "goto":
				print("Error on line "+str(pc+1)+": if statement missing not 0 goto clause")
				print(stmt)
				exit(-1)
			# get the L from the statement
			label_compare = stmt_tokens[5]
			# now we compare the value of var_compare to 0
			if variables[var_compare] != 0:
				# if it's not 0 we change pc and continue
				pc = int(label_compare)
				gc += 1
				continue
		elif first == "skip":
			# skip is always 'naked'
			# make sure no other tokens exist
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(pc+1)+": Too many tokens")
				print(stmt)
				exit(-1)
		elif first == "exit":
			# this isnt part of the formal grammar
			# but i will use it when compiling to just be a straight-up termination
			# statement.
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(pc+1)+": Too many tokens")
				print(stmt)
				exit(-1)
			return
		else:
			print("Error on line "+str(pc+1)+": Unmatched initial token")
			print(stmt)
			exit(-1)
		pc += 1
		gc += 1

# definition for %specvar directive
# %specvar provides an initialization value for a variable,
# e.g. %specvar X 4 means X <- 4.
def specvar(l):
	global variables
	# confirm the correct format
	if not len(l.split(" ")) == 3:
		print("Runtime error, %specvar has incorrect argument count")
		print(l)
		exit(-1)
	var = l.split(" ")[1]
	if not var in variables:
		print("Runtime error, %specvar specifies a non-existent variable")
		print(l)
		exit(-1)
	val = l.split(" ")[2]
	if not val.isdigit():
		print("Runtime error, %specvar assigns a non-numeric value to a variable")
		print(l)
		exit(-1)
	# assign the value to the variable
	variables[var] = int(val)

def gruntime(file):
	global variables
	global debug
	global step
	if '-debug' in sys.argv:
		debug = True
	if '-step' in sys.argv:
		step = True
	program = []
	# open the input file
	with open(file) as f:
		# load all lines into program
		program = f.readlines()
		# replace all newlines with blank and trim
		# I also do a replacement from ';' -> ' ; ' to avoid difficulty tokenizing comments
		program = [l.replace('\n', '').replace(';', ' ; ').strip() for l in program]
		# remove any blank lines
		program = [l for l in program if l is not ""]
		# remove any lines starting with ;
		# to not have to tokenize
		program = [l for l in program if not l.startswith(';')]
		# check for a leading '%vars' directive
		# the %vars directive will always, always be line 0
		if program[0].startswith("%vars"):
			# load the list of vars
			vars_ = program[0].split(" ")
			if not len(vars_) == 2:
				print("Runtime error, %vars malformed")
				print(program[0])
				exit(-1)
			vars = vars_[1].split(',')
			for var in vars:
				variables[var] = 0
			# now remove the leading %vars directive
			program = program[1:]
		# check for any other % directives
		# some will be processed but the rest will be ignored
		line = 0
		l = program[line]
		while (l.startswith("%")):
			# %specvar V i fills variable V with integer i initially.
			if l.startswith("%specvar"):
				# offloaded
				specvar(l)
			line += 1
			l = program[line]
		# this cuts off all the % directives
		program = program[line:]
		# now we want to actually run the program.
		run_program(program)
		# print the return value of the program
		print("out: " + str(variables['Y']))
		print("final state: " + str(variables))

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Please provide at least 1 argument, the path to a compiled G file, and optionally additional -flags after this.")
		exit(-1)
	gruntime(sys.argv[1])