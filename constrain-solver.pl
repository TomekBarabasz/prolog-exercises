:- use_module(library(clpfd)).

test(X,Y):-
    X in 0..10,
    Y in 5..8,
    X #> Y.

not_first(_,[]).
not_first(X,[F|_]):-X\=F.
%moveone([L],[],[],[L],left2right).
moveRight([F|T],[],T,[F],F).
moveRight([Fl|Tl],[Fr|Tr],Tl,[Fl,Fr|Tr],Fl):-Fl#<Fr.
moveLeft([],[F|T],[F],T,F).
moveLeft([Fl|Tl],[Fr|Tr],[Fr,Fl|Tl],Tr,Fr):-Fr#<Fl.

move(L1,C1,R1,L,C,R,Moves):-
    move1(L1,C1,R1,L,C,R,x,[],Mr),
    rev(Mr,Moves).
move1(L,C,R,L,C,R,_,Moves,Moves).
/*
move1(L1,C1,R1,L,C,R,Prev,Sub,Moves):-
    (moveRight(L1,C1,L2,C2,E),R2=R1,E\=Prev,P=l2c+E,\+member(P,Sub);
     moveRight(L1,R1,L2,R2,E),C2=C1,E\=Prev,P=l2r+E,\+member(P,Sub);
     moveRight(C1,R1,C2,R2,E),L2=L1,E\=Prev,P=c2r+E,\+member(P,Sub)),
     move1(L2,C2,R2,L,C,R,E,[P|Sub],Moves).
move1(L1,C1,R1,L,C,R,Prev,Sub,Moves):-
    (moveLeft(L1,C1,L2,C2,E),R2=R1,E\=Prev,P=c2l+E,\+member(P,Sub);
     moveLeft(L1,R1,L2,R2,E),C2=C1,E\=Prev,P=r2l+E,\+member(P,Sub);
     moveLeft(C1,R1,C2,R2,E),L2=L1,E\=Prev,P=r2c+E,\+member(P,Sub)),
     move1(L2,C2,R2,L,C,R,E,[P|Sub],Moves).
*/
%move1(L1,C1,R1,L,C,R,Prev,Sub,Moves).

hanoi(L,C,R,Moves):-
    hanoi1(L,C,R,x,[],Mr),
    rev(Mr,Moves).
hanoi_ok([],[],[1,2,3],Moves,Moves).
get_first([F|_],F).
can_move(A,Prev,Dir,Sub,M,E):-
    get_first(A,E),
    E\=Prev,
    M=E+Dir.
    %\+member(M,Sub).
mv(A,B,C,D):-moveRight(A,B,C,D,_).
dump(L,C,R,P,S):-
  write('L='),write(L),
  write('C='),write(C),
  write('R='),write(R),
  write('Pr='),write(P),
  write('Mv='),write(S),nl.

hanoi1(L,C,R,Prev,Sub,Moves):-
    dump(L,C,R,Prev,Sub),
    hanoi_ok(L,C,R,Sub,Moves);
   ((can_move(L,Prev,lc,Sub,M,E),mv(L,C,L1,C1),R1=R);
    (can_move(L,Prev,lr,Sub,M,E),mv(L,R,L1,R1),C1=C);
    (can_move(C,Prev,cr,Sub,M,E),mv(C,R,C1,R1),L1=L);
    (can_move(C,Prev,cl,Sub,M,E),mv(C,L,C1,L1),R1=R);
    (can_move(R,Prev,rc,Sub,M,E),mv(R,C,R1,C1),L1=L);
    (can_move(R,Prev,rl,Sub,M,E),mv(R,L,R1,L1),C1=C)),
    hanoi1(L1,C1,R1,E,[M|Sub],Moves).


adj(1,2).
adj(1,3).
adj(1,4).
adj(1,5).
adj(2,3).
adj(2,4).
adj(3,4).
adj(4,5).
adjacent(X,Y):-adj(X,Y);adj(Y,X).

alldifferent([],_).
alldifferent([F|T],L):-
    \+ member(F,L),
    alldifferent(T,L).









































