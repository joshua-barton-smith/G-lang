import re
import os
import sys

# main steps for compilation:
# 1. syntax evaluation, macro loading
# 2. identify list of used variables and labels
# 3. macro expansion
# 4. label replacement
# 5. E insertion
# outputs code that can be run

macros = {}
debug = False
debug_extreme = False

# handles the %prefix macro
# the minimum definition of a macro has a
# %prefix directive to indicate how it's supposed to be used.
# e.g. %prefix zero
def macro_prefix(mc_struct, l):
	if debug:
		print("Handle macro prefix for macro " + mc_struct['name'])
	mc_def = l.split(" ")
	if not len(mc_def) == 2:
		print("Macro compilation error, macro " + mc_struct['name'] + " has incorrect argument count for prefix directive")
		exit(-1)
	# get the prefix
	pref = mc_def[1]
	# check if the prefix has already been used
	if pref in macros:
		print("Macro compilation error, macro " + mc_struct['name'] + " duplicates prefix with " + macros[pref]['name'])
		exit(-1)
	# store the prefix into mc_struct
	mc_struct['prefix'] = pref
	if debug:
		print("Prefix " + pref + " assigned")
		print()

# handles the %input macro
# e.g. %input 1 variable 1 label
def macro_input(mc_struct, l):
	if debug:
		print("Handle macro input for macro " + mc_struct['name'])
	mc_def = l.split(" ")
	if not len(mc_def) == 5:
		print("Macro compilation error, macro " + mc_struct['name'] + " has incorrect argument count for input directive")
		exit(-1)
	# check the right values are being passed
	if not mc_def[1].isdigit() or not mc_def[3].isdigit():
		print("Macro compilation error, macro " + mc_struct['name'] + " does not provide integer values for input directive")
		exit(-1)
	# get the number of variables and labels
	var_count = int(mc_def[1])
	label_count = int(mc_def[3])
	if var_count < 0 or label_count < 0:
		print("Macro compilation error, macro " + mc_struct['name'] + " defines negative label or variable counts")
		exit(-1)
	# put it into mc_struct
	mc_struct['var_count'] = var_count
	mc_struct['label_count'] = label_count
	if debug:
		print(str(var_count) + " in vars assigned for macro")
		print(str(label_count) + " in labels assigned for macro")
		print()

def macro_require(mc_struct, l):
	if debug:
		print("Handle macro require for macro " + mc_struct['name'])
	mc_def = l.split(" ")
	if not len(mc_def) == 2:
		print("Macro compilation error, macro " + mc_struct['name'] + " has incorrect argument count for require directive")
		exit(-1)
	prefreq = mc_def[1]
	if not 'requires' in mc_struct:
		mc_struct['requires'] = [prefreq]
	else:
		mc_struct['requires'].append(prefreq)
	if debug:
		print("Added macro requirement " + prefreq)

def macro_loading(macro_folders):
	if debug:
		print("Start processing macros")
	global macros
	for folder in macro_folders:
		if debug:
			print("Start processing macros from library " + folder)
		for filename in os.listdir('macro/' + folder):
			if filename.endswith('.gmacro'):
				with open(os.path.join('macro/' + folder, filename)) as macro:
					if debug:
						print ("Start processing macro " + filename.replace(".gmacro", ""))
					mc = macro.readlines()
					mc = [l.replace('\n', '').replace(';', ' ; ').strip() for l in mc]
					# remove any blank lines
					mc = [l for l in mc if l is not ""]
					# remove any lines starting with ;
					# to not have to tokenize
					mc = [l for l in mc if not l.startswith(';')]
					# now we process % directives
					# some will be processed but the rest will be ignored
					mc_struct = {'name': filename.replace('.gmacro', ''), 'requires': []}
					line = 0
					l = mc[line]
					while (l.startswith("%")):
						if l.startswith("%input"):
							macro_input(mc_struct, l)
						elif l.startswith("%prefix"):
							macro_prefix(mc_struct, l)
						elif l.startswith("%require"):
							macro_require(mc_struct, l)
						line += 1
						l = mc[line]
					# this cuts off all the % directives
					mc = mc[line:]
					# confirm that the macro contained at a minimum the %prefix directive
					if not 'prefix' in mc_struct:
						print("Macro compilation error, macro " + mc_struct['name'] + " does not define a prefix operator")
						exit(-1)
					# store code into mc_struct
					mc_struct['code'] = mc
					# and push the struct into macros
					macros[mc_struct['prefix']] = mc_struct
					if debug:
						print("Finish processing macro")
						print()
	if debug:
		print("All macros finished processing")
		print("Macro definitions: " + str(macros))
		print()

# checks that all macros have their requirements met.
# will unload any macros with a missing requirement.
def macro_requirement_checking():
	global macros
	if debug:
		print("Checking macro requirements")
	should_unload = []
	for m in macros:
		macro = macros[m]
		reqs = macro['requires']
		for req in reqs:
			if not req in macros:
				if debug:
					print("Macro " + macro['name'] + " is missing requirement " + req)
					print("Unloading")
				should_unload.append(m)
				break
	for m in should_unload:
		del macros[m]
	if debug:
		print("Macro requirements checked")

# checks syntax on an input program (list of statements)
# it will also produce a list of variables and labels used in the program
# and return a tuple (vars, labels).
def syntax_check(program):
	if debug:
		print("syntax checking program")
	# list of vars, labels
	vars = ['Y']
	labels = []
	# line count
	line = 1
	# this is used to continually re-load/re-check until all macros are expanded
	# this allows macros to use other macros themselves.
	has_macro = False
	# possible stmt in a program:
	# V++
	# V--
	# if V not 0 goto L
	# skip
	# any content after a semicolon ; should be ignored
	# any statement can have a [L] before it to indicate a label
	# due to the above 2 requirements we must tokenize
	label_checker = re.compile(r'\[[A-Za-z]+[0-9]*\]$')
	inc_checker = re.compile(r'[A-Za-z]+[0-9]*\+\+$')
	dec_checker = re.compile(r'[A-Za-z]+[0-9]*\-\-$')
	for stmt in program:
		# tokenize the statement
		stmt_tokens = stmt.split(' ')
		stmt_tokens = [token for token in stmt_tokens if token.strip() != ""]
		# start with the first token in the list.
		first = stmt_tokens[0]
		# if it's [L] we should extract the label and discard.
		if label_checker.match(first):
			# we need to confirm this label is not already in labels.
			if not first[1:-1] in labels:
				labels.append(first[1:-1])
			else:
				print("Error on line "+str(line)+": Repeated label")
				print(stmt)
				exit(-1)
			stmt_tokens = stmt_tokens[1:]
			first = stmt_tokens[0]
		if inc_checker.match(first):
			# match an increment operation, V++.
			# make sure no other tokens exist after first.
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(line)+": Too many tokens")
				print(stmt)
				exit(-1)
			# grab the variable name
			var = first.replace("++", "")
			# add it to the list
			if not var in vars:
				vars.append(var)
		elif dec_checker.match(first):
			# match a decrement operation, V--.
			# make sure no other tokens exist after first.
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(line)+": Too many tokens")
				print(stmt)
				exit(-1)
			# grab the variable name
			var = first.replace("--", "")
			# add it to the list
			if not var in vars:
				vars.append(var)
		elif first == "if":
			# if statement (conditional branch) has a very specific structure.
			# if V not 0 goto L
			# check remaining tokens... structure is very firm so we don't need to 
			# be too concerned about looping over the tokens, just check the
			# exact matching structure.
			# check for wrong count of tokens
			if len(stmt_tokens) < 6:
				print("Error on line "+str(line)+": Not enough tokens")
				print(stmt)
				exit(-1)
			# check for too many tokens (not in a comment)
			if len(stmt_tokens) > 6 and stmt_tokens[6].strip() != ";":
				print("Error on line "+str(line)+": Too many tokens")
				print(stmt)
				exit(-1)
			# get the V from the statement
			var_compare = stmt_tokens[1]
			# check for bad setup of the rest of the statement
			if not stmt_tokens[2] == "not" or not stmt_tokens[3] == "0" or not stmt_tokens[4] == "goto":
				print("Error on line "+str(line)+": if statement missing not 0 goto clause")
				print(stmt)
				exit(-1)
			# get the L from the statement
			label_compare = stmt_tokens[5]

			# add var_compare to vars if not exists
			if not var_compare in vars:
				vars.append(var_compare)
			# we don't need to appent label_compare, bc there is no guarantee
			# that label_compare is real (if it is undeclared we will rename it to E later)
		elif first == "skip":
			# skip is always 'naked'
			# make sure no other tokens exist
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(line)+": Too many tokens")
				print(stmt)
				exit(-1)
		elif first == "exit":
			# this isnt part of the formal grammar
			# but i will use it when compiling to just be a straight-up termination
			# statement.
			if len(stmt_tokens) > 1 and stmt_tokens[1].strip() != ";":
				print("Error on line "+str(line)+": Too many tokens")
				print(stmt)
				exit(-1)
		else:
			# possible that the token matches a macro
			# we need to check if first contains a macro prefix
			if first not in macros:
				print("Error on line "+str(line)+": Unmatched initial token")
				print(stmt)
				exit(-1)
			else:
				# we want to validate the right argument count is going to the macro
				# this is imperfect at this step bc we don't have a full label/variable list.
				# so we just check the arg count is equal to var_count+label_count
				arg_count = macros[first]['label_count'] + macros[first]['var_count']
				has_macro = True
				if len(stmt_tokens) > (1+arg_count) and stmt_tokens[1+arg_count].strip() != ";":
					print("Error on line "+str(line)+": Too many tokens")
					print(stmt)
					exit(-1)
		line += 1
	if debug:
		print("Program passed syntax check")
		print("Vars: " + str(vars))
		print("Labels: " + str(labels))
		print("Has macro: " + str(has_macro))
		print()
	return (vars, labels, has_macro)

def macro_expansion(program, vars, labels):
	if debug:
		print("Expanding macros for program")
	line = 0
	label_checker = re.compile(r'\[\_[A-Za-z]+[0-9]*\]$')
	inc_checker = re.compile(r'\_[A-Za-z]+[0-9]*\+\+$')
	dec_checker = re.compile(r'\_[A-Za-z]+[0-9]*\-\-$')
	# iterate over all the statements in the program
	while True:
		var_repl = {}
		lab_repl = {}
		stmt = program[line]
		# tokenize the statement
		stmt_tokens = stmt.split(' ')
		stmt_tokens = [token for token in stmt_tokens if token.strip() != ""]
		# start with the first token in the list.
		first = stmt_tokens[0]
		# we only care about tokens for macros
		if first in macros:
			# if a macro exists we need to define a label for the line immediately following the macro.
			# this is because any macro calling 'goto E' should jump to next line instead of terminating.
			# so first we will gen a new label name, and then replace any E with that label name
			# within the macro.
			# construct a new variable name not already in labels
			new_name_suf = 0
			new_name = "L" + str(new_name_suf)
			while new_name in labels:
				new_name_suf += 1
				new_name = "L" + str(new_name_suf)
			labels.append(new_name)
			exit_name = new_name
			if debug:
				program.insert(line+1, "[" + exit_name + "] skip ; end of macro " + macros[first]['name'])
			else:
				program.insert(line+1, "[" + exit_name + "] skip")
			# this gets the macro in use
			macro = macros[first]
			# get the number of input variables/labels from the line
			varct = macro['var_count']
			labct = macro['label_count']
			in_vars = []
			in_labs = []
			# iterate over each input token and map it to one of each
			for token in stmt_tokens[1:]:
				if token in vars:
					varct -= 1
					in_vars.append(token)
				elif token in labels:
					labct -= 1
					in_labs.append(token)
				elif token == ";":
					# this marks end bc rest of statement is a comment
					break
				else:
					# we have to assume any other input token is a new, previously undefined variable
					# and add it to vars.
					vars.append(token)
					in_vars.append(token)
					varct -= 1
			if not varct == 0 or not labct == 0:
				print("Macro expansion error, input tokens do not match required count of variables or labels")
				print(stmt_tokens)
				print("Line " + str(line+1))
				exit(-1)
			# need to replace placeholder labels, variables with real ones
			# first - replace the _V*, _L* because these are the ones which were input to the program
			varct = macro['var_count']
			labct = macro['label_count']
			while varct != 0:
				name = "_V" + str(varct)
				repl = in_vars.pop(len(in_vars) - 1)
				var_repl[name] = repl
				varct -= 1
			while labct != 0:
				name = "_L" + str(labct)
				repl = in_labs.pop(len(in_labs) - 1)
				lab_repl[name] = repl
				labct -= 1
			# iterate over lines in macro['code'] to do the replacement
			mc_code = macro['code'].copy()
			lmc = 0
			for c in mc_code:
				has_prefix = False
				# we need to tokenize this, again, because a find+replace doesnt work well (annoying)
				mc_tokens = c.split(" ")
				mc_tokens = [token for token in mc_tokens if token.strip() != ""]
				# check the input... we care about V++, V--, if-goto statements
				first = mc_tokens[0]
				# if it's [L] we should extract the label and discard.
				if label_checker.match(first):
					# we need to confirm this label is not already in labels.
					if not first[1:-1] in labels:
						# now we want to check if this label needs replacing
						lb = first[1:-1]
						if not lb in lab_repl and lb.startswith('_label'):
							# construct a new variable name not already in labels
							new_name_suf = 0
							new_name = "L" + str(new_name_suf)
							while new_name in labels:
								new_name_suf += 1
								new_name = "L" + str(new_name_suf)
							labels.append(new_name)
							lab_repl[lb] = new_name
							# now replace the line with the new case
							label_prefix = "[" + lab_repl[lb] + "] "
							has_prefix = True
							del mc_tokens[0]
							first = mc_tokens[0]
						elif lb in lab_repl and lb.startswith('_label'):
							# now replace the line with the new case
							label_prefix = "[" + lab_repl[lb] + "] "
							has_prefix = True
							del mc_tokens[0]
							first = mc_tokens[0]
					else:
						print("Error in macro expansion: Repeated label")
						print(stmt)
						exit(-1)
				if inc_checker.match(first):
					# match an increment operation, V++.
					# make sure no other tokens exist after first.
					if len(mc_tokens) > 1 and mc_tokens[1].strip() != ";":
						print("Error in macro expansion: Too many tokens")
						print(c)
						exit(-1)
					# grab the variable name
					var = first.replace("++", "")
					# replace if needed
					if var in var_repl:
						mc_code[lmc] = var_repl[var] + "++"
					# check if the variable starts with _var
					# (implicitly it won't be in var_repl due to previous if)
					elif var.startswith('_var'):
						# construct a new variable name not already in vars
						new_name_suf = 0
						new_name = "V" + str(new_name_suf)
						while new_name in vars:
							new_name_suf += 1
							new_name = "V" + str(new_name_suf)
						vars.append(new_name)
						var_repl[var] = new_name
						mc_code[lmc] = var_repl[var] + "++"
				elif dec_checker.match(first):
					# match an increment operation, V++.
					# make sure no other tokens exist after first.
					if len(mc_tokens) > 1 and mc_tokens[1].strip() != ";":
						print("Error in macro expansion: Too many tokens")
						print(c)
						exit(-1)
					# grab the variable name
					var = first.replace("--", "")
					# replace if needed
					if var in var_repl:
						mc_code[lmc] = var_repl[var] + "--"
					# check if the variable starts with _var
					# (implicitly it won't be in var_repl due to previous if)
					elif var.startswith('_var'):
						# construct a new variable name not already in vars
						new_name_suf = 0
						new_name = "V" + str(new_name_suf)
						while new_name in vars:
							new_name_suf += 1
							new_name = "V" + str(new_name_suf)
						vars.append(new_name)
						var_repl[var] = new_name
						mc_code[lmc] = var_repl[var] + "--"
				elif first.startswith("if"):
					# if statement (conditional branch) has a very specific structure.
					# if V not 0 goto L
					# check remaining tokens... structure is very firm so we don't need to 
					# be too concerned about looping over the tokens, just check the
					# exact matching structure.
					# check for wrong count of tokens
					if len(mc_tokens) < 6:
						print("Error in macro expansion: Not enough tokens")
						print(c)
						exit(-1)
					# check for too many tokens (not in a comment)
					if len(mc_tokens) > 6 and mc_tokens[6].strip() != ";":
						print("Error in macro expansion: Too many tokens")
						print(c)
						exit(-1)
					# get the V from the statement
					var_compare = mc_tokens[1]
					# check for bad setup of the rest of the statement
					if not mc_tokens[2] == "not" or not mc_tokens[3] == "0" or not mc_tokens[4] == "goto":
						print("Error in macro expansion: if statement missing not 0 goto clause")
						print(c)
						exit(-1)
					# get the L from the statement
					label_compare = mc_tokens[5]
					if label_compare == "E":
						label_compare = exit_name

					if var_compare not in var_repl and var_compare.startswith("_var"):
						# construct a new variable name not already in vars
						new_name_suf = 0
						new_name = "V" + str(new_name_suf)
						while new_name in vars:
							new_name_suf += 1
							new_name = "V" + str(new_name_suf)
						vars.append(new_name)
						var_repl[var_compare] = new_name

					if label_compare not in lab_repl and label_compare.startswith("_label"):
						# construct a new variable name not already in labels
						new_name_suf = 0
						new_name = "L" + str(new_name_suf)
						while new_name in labels:
							new_name_suf += 1
							new_name = "L" + str(new_name_suf)
						labels.append(new_name)
						lab_repl[label_compare] = new_name


					# we need to check if either V or L needs replacing.
					if var_compare in var_repl and label_compare in lab_repl:
						mc_code[lmc] = "if " + var_repl[var_compare] + " not 0 goto " + lab_repl[label_compare]
					elif var_compare in var_repl:
						mc_code[lmc] = "if " + var_repl[var_compare] + " not 0 goto " + label_compare
					elif label_compare in lab_repl:
						mc_code[lmc] = "if " + var_compare + " not 0 goto " + lab_repl[label_compare]
				elif first in macros:
					tk = 1
					had_e = False
					for next_token in mc_tokens[1:]:
						if next_token == "E":
							had_e = True
							mc_tokens[tk] = exit_name
						if next_token.startswith("_L") or next_token.startswith("_label"):
							if next_token in lab_repl:
								mc_tokens[tk] = lab_repl[next_token]
							else:
								# construct a new variable name not already in labels
								new_name_suf = 0
								new_name = "L" + str(new_name_suf)
								while new_name in labels:
									new_name_suf += 1
									new_name = "L" + str(new_name_suf)
								labels.append(new_name)
								lab_repl[next_token] = new_name
								mc_tokens[tk] = lab_repl[next_token]
						if next_token.startswith("_V") or next_token.startswith("_var"):
							if next_token in var_repl:
								mc_tokens[tk] = var_repl[next_token]
							else:
								# construct a new variable name not already in labels
								new_name_suf = 0
								new_name = "V" + str(new_name_suf)
								while new_name in vars:
									new_name_suf += 1
									new_name = "V" + str(new_name_suf)
								vars.append(new_name)
								var_repl[next_token] = new_name
								mc_tokens[tk] = var_repl[next_token]
						tk += 1
					mc_code[lmc] = " ".join(mc_tokens)
				if has_prefix:
					mc_code[lmc] = label_prefix + mc_code[lmc]
				if lmc == 0 and debug:
					mc_code[lmc] = mc_code[lmc] + " ; start of macro " + macro['name'] + " (" + stmt + ")"
				lmc += 1
			# remove the original line from the program
			program.pop(line)
			# insert the new code from the macro
			for c in mc_code:
				program.insert(line, c)
				line += 1
			# this is some manip to keep the line counter working...
			line -= 1
		line += 1
		# break when whole program has been de-macroed
		if line >= len(program):
			break
	if debug:
		print("Macro expansion completed")
		print()

# replaces all instances of labels with their actual line number
# so that all goto statements point to a specific line.
def label_replacement(program):
	if debug:
		print ("Performing label replacement")
	label_map = {}
	label_checker = re.compile(r'\[[A-Za-z]+[0-9]*\]$')
	line = 1
	# iterate over each statement and find label definitions
	for stmt in program:
		# tokenize the statement
		stmt_tokens = stmt.split(' ')
		# start with the first token in the list.
		first = stmt_tokens[0]
		# if it's [L] we should extract the label.
		if label_checker.match(first):
			label = first[1:-1]
			# now we want to map the label to the current line.
			label_map[label] = line-1
			program[line-1] = stmt[len(first)+1:]
		line += 1
	# now replace any uses of the label with the line number
	line = 1
	for stmt in program:
		# tokenize the statement
		stmt_tokens = stmt.split(' ')
		# start with the first token in the list.
		first = stmt_tokens[0]
		# we only care about if-goto statements for label replacement
		if first == "if":
			# note that the label may or may not exist, if it doesn't exist we need to replace it with E
			# (since non-existent labels terminate)
			if not stmt_tokens[5] in label_map:
				stmt_tokens[5] = 'E'
			# we already validated the syntax so just grab stmt_tokens[5]
			stmt_tokens[5] = str(label_map[stmt_tokens[5]])
			program[line-1] = " ".join(stmt_tokens)
		line += 1
	if debug:
		print("Label replacement completed")
		print("Label mapping: " + str(label_map))
	return program

# the label E is used as a special label, which indicates the program should terminate.
# this label doesn't exist so we just need to add it to the end.
# fortunately this is simple, we just add one line to the very end of the program,
# "exit"
def e_insertion(program):
	if debug:
		print("Adding E label")
	program.append("[E] exit")
	if debug:
		print("E label added")
		print()
	return program

def collect_directives(program):
	if debug:
		print("Finding % directives")
	dirs = []
	line = 0
	stmt = program[line]
	while stmt.startswith("%"):
		if debug:
			print ("Found directive " + stmt)
		dirs.append(stmt)
		line += 1
		stmt = program[line]
	if debug:
		print("Finished finding % directives")
	return (line, dirs)

# performs compilation on an input file
def precompile(file):
	program = []
	global debug
	global debug_extreme
	if '-debug' in sys.argv:
		debug = True
	if '-debugx' in sys.argv:
		debug = True
		debug_extreme = True

	print ("Compiling G-program from source file " + file)
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

		# collect %directives
		# these are passed directly from the .gc to the .g
		# so you can specify e.g. %specvar directives
		# and have them copied through to the compiled code
		(line, dirs) = collect_directives(program)
		program = program[line:]

		# 0. perform macro loading by scanning folders.
		# all folders in the macro subdirectory are 'packages' of macros.
		# the stdlib folder is loaded by default as it contains a lot of generally useful macros.
		# any other folders currently are not loaded but we will implement %directives for this.
		macro_loading(['stdlib'])
		macro_requirement_checking()

		# 0b. E insertion
		program = e_insertion(program)

		# 1. syntax evaluation and 2. identify var/label list
		(vars, labels, has_macro) = syntax_check(program)

		x = 1

		# we need to call this continually so long as more macros exist to expand.
		while has_macro:
			# 3. macro expansion
			# essentially we need to scan lines in program again,
			# identify which lines use a macro, and then insert the
			# macro code into those lines.
			macro_expansion(program, vars, labels)

			# 4. syntax recheck
			# this is important to make sure the macros expanded out properly,
			# to check if more macros need to be expanded,
			# and to recompute var/label lists
			(v, l, has_macro) = syntax_check(program)
			# output to .g file
			noext = file.split('.')[0]
			if debug_extreme:
				with open(noext + ".g" + str(x), "w+") as f2:
					f2.write("\n".join(program))

			x += 1

		# 5. label replacement
		program = label_replacement(program)
		# final processing - add variable list to the header
		program.insert(0, "%vars " + ",".join(vars))
		# add remaining %dirs to the file
		program.insert(1, "\n".join(dirs) + "\n")
		# output to .g file
		noext = file.split('.')[0]
		with open(noext + ".g", "w+") as f2:
			f2.write("\n".join(program))
			print("Wrote compiled code to " + noext + ".g")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Please provide at least 1 argument, the path to a G source file, and optionally additional -flags after this.")
		exit(-1)
	precompile(sys.argv[1])