%vars Y,V,X,V0,V1,V2,V3,V4
%specvar X 5

V--
if V not 0 goto 0
skip
if X not 0 goto 7
V1++
if V1 not 0 goto 13
skip
X--
V++
V0++
V2++
if V2 not 0 goto 3
skip
if V0 not 0 goto 17
V3++
if V3 not 0 goto 22
skip
V0--
X++
V4++
if V4 not 0 goto 13
skip
skip
Y--
if Y not 0 goto 23
skip
exit