smierdzi(dupa).
smierdzi(X):-nieumyte(X).
nieumyte(zeby).

accMax([F|T],Acc,Max):-F<Acc,accMax(T,Acc,Max).
accMax([F|T],Acc,Max):-F>=Acc,accMax(T,F,Max).
accMax([],A,A).
max([F|T],Max):-accMax(T,F,Max).

inc([X],[Y]):-Y is X+1.
inc([F|T],[F1|T1]):-F1 is F+1, inc(T,T1).

app(X,[],[X]).
app(X,[F|T],[F|T1]):-app(X,T,T1).

%srev = slow reverse
srev([],[]).
srev([F|T],R):-srev(T,R1),app(F,R1,R).

%faster version
rev(L,R):-accRev(L,[],R).
accRev([F|T],Acc,R):-accRev(T,[F|Acc],R).
accRev([],A,A).

palindrome(X):-rev(X,R),X=R.

edge(1,2).
edge(3,2).
edge(4,3).
connected(A,B):-edge(A,B);edge(B,A).

path(A,B,Path):-
  path1(A,B,[A],P1),
  rev(P1,Path).
path1(A,B,SubPath,[B|SubPath]):-
  connected(A,B).
path1(A,B,SubPath,Path):-
  connected(A,C),
  C\=B,
  \+ member(C,SubPath),
  path1(C,B,[C|SubPath],Path).




















