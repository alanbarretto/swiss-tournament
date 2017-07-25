#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

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
    cursor.execute("SELECT * from standings;")
    
    standings_report = cursor.fetchall()
    db.close()
    return standings_report

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
    report_sql = "Insert into matches (winner_id, loser_id) Values ((%s), (%s));"
    report_match = cursor.execute(report_sql, (winner, loser))
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
   
    number_matches = playerStandings()    
    pairing_list = []

    """Since the touples are already ordered, take the touples two at a time from the 
    start of the list, take only the first two elements in each, group them into a single 
    touple, then append into the empty pairing_list. 

    """
   
    for n in range(0, len(number_matches), 2):
        pairing_list.append((number_matches[n][0], \
            number_matches[n][1], number_matches[n+1][0], number_matches[n+1][1]))
    
    return pairing_list
    db.close()

  


