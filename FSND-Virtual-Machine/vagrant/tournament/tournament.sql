Create Table registered_players (
	id serial primary key,
	name text
);

Create Table matches (
	match_id serial primary key,
	winner_id integer REFERENCES registered_players (id),
	loser_id integer REFERENCES registered_players (id)
	
);


-- creates a view called match_count with two columns: id, and total_matches 

Create View match_count as 
Select player.id as id,
	Count(matches.match_id) as total_matches
from registered_players player
left join matches
  	on player.id = matches.winner_id or player.id =  matches.loser_id
  	group by player.id;

-- creates a view called standings with four columns: id, name, wins, matches_played

Create View standings as 
SELECT players.id as id, 
	   players.name as name, 
       Count(matches.winner_id) as wins, 
       (Case When match_count.total_matches is null then 0 Else match_count.total_matches 
        End) as matches_played 
from registered_players players 
left join matches on players.id = matches.winner_id 
left join match_count on players.id = match_count.id 
group by 1, 2, 4 
order by wins desc, matches_played desc;