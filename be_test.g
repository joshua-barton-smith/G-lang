%vars Y,X,X2,V0,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26
%specvar X 3
%specvar X2 2

V0-- ; start of macro zero_assign (zero V0 ; start of macro assignment (assign V0 X ; start of macro branch_equal (be X X2 L1)))
if V0 not 0 goto 0
skip ; end of macro zero_assign
if X not 0 goto 7
V13++ ; start of macro unconditional_branch (goto L13)
if V13 not 0 goto 13
skip ; end of macro unconditional_branch
X--
V0++
V4++
V14++ ; start of macro unconditional_branch (goto L11)
if V14 not 0 goto 3
skip ; end of macro unconditional_branch
if V4 not 0 goto 17
V15++ ; start of macro unconditional_branch (goto L10)
if V15 not 0 goto 22
skip ; end of macro unconditional_branch
V4--
X++
V16++ ; start of macro unconditional_branch (goto L13)
if V16 not 0 goto 13
skip ; end of macro unconditional_branch
skip ; end of macro assignment
V1-- ; start of macro zero_assign (zero V1 ; start of macro assignment (assign V1 X2))
if V1 not 0 goto 23
skip ; end of macro zero_assign
if X2 not 0 goto 30
V17++ ; start of macro unconditional_branch (goto L18)
if V17 not 0 goto 36
skip ; end of macro unconditional_branch
X2--
V1++
V5++
V18++ ; start of macro unconditional_branch (goto L16)
if V18 not 0 goto 26
skip ; end of macro unconditional_branch
if V5 not 0 goto 40
V19++ ; start of macro unconditional_branch (goto L15)
if V19 not 0 goto 45
skip ; end of macro unconditional_branch
V5--
X2++
V20++ ; start of macro unconditional_branch (goto L18)
if V20 not 0 goto 36
skip ; end of macro unconditional_branch
skip ; end of macro assignment
if V0 not 0 goto 50 ; start of macro branch_zero (bz V0 L2)
V21++ ; start of macro unconditional_branch (goto L2)
if V21 not 0 goto 54
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V6++ ; start of macro unconditional_branch (goto L3)
if V6 not 0 goto 65
skip ; end of macro unconditional_branch
if V1 not 0 goto 58 ; start of macro branch_zero ([L2] bz V1 L4)
V22++ ; start of macro unconditional_branch (goto L4)
if V22 not 0 goto 62
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V7++ ; start of macro unconditional_branch (goto L0)
if V7 not 0 goto 99
skip ; end of macro unconditional_branch
V8++ ; start of macro unconditional_branch ([L4] goto L1)
if V8 not 0 goto 103
skip ; end of macro unconditional_branch
V0--
if V0 not 0 goto 70 ; start of macro branch_zero (bz V0 L5)
V23++ ; start of macro unconditional_branch (goto L5)
if V23 not 0 goto 74
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V9++ ; start of macro unconditional_branch (goto L6)
if V9 not 0 goto 82
skip ; end of macro unconditional_branch
if V1 not 0 goto 78 ; start of macro branch_zero ([L5] bz V1 L0)
V24++ ; start of macro unconditional_branch (goto L0)
if V24 not 0 goto 99
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V10++ ; start of macro unconditional_branch (goto L6)
if V10 not 0 goto 82
skip ; end of macro unconditional_branch
V1--
if V0 not 0 goto 87 ; start of macro branch_zero (bz V0 L7)
V25++ ; start of macro unconditional_branch (goto L7)
if V25 not 0 goto 91
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V11++ ; start of macro unconditional_branch (goto L3)
if V11 not 0 goto 65
skip ; end of macro unconditional_branch
if V1 not 0 goto 95 ; start of macro branch_zero ([L7] bz V1 L1)
V26++ ; start of macro unconditional_branch (goto L1)
if V26 not 0 goto 103
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V12++ ; start of macro unconditional_branch (goto L0)
if V12 not 0 goto 99
skip ; end of macro unconditional_branch
skip ; end of macro branch_equal
V2++ ; start of macro unconditional_branch (goto E)
if V2 not 0 goto 107
skip ; end of macro unconditional_branch
Y++
V3++ ; start of macro unconditional_branch (goto E)
if V3 not 0 goto 107
skip ; end of macro unconditional_branch
exit