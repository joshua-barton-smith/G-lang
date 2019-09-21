%vars Y,X,V0,V1,V2,V3,V4,V5,V6,V7,V8
%specvar X 23

V0-- ; start of macro zero_assign (zero V0 ; start of macro assignment (assign V0 X ; start of macro is_even (iseven X Y)))
if V0 not 0 goto 0
skip ; end of macro zero_assign
if X not 0 goto 7
V5++ ; start of macro unconditional_branch (goto L6)
if V5 not 0 goto 13
skip ; end of macro unconditional_branch
X--
V0++
V1++
V6++ ; start of macro unconditional_branch (goto L4)
if V6 not 0 goto 3
skip ; end of macro unconditional_branch
if V1 not 0 goto 17
V7++ ; start of macro unconditional_branch (goto L3)
if V7 not 0 goto 22
skip ; end of macro unconditional_branch
V1--
X++
V8++ ; start of macro unconditional_branch (goto L6)
if V8 not 0 goto 13
skip ; end of macro unconditional_branch
skip ; end of macro assignment
if V0 not 0 goto 33 ; start of macro ig (ig V0 L1)
skip ; end of macro ig
Y-- ; start of macro zero_assign (zero Y ; start of macro unit (unit Y))
if Y not 0 goto 25
skip ; end of macro zero_assign
Y++
skip ; end of macro unit
V2++ ; start of macro unconditional_branch (goto L0)
if V2 not 0 goto 53
skip ; end of macro unconditional_branch
V0--
if V0 not 0 goto 42 ; start of macro ig (ig V0 L2)
skip ; end of macro ig
Y-- ; start of macro zero_assign (zero Y)
if Y not 0 goto 36
skip ; end of macro zero_assign
V3++ ; start of macro unconditional_branch (goto L0)
if V3 not 0 goto 53
skip ; end of macro unconditional_branch
V0--
if V0 not 0 goto 33 ; start of macro ig (ig V0 L1)
skip ; end of macro ig
Y-- ; start of macro zero_assign (zero Y ; start of macro unit (unit Y))
if Y not 0 goto 45
skip ; end of macro zero_assign
Y++
skip ; end of macro unit
V4++ ; start of macro unconditional_branch (goto L0)
if V4 not 0 goto 53
skip ; end of macro unconditional_branch
skip ; end of macro is_even
exit