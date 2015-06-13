from itertools import chain
from django.db import models
from collections import Counter
import itertools

#TODO
#clean up the winning_combos property
#add suite of tests

class Game(models.Model):
    computer = models.ForeignKey('Computer', related_name='games', default=lambda: Computer.objects.get_or_create(id=1)[0])

    class Meta:
        app_label = 'tic_tac_toe'

    def set_up_tiles(self):
        tile_list = list(chain.from_iterable(('a'+str(x), 'b'+str(x), 'c'+str(x)) for x in range(1, 4)))
        for position in tile_list:
            tile = Tile(position=position, game=self)
            tile.save()

    def set_up_winning_combos(self):
        for combo in self.winning_combos_property:
            winning_combo = WinningCombo(game=self)
            winning_combo.save()
            for tile in combo:
                winning_combo.tiles.add(tile)



    @property
    def winning_combos_property(self):
        """
         Returns a list of all combination of moves that can win a game. I use this as a constant and also to whittle
         down potential combos.
        """
        alpha = 'abc'
        num = '123'
        all_tiles = self.tiles.all()
        winning_combos = []
#        winning_combo = WinningCombo()
        new_combo = [tile for tile in all_tiles if tile.position[0] == 'a']
        winning_combos.append(new_combo)
        new_combo = [tile for tile in all_tiles if tile.position[0] == 'b']
        winning_combos.append(new_combo)
        new_combo = [tile for tile in all_tiles if tile.position[0] == 'c']
        winning_combos.append(new_combo)
        new_combo = [tile for tile in all_tiles if tile.position[1] == '1']
        winning_combos.append(new_combo)
        new_combo = [tile for tile in all_tiles if tile.position[1] == '2']
        winning_combos.append(new_combo)
        new_combo = [tile for tile in all_tiles if tile.position[1] == '3']
        winning_combos.append(new_combo)

        x_list = []
        for n in num:
            tile = self.tiles.filter(position=alpha[int(n)-1] + n).select_related('player')[0]
            x_list.append(tile)
        winning_combos.append(x_list)

        x_list = []
        alpha = alpha[::-1]
        for n in num:
            x = self.tiles.filter(position=alpha[int(n)-1] + n)[0]
            x_list.append(x)
        winning_combos.append(x_list)

        return list(winning_combos)


    def available_combos(self):
        combos = WinningCombo.objects.filter(tiles__in=self.tiles_open).prefetch_related('tiles')
        return combos


    def valid_computer_combos(self):
        """
        Determines which combination of winning moves are still available to the computer
        """
        win_list = list(self.available_combos().distinct())
#        win_list = []
        # Cycle through winning combos. if player doesn't own a single tile in that combo, add it to the win_list
        for combo in win_list:
            for tile in combo.tiles.all():
                if tile.player:
                    win_list.remove(combo)

        for combo in win_list:
            for tile in combo.tiles.all():
                if tile.player:
                    win_list.remove(combo)
        return win_list

#        for combo in self.winning_combos_property:
#            if not combo[0].player and not combo[1].player and not combo[2].player:
#                win_list.append(combo)
#        return win_list

    def valid_player_combos(self):
        """
        Determines which combination of winning moves are available to the player. This helps the computer figure out
        if he needs to block a move
        """
#        win_list = []
        # Cycle through winning combos. if computer doesn't own a single tile in that combo, add it to the win_list
#        for combo in self.winning_combos_property:
#            if not combo[0].computer and not combo[1].computer and not combo[2].computer:
#                win_list.append(combo)
#        return win_list
        win_list = list(self.available_combos().distinct())
#        win_list = []
        # Cycle through winning combos. if player doesn't own a single tile in that combo, add it to the win_list
        for combo in win_list:
            for tile in combo.tiles.all():
                if tile.computer:
                    try:
                        win_list.remove(combo)
                    except:
                        pass

        for combo in win_list:
            for tile in combo.tiles.all():
                if tile.computer:
                    win_list.remove(combo)
        return win_list


    def center_tile(self):
        """
        If the center tile is available, return that tile. Return it because the center tile not only gives a player
        the most options to win, but also blocks the most moves by an opponent
        """
        try:
            tile = Tile.objects.get(position='b2', player__isnull=True, computer__isnull=True, game=self)
            return tile
        except Exception:
            return

    def get_most_common_tile(self):
        """
        Get the most common tile that appears in avenues for the computer to win.
        """
        # Here we make just a flattened list of possible winning tile combinations for the computer so we can find out
        # which tile appears in the most combos. Then we return the first result in a list of the most common tiles.
        n = [tile for combo in self.winning_combos_property for tile in combo if (not tile.player and not tile.computer)]
        count = Counter(n)
        if n:
            return count.most_common(1)[0][0]
        else:
            return self.tiles_open[0]


    def guaranteed_player_win_in_3_moves(self):
        """
        Returns a list of the tiles a player could make now that guarantees a win in two additional moves. If this is
        filled, Computer must prevent moves in these ALL of the tiles in this list.
        """
        tiles = []
        potential_danger_combos = []
        for combo in self.valid_player_combos():
            for tile in combo.tiles.all():
                if tile.player:
#            if combo[0].player or combo[1].player or combo[2].player:
                    potential_danger_combos.append(combo)
        for tile in self.tiles_open:
            num_combos = 0
            for combo in potential_danger_combos:
                if tile in combo.tiles.all():
                    num_combos += 1
                    if num_combos == 2:
                        tiles.append(tile)
        return tiles


    def force_player_move(self):
        """
        This is the most complicated logic in the app. We have to determine which move is best here to account for various
        permutations that could give the player a win.

        Finds moves that will win for the computer in two moves, since the player can win in three moves. This builds off
        of guaranteed_player_win_in_3_moves().
        """
        dangerous_player_combos = []
        danger_tiles = list(self.guaranteed_player_win_in_3_moves())

        # Here we cycle through the tiles that give the player a guaranteed win in 2 more moves and also all the
        # tiles in all winning combos to see if any of them correlate. If they do, we add all the possible combos
        # to the player_win_combo list to iterate through below.
        for tile in danger_tiles:
            for combo in self.valid_player_combos():
                for combo_tile in combo.tiles.all():
                    if tile == combo_tile:
                        dangerous_player_combos.append(combo)

        if len(danger_tiles) > 1:
            if (danger_tiles[0].position == 'a1' and danger_tiles[1].position == 'c3') or (danger_tiles[0].position == 'c1' and danger_tiles[1].position == 'a3'):
                for combo in dangerous_player_combos:
                    for tile in combo.tiles.all():
                        if tile not in danger_tiles and (not tile.player and not tile.computer):
                            return tile
            else:
                return danger_tiles[0]
        else:
            return danger_tiles[0]


    def kill_shot(self):
        """
        Determines if the computer has any move that will win it for him with one move.
        """
#        for combo in self.valid_computer_combos():
#        tile = Tile.winning_combos.filter(game=self, computer=None, player=None)
#        select tile where not tile.computer and not tile.player and tile in combo and tile1.computer and tile2.computer
        for combo in self.winning_combos_property:
            num_tiles = 0
            for tile in combo:
                if tile.computer:
                    num_tiles += 1
                if num_tiles == 2:
#                    tile = Tile.objects.get(game=self, computer=None, player=None)
                    for tile in combo:
                        if not tile.computer and not tile.player:
                            return tile


    def player_wins_next_turn(self):
        """
        Returns a list of possible tile combinations that allow the player to win next turn. We use this to
        determine if the computer needs to make an emergency move to block the player from winning. If this has more
        than one combo in it, computer is potentially in trouble.
        """
        danger_zone_combos = []
        for combo in self.valid_player_combos():
            num_tiles_in_combo = 0
            for tile in combo.tiles.all():
                if tile.player:
                    num_tiles_in_combo += 1
                if num_tiles_in_combo == 2:
                    danger_zone_combos.append(combo)
        return danger_zone_combos


    def last_tile_for_player_to_win(self):
        """
        If a player has one move left to win the game, this finds the tile that player can win with. Used to block the
        player's move if possible
        """
        for combo in self.player_wins_next_turn():
            for tile in combo.tiles.all():
                if not tile.computer and not tile.player:
                    return tile


    @property
    def tiles_open(self):
        open_tiles = Tile.objects.filter(game=self, player__isnull=True, computer__isnull=True)
#        open_tiles = [tile for tile in self.tiles.all() if (not tile.player and not tile.computer)]
        return open_tiles

    @property
    def winner(self):
        winner = None
        winning_combos = self.winning_combos_property
        for combo in winning_combos:
            if combo[0].player and combo[1].player and combo[2].player:
                winner = self.player
            elif combo[0].computer and combo[1].computer and combo[2].computer:
                winner = self.computer
        return winner




class Player(models.Model):
    game = models.OneToOneField('Game', related_name='player')

    @property
    def avatar(self):
        return u'x'

    def __unicode__(self):
        return 'Player'

    class Meta:
        app_label = 'tic_tac_toe'


class Computer(models.Model):
    def __unicode__(self):
        return 'Computer'

    class Meta:
        app_label = 'tic_tac_toe'

    @property
    def avatar(self):
        return u'o'


class Tile(models.Model):
    position = models.CharField(max_length=10)
    player = models.ForeignKey('Player', related_name='moves', null=True, default=None)
    computer = models.ForeignKey('Computer', related_name='moves', null=True, default=None)
    game = models.ForeignKey('Game', related_name='tiles', null=True, default=None)

    class Meta:
        app_label = 'tic_tac_toe'

    def __unicode__(self):
        return self.position


class WinningCombo(models.Model):
    tiles = models.ManyToManyField('Tile', related_name='winning_combos')
    game = models.ForeignKey('Game', related_name='winning_combos')

    class Meta:
        app_label = 'tic_tac_toe'



def generate_tile_position_values():
    alpha = 'abc'
    numbers = '123'
    len2 = itertools.product(alpha, numbers)
    positions = [''.join(p) for p in itertools.chain(len2)]
    return positions

def all_combos():
    return list(itertools.combinations(generate_tile_position_values(), 3))





