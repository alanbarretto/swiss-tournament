Create Table registered_players (
	id serial primary key,
	name text
);

Create Table matches (
	id1 integer REFERENCES registered_players (id),
	winner text,
	id2 integer REFERENCES registered_players (id),
	loser text
);


-- creates a view with two columns: id, and matches (total matches for each player)

Create View match_count as (Select player.id, Count(total.name) as matches from 
	registered_players player  left join (Select a.id1 as id, a.winner as name
	from matches a UNION ALL Select b.id2 as id, b.loser as name from matches b) 
	total on player.id = total.id group by 1);





