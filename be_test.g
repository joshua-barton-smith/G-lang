%vars Y,X,X2,V0,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27
%specvar X 3
%specvar X2 2

V2-- ; start of macro zero_assign (zero V2 ; start of macro assignment (assign V2 X ; start of macro branch_equal (be X X2 L0 ; start of macro branch_not_equal (bne X X2 L1))))
if V2 not 0 goto 0
skip ; end of macro zero_assign
if X not 0 goto 7
V14++ ; start of macro unconditional_branch (goto L15)
if V14 not 0 goto 13
skip ; end of macro unconditional_branch
X--
V2++
V5++
V15++ ; start of macro unconditional_branch (goto L13)
if V15 not 0 goto 3
skip ; end of macro unconditional_branch
if V5 not 0 goto 17
V16++ ; start of macro unconditional_branch (goto L12)
if V16 not 0 goto 22
skip ; end of macro unconditional_branch
V5--
X++
V17++ ; start of macro unconditional_branch (goto L15)
if V17 not 0 goto 13
skip ; end of macro unconditional_branch
skip ; end of macro assignment
V3-- ; start of macro zero_assign (zero V3 ; start of macro assignment (assign V3 X2))
if V3 not 0 goto 23
skip ; end of macro zero_assign
if X2 not 0 goto 30
V18++ ; start of macro unconditional_branch (goto L20)
if V18 not 0 goto 36
skip ; end of macro unconditional_branch
X2--
V3++
V6++
V19++ ; start of macro unconditional_branch (goto L18)
if V19 not 0 goto 26
skip ; end of macro unconditional_branch
if V6 not 0 goto 40
V20++ ; start of macro unconditional_branch (goto L17)
if V20 not 0 goto 45
skip ; end of macro unconditional_branch
V6--
X2++
V21++ ; start of macro unconditional_branch (goto L20)
if V21 not 0 goto 36
skip ; end of macro unconditional_branch
skip ; end of macro assignment
if V2 not 0 goto 50 ; start of macro branch_zero (bz V2 L5)
V22++ ; start of macro unconditional_branch (goto L5)
if V22 not 0 goto 54
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V7++ ; start of macro unconditional_branch (goto L6)
if V7 not 0 goto 65
skip ; end of macro unconditional_branch
if V3 not 0 goto 58 ; start of macro branch_zero ([L5] bz V3 L7)
V23++ ; start of macro unconditional_branch (goto L7)
if V23 not 0 goto 62
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V8++ ; start of macro unconditional_branch (goto L4)
if V8 not 0 goto 99
skip ; end of macro unconditional_branch
V9++ ; start of macro unconditional_branch ([L7] goto L0)
if V9 not 0 goto 103
skip ; end of macro unconditional_branch
V2--
if V2 not 0 goto 70 ; start of macro branch_zero (bz V2 L8)
V24++ ; start of macro unconditional_branch (goto L8)
if V24 not 0 goto 74
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V10++ ; start of macro unconditional_branch (goto L9)
if V10 not 0 goto 82
skip ; end of macro unconditional_branch
if V3 not 0 goto 78 ; start of macro branch_zero ([L8] bz V3 L4)
V25++ ; start of macro unconditional_branch (goto L4)
if V25 not 0 goto 99
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V11++ ; start of macro unconditional_branch (goto L9)
if V11 not 0 goto 82
skip ; end of macro unconditional_branch
V3--
if V2 not 0 goto 87 ; start of macro branch_zero (bz V2 L10)
V26++ ; start of macro unconditional_branch (goto L10)
if V26 not 0 goto 91
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V12++ ; start of macro unconditional_branch (goto L6)
if V12 not 0 goto 65
skip ; end of macro unconditional_branch
if V3 not 0 goto 95 ; start of macro branch_zero ([L10] bz V3 L0)
V27++ ; start of macro unconditional_branch (goto L0)
if V27 not 0 goto 103
skip ; end of macro unconditional_branch
skip ; end of macro branch_zero
V13++ ; start of macro unconditional_branch (goto L4)
if V13 not 0 goto 99
skip ; end of macro unconditional_branch
skip ; end of macro branch_equal
V4++ ; start of macro unconditional_branch (goto L1)
if V4 not 0 goto 107
skip ; end of macro unconditional_branch
skip ; end of macro branch_not_equal
V0++ ; start of macro unconditional_branch (goto E)
if V0 not 0 goto 111
skip ; end of macro unconditional_branch
Y++
V1++ ; start of macro unconditional_branch (goto E)
if V1 not 0 goto 111
skip ; end of macro unconditional_branch
exit