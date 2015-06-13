from django.shortcuts import render, redirect, get_object_or_404
from tic_tac_toe.forms import MoveForm
from tic_tac_toe.models.game import Game, Player, Computer, Tile





def home(request):
    context = {}
    if request.POST:
        if request.POST.get('new_game'):
            game = Game()
            game.save()
            game.set_up_tiles()
            game.set_up_winning_combos()
            player = Player(game=game)
            player.save()
            request.session['game_id'] = game.id
            context['game'] = game
            context['player'] = player
        elif request.POST.get('tile'):
            game = Game.objects.filter(id=request.session['game_id'])[0]
            tile = Tile.objects.get(id=game.tiles.all().filter(position=request.POST.get('tile')))
            game.player.moves.add(tile)

            player = game.player
            player_tiles = game.player.moves.all()
            if game.winner == player:
                context['game_message'] = "%s won" % player
            elif game.tiles_open:
                if game.center_tile():
                    game.computer.moves.add(game.center_tile())
                # If computer can end the game in its favor, do that! Otherwise, just block the player
                elif game.kill_shot():
                    game.computer.moves.add(game.kill_shot())
                elif game.player_wins_next_turn():
                    game.computer.moves.add(game.last_tile_for_player_to_win())
                # If the computer ever has a chance to win the game, do that!
                # If the above conditions arent met, we check to see what moves the player can make that will
                # guarantee the game ending in his favor in two more moves (after this move by the player).
                # Whatever the moves are that will allow the player to do that, the computer uses its algorithm
                # to determine what action to take that will prevent that from happening.
                elif game.guaranteed_player_win_in_3_moves():
                    game.computer.moves.add(game.force_player_move())
                # If none of the other conditions are met, the computer will just take the first tile that appears
                # in a list of tiles that show up in the most possible winning combinations
                else:
                    game.computer.moves.add(game.get_most_common_tile())

            if game.winner == game.computer:
                context['game_message'] = "%s won" % game.computer
            if not game.tiles_open and not game.winner:
                context['game_message'] = "Game was a tie. Better luck next time! (Not really. All hope is lost of you \
                                          winning! Bwahaha)"
            context['game'] = game
            context['player'] = player
            context['player_tiles'] = player_tiles
    else:
        return render(request, 'home.html', context)
    return render(request, 'home.html', context)


