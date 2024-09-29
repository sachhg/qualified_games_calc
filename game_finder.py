"""
Given the following inputs:
- <game_data> is a list of dictionaries, with each dictionary representing a player's shot attempts in a game. The list can be empty, but any dictionary in the list will include the following keys: gameID, playerID, gameDate, fieldGoal2Attempted, fieldGoal2Made, fieldGoal3Attempted, fieldGoal3Made, freeThrowAttempted, freeThrowMade. All values in this dictionary are ints, except for gameDate which is of type str in the format 'MM/DD/YYYY'
- <true_shooting_cutoff> is the minimum True Shooting percentage value for a player to qualify in a game. It will be an int value >= 0.
- <player_count> is the number of players that need to meet the <true_shooting_cutoff> in order for a gameID to qualify. It will be an int value >= 0.

Implement find_qualified_games to return a list of unique qualified gameIDs in which at least <player_count> players have a True Shooting percentage >= <true_shooting_cutoff>, ordered from most to least recent game.
"""

from datetime import datetime

def true_shooting(attempted2, made2, attempted3, made3, attemptedFT, madeFT):
  points = (made2 * 2) + (made3 * 3) + (madeFT * 1)
  fieldGoalsAttempted = attempted2 + attempted3
  return 100 * (points / (2 * (fieldGoalsAttempted + (0.44 * attemptedFT))))

def find_qualified_games(game_data: list[dict], true_shooting_cutoff: int, player_count: int) -> list[int]:
  if not game_data: #checks for base case
    return []

  sorted_games = sorted(game_data, key=lambda x: datetime.strptime(x['gameDate'], '%m/%d/%Y'), reverse=True) # sorts games by date, newest first
  qualified_games = []  # list to store qualified games - to be final output later
  current_gameID = sorted_games[0]['gameID'] # int representing the current gameID being checked, starts as gameID of first item in sorted_games list
  tsp_for_game = []  # list for storing TSPs of current game

  for item in sorted_games:
    if item['gameID'] == current_gameID:
      # calculate TSP for the current player in the same game
      tsp_for_game.append(true_shooting(item['fieldGoal2Attempted'], item['fieldGoal2Made'], item['fieldGoal3Attempted'], item['fieldGoal3Made'], item['freeThrowAttempted'], item['freeThrowMade']))
    else:
      # check if the current game qualifies, add to qualified_games if so
      if sum(1 for tsp in tsp_for_game if tsp >= true_shooting_cutoff) >= player_count:
        qualified_games.append(current_gameID)

      # reset to check a new game
      current_gameID = item['gameID']
      tsp_for_game = [true_shooting(item['fieldGoal2Attempted'], item['fieldGoal2Made'], item['fieldGoal3Attempted'], item['fieldGoal3Made'], item['freeThrowAttempted'], item['freeThrowMade'])]

  # check the last game after the loop ends
  if sum(1 for tsp in tsp_for_game if tsp >= true_shooting_cutoff) >= player_count:
    qualified_games.append(current_gameID)

  return qualified_games
