%vars Y,X,V0,V1,V2,V3
%specvar X 3

if X not 0 goto 10
skip
Y--
if Y not 0 goto 2
skip
Y++
skip
V0++
if V0 not 0 goto 31
skip
X--
if X not 0 goto 16
skip
V1++
if V1 not 0 goto 27
skip
X--
if X not 0 goto 10
skip
Y--
if Y not 0 goto 19
skip
Y++
skip
V2++
if V2 not 0 goto 31
skip
skip
V3++
if V3 not 0 goto 27
skip
exit