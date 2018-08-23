:- dynamic true/1.
:- dynamic does/2.

%karty
card(zombie(2,Krzysztof)).	%2x
card(zombie(3,Arkadiusz)).	%6x
card(zombie(4,Mariusz)).	%3x
card(zombie(5,Iwan)).		%5x


card(human(chuck)).

tymczasowe_karty([siec,zapora]).
karta_jest_tymczasowa(C) :-
  tymczasowe_karty(TC),
  member(C,TC).

implement.

role(zombies).
role(humans).

/* plansza
 * barykada
 *		  ulica 1   2  3
 * przecznica 1 [] [] [] 
 * przecznica 2 [] [] [] 
 * przecznica 3 [] [] [] 
 * przecznica 4 [] [] [] 
 * przecznica 5 [] [] [] 
 * cmentarz 
 * cell(przecznica,ulica,karta).
 * cell(przecznica,ulica,puste).
 */

init(cell(1,1,puste)).
init(cell(1,2,puste)).
init(cell(1,3,puste)).
init(cell(2,1,puste)).
init(cell(2,2,puste)).
init(cell(2,3,puste)).
init(cell(3,1,puste)).
init(cell(3,2,puste)).
init(cell(3,3,puste)).
init(cell(4,1,puste)).
init(cell(4,2,puste)).
init(cell(4,3,puste)).
init(cell(5,1,puste)).
init(cell(5,2,puste)).
init(cell(5,3,puste)).

init(cemetary([])).
init(barricade([])).
init(zombie_deck(D)) :- all_zombie_cards(D1), shuffle(D1,D).
init(humans_deck(D)) :- all_humans_cards(D1), shuffle(D1,D).
init(thrash([])).
init(control(zombies)).
init(turn(new_cards)).

/*
 * LEGAL MOVES
 */
 
 
/*
 * NEXT STATE
 */

%kolejność graczy

next(control(humans)) :-
	true(control(zombies)),
	true(faza(play_3rd_card)).
next(control(zombies)) :-
	true(control(humans)),
	true(faza(play_3rd_card)).
	
%kolejność tur
next(faza(ruch)) :- true(faza(sprzatanie)).
next(faza(new_cards)) :- true(faza(movement)).
next(faza(discard)) :- true(faza(new_cards)).
next(faza(use_1st_card)) :- true(faza(discard)).
next(faza(use_2nd_card)) :- true(faza(play_1st_card)).
next(faza(use_3rd_card)) :- true(faza(play_2nd_card)).
next(faza(sprzatanie)) :- true(faza(play_3rd_card)).

%faza sprzatanie
next(cell(X,Y,puste)) :-
	true(faza(sprzatanie)),
	true(cell(X,Y,Card)),
	karta_jest_tymczasowa(card).
next(cell(X,Y,C)) :- 
	true(cell(X,Y,Z)).
next(cemetary(X)) :- 
	true(cemetary(X)).
next(barricade(X))) :-
	true(barricade(X)).
next(trash(X)) :-
	true(trash(X)).

%poruszanie karty
next(cell(X,Y,Card)) :-
	is_movable_card(Card),
	is_zombies_card(Card),
	X1 is X 
	true(cell(

%chuck norris

%terror
next(terrorized) :- does(zombies,play_card(terror)).

next(