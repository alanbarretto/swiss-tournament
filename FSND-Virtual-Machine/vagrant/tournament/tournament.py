#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()
    
def deletePlayers():
    """Remove all the player records from the database."""

    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM registered_players;")
    db.commit()
    db.close()
    
def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) from registered_players;")
    count = int(cursor.fetchone()[0])
    db.close()
    return count


def registerPlayer(player):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    cursor = db.cursor()
    register_sql = "INSERT INTO registered_players (name) VALUES (%s);"
    register_player = (player,)
    cursor.execute(register_sql, register_player)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()

    """This query will first join the registered_players table, the matches table, and the 
    match_count view to create the player standings table ordered by wins and matches 
    descending."""

    cursor.execute("SELECT players.id, players.name, Count(matches.winner) as \
        wins, (Case When match_count.matches is null then 0 Else match_count.matches \
        End) as matches from registered_players players left join matches on \
        players.id = matches.id1 left join match_count on players.id = match_count.id \
        group by 1, 2, 4 order by wins desc;")
    
    report = cursor.fetchall()
    db.close()
    return report

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = connect()
    cursor = db.cursor()
    win_sql = "SELECT name from registered_players where id = (%s);"
    lose_sql = "SELECT name from registered_players where id = (%s);"
    player_win = cursor.execute(win_sql, (winner,))
    winner_name = cursor.fetchone()
    player_lose = cursor.execute(lose_sql, (loser,))
    loser_name = cursor.fetchone()
    report_sql = "Insert into matches Values ((%s), (%s), (%s), (%s));"
    report_match = cursor.execute(report_sql, (winner, winner_name, loser, loser_name))
    db.commit()
    db.close()
    
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cursor = db.cursor()

    """This query will first join the registered_players table, the matches table, and the 
    match_count view to create the player standings table ordered by wins and matches 
    descending.  This is necessary to determine the order or rank of each player.
    From there, it selects only the id and player name into a new relation which will
    be used to create the touple.
    """
    cursor.execute("SELECT id, name from (SELECT players.id, players.name, \
        Count(matches.winner) as wins, (Case when match_count.matches is null \
        then 0 Else match_count.matches End) as matches from registered_players \
        players left join matches on players.id = matches.id1 left join match_count \
        on players.id = match_count.id group by 1, 2, 4 order by wins desc, \
        matches desc) as standings;")
    
    number_matches = cursor.fetchall()    

    pairing_list = []

    """Loop through the List of touples, skipping every other.  Join each pair 
    into one touple and append it into the empty pairing_list array. Pairing list should
    have the first two touples from number_matches joined into a single touple and 
    appended as its first element.  The next two touples from pairing_list are then 
    joined and appended, and so on. 

    """
   
    for n in range(0, len(number_matches), 2):
    
        pairing_list.append((number_matches[n][0], \
            number_matches[n][1], number_matches[n+1][0], number_matches[n+1][1]))
    
    return pairing_list

    db.close()

  

