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


-- creates a view called match_count with two columns: id, and total_matches 

Create View match_count as (Select player.id as id, Count(total.name) as total_matches from 
	registered_players player  left join (Select a.id1 as id, a.winner as name
	from matches a UNION ALL Select b.id2 as id, b.loser as name from matches b) 
	total on player.id = total.id group by 1);





