%vars Y,X,V0,V1,V2,V3
%specvar X 3

if X not 0 goto 10 ; start of macro ig (ig X L)
skip ; end of macro ig
Y-- ; start of macro zero_assign (zero Y ; start of macro unit (unit Y))
if Y not 0 goto 2
skip ; end of macro zero_assign
Y++
skip ; end of macro unit
V0++ ; start of macro unconditional_branch (goto E)
if V0 not 0 goto 30
skip ; end of macro unconditional_branch
X--
if X not 0 goto 16 ; start of macro ig (ig X L2)
skip ; end of macro ig
V1++ ; start of macro unconditional_branch (goto L3)
if V1 not 0 goto 27
skip ; end of macro unconditional_branch
X--
if X not 0 goto 10 ; start of macro ig (ig X L)
skip ; end of macro ig
Y-- ; start of macro zero_assign (zero Y ; start of macro unit (unit Y))
if Y not 0 goto 19
skip ; end of macro zero_assign
Y++
skip ; end of macro unit
V2++ ; start of macro unconditional_branch (goto E)
if V2 not 0 goto 30
skip ; end of macro unconditional_branch
V3++ ; start of macro unconditional_branch ([L3] goto L3)
if V3 not 0 goto 27
skip ; end of macro unconditional_branch
exit