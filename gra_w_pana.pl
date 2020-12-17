:- dynamic has_cards/2.
:- dynamic does/2.
:- dynamic true/1.

% Gra przeznaczona dla 2-4 osób.
role(player1).
role(player2).
role(player3).
role(player4).
num_players(3).

%W grze bior¹ udzia³ karty: 9, 10, walet, dama, król, as (tzw. ma³a talia).
card(9-kier).
card(9-karo).
card(9-pik).
card(9-trefl).
card(10-kier).
card(10-karo).
card(10-pik).
card(10-trefl).
card(walet-kier).
card(walet-karo).
card(walet-pik).
card(walet-trefl).
card(dama-kier).
card(dama-karo).
card(dama-pik).
card(dama-trefl).
card(król-kier).
card(król-karo).
card(król-pik).
card(król-trefl).
card(as-kier).
card(as-karo).
card(as-pik).
card(as-trefl).

card_value(9,9).
card_value(10,10).
card_value(walet,11).
card_value(dama,12).
card_value(król,13).
card_value(as,14).

all_cards(List) :- findall(X,card(X),List).

% initial state
init(true(stack([]))).
%how to get random list here? or
init(true(has_cards(player1,[]))).

/*Starszeñstwo kart w kolejnoœci od najm³odszej do najstarszej:
9, 10, walet, dama, król, as
(kolory nie maj¹ znaczenia) */
card_is_higher(A-_,B-_) :- card_value(A,Va), card_value(B,Vb), Va > Vb.
card_is_equal(A-_,B-_)  :- card_value(A,Va), card_value(B,Vb), Va == Vb.
card_is_lower(A-_,B-_)  :- card_value(A,Va), card_value(B,Vb), Va < Vb.
card_is_not_lower(A-_,B-_)  :- card_value(A,Va), card_value(B,Vb), Va >= Vb.

% Karty s¹ rozdzielane po równo miêdzy wszystkich graczy.
initial_num_cards(Nc) :- num_players(Np), Nc is 24 div Np.

/* Rozpoczyna gracz, który posiada 9 kier¦,
 * wyk³adaj¹c j¹ (odkryt¹) na stó³ */
is_starting_player(Player) :-
  has_cards(Player,Cards),
  member(9-kier,Cards).

% gracze dok³adaj¹ karty kolejno, zgodnie z ruchem wskazówek zegara.

next_player(player1,player2).
next_player(player2,player3) :- num_players(N), N >= 3.
next_player(player2,player1) :- num_players(N), N < 3.
next_player(player3,player4) :- num_players(N), N == 4.
next_player(player3,player1) :- num_players(N), N < 4.

%Wyk³adane karty tworz¹ STOS.

/* Karty wyk³adane na stos nie mog¹ byæ m³odsze od karty znajduj¹cej siê na szczycie stosu.
Starszeñstwo kart w kolejnoœci od najm³odszej do najstarszej: 9, 10, walet, dama, król, as (kolory nie maj¹ znaczenia).
Przyk³ad: Jeœli na szczycie stosu znajduje siê dama,
gracz mo¿e wy³o¿yæ inn¹ damê, króla b¹dŸ asa;
nie mo¿e dziewi¹tki, dziesi¹tki ani waleta. */

%Na stos mo¿na wy³o¿yæ dok³adnie jedn¹ kartê
can_play_card(9-kier,[]).
can_play_card(Card,[Top|_]) :-
  card_is_not_lower(Card,Top).

/*Dotyczy to równie¿ gracza, który rozpoczyna --
mo¿e on zamiast 9 kier wy³o¿yæ wszystkie cztery dziewi¹tki
jeœli posiada (karty wy³o¿one s¹ wtedy w ten sposób,
¿e 9 kier znajduje siê na samym spodzie stosu) */

can_play_cards([9-kier,9-_,9-_,9-_],[]).

/*Istnieje tak¿e wyj¹tek, kiedy mo¿liwe jest wy³o¿enie trzech kart --
jeœli na stosie znajduje siê tylko 9 kier,
mo¿na wy³o¿yæ pozosta³e trzy 9 za jednym razem.*/

can_play_cards([9-_,9-_,9-_],[9-kier|_]).

%albo dok³adnie cztery jednakowej wartoœci (np. cztery asy, cztery dziesi¹tki).
can_play_cards([X-_,X-_,X-_,X-_],[Top|_]) :-
  card_is_not_lower(X-_,Top).

put_cards_on_stack(C,S,NS) :- append(C,S,NS).
take_cards_from_stack(C,S,NS) :- false.

subset2([],[]).
subset2([X|L],[X|S]) :-
  subset2(L,S).
subset2(L, [_|S]) :-
  subset2(L,S).

legal(Player,play_cards([Card])) :-
  has_cards(Player,Hand),
  true(stack(Stack)),
  member(Card,Hand),
  can_play_card(Card,Stack).

legal(Player,play_cards(C)) :-
  has_cards(Player,Hand),
  true(stack(Stack)),
  subset2(C,Hand),
  can_play_cards(C,Stack).

legal(_,take_cards(Cards)) :-
  true(stack(Stack)),
  take_from_stack(Stack,Cards).

take_from_stack([9-karo],[]).
take_from_stack([X,9-karo],[X]).
take_from_stack([X,Y,9-karo],[X,Y]).
take_from_stack([X,Y,Z|T],[X,Y,Z]) :- length(T,N), N >= 1.

/*Gracz, który nie chce lub nie mo¿e wy³o¿yæ karty (ma tylko m³odsze ni¿ ta, znajduj¹ca siê na szczycie stosu), pobiera ze stosu trzy karty. Jeœli na stosie znajduj¹ siê trzy karty lub mniej, pobierane s¹ wszystkie poza 9 kier. Po pobraniu kart kolejka przechodzi do nastêpnego gracza.*/

%Celem gry jest wy³o¿enie wszystkich posiadanych kart.


%only for testing
has_cards(player1,[9-pik,9-karo]).
has_cards(player2,[10-trefl,walet-trefl,dama-pik]).
has_cards(player3,[10-kier,as-kier,9-kier]).

has_cards(player4,[9-karo,9-pik,9-trefl]).
has_cards(player5,[dama-kier,dama-trefl,dama-karo,dama-pik]).

















