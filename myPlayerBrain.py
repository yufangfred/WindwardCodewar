import random as rand
import api.units as lib
from api.units import SpecialPowers
from api.units import MapTile

NAME = "DAMA"
SCHOOL = "UMD"


def random_element(list):
    if len(list) < 1:
        print "random element from empty list? returning None..."
        return None
    return list[rand.randint(0, len(list) - 1)]


class MyPlayerBrain(object):
    """The Python AI class."""

    def __init__(self):
        self.name = NAME
        self.school = SCHOOL
        self.cnt = 0
        if NAME is "Anders Hejlsberg" or SCHOOL is "Windward U.":
            print "Please enter your name and university at the top of MyPlayerBrain.py"

            #The player's avatar (looks in the same directory that this module is in).
            #Must be a 32 x 32 PNG file.
        try:
            avatar = open("MyAvatar.png", "rb")
            avatar_str = b''
            for line in avatar:
                avatar_str += line
            avatar = avatar_str
        except IOError:
            avatar = None # avatar is optional
        self.avatar = avatar

    def Setup(self, map, me, hotelChains, players):
        pass #any setup code...

    def is_tile_undeveloped(self, tile):
        return tile.Type == MapTile.UNDEVELOPED

    def QuerySpecialPowersBeforeTurn(self, map, me, hotelChains, players):
        self.cnt += 1
        if self.cnt == 1:
            return SpecialPowers.DRAW_5_TILES
        if self.cnt == 2:
            return SpecialPowers.PLACE_4_TILES
        return SpecialPowers.NONE

    def QueryTileOnly(self, map, me, hotelChains, players):
        tile = random_element(me.tiles)
        createdHotel = next((hotel for hotel in hotelChains if not hotel.is_active), None)
        mergeSurvivor = next((hotel for hotel in hotelChains if hotel.is_active), None)
        return PlayerPlayTile(tile, createdHotel, mergeSurvivor)

 #   def isGood1(self, map, tile):
        
        
    def QueryTileAndPurchase(self, map, me, hotelChains, players):
        inactive = next((hotel for hotel in hotelChains if not hotel.is_active), None)
        turn = PlayerTurn(tile=random_element(me.tiles), created_hotel=inactive, merge_survivor=inactive)
        done = 0
        for x in range(0, map.height):
            for y in range(0, map.width):
                mapTile = map.tiles[x][y]
                if mapTile.type == MapTile.SINGLE:
                    for thisTile in me.tiles:
                        xx = (x - thisTile.x)
                        yy = (y - thisTile.y)
                        if xx * xx + yy * yy == 1:
                            turn.Tile = thisTile
                           # turn.Buy.append(lib.HotelStock(hotelChains[0], 3))
                            #done = 1
                            break 
        if done == 0:  
            turn.Buy.append(lib.HotelStock(random_element(hotelChains), rand.randint(1, 3)))
            turn.Buy.append(lib.HotelStock(random_element(hotelChains), rand.randint(1, 3)))
        
        #turn.Buy.append(lib.HotelStock(random_element(hotelChains), rand.randint(1, 3)))
        
        #print("at round #" + self.cnt + ", Buy is: " + turn.Buy + ".\n")
        if rand.randint(0, 20) is not 1:
            return turn
        temp_rand = rand.randint(0, 2)
        if self.cnt == 2 or temp_rand == 0:
            turn.Card = SpecialPowers.BUY_5_STOCK
            turn.Buy.append(lib.HotelStock(random_element(hotelChains), 3))
            return turn
        elif temp_rand == 1 or self.cnt == 8:
            turn.Card = SpecialPowers.FREE_3_STOCK
            return turn
        else:
            if (len(me.stock) > 0):
                turn.Card = SpecialPowers.TRADE_2_STOCK
                turn.Trade.append(TradeStock(random_element(me.stock).chain, random_element(hotelChains)))
                return turn

    def QueryMergeStock(self, map, me, hotelChains, players, survivor, defunct):
        myStock = next((stock for stock in me.stock if stock.chain == defunct.name), None)
        return PlayerMerge(myStock.num_shares / 3, myStock.num_shares / 3, (myStock.num_shares + 2) / 3)


class PlayerMerge(object):
    def __init__(self, sell, keep, trade):
        self.Sell = sell
        self.Keep = keep
        self.Trade = trade


class PlayerPlayTile(object):
    def __init__(self, tile, created_hotel, merge_survivor):
        self.Tile = tile
        self.CreatedHotel = created_hotel
        self.MergeSurvivor = merge_survivor


class PlayerTurn(PlayerPlayTile):
    def __init__(self, tile, created_hotel, merge_survivor):
        super(PlayerTurn, self).__init__(tile, created_hotel, merge_survivor)
        self.Card = lib.SpecialPowers.NONE
        self.Buy = []   # hotel stock list
        self.Trade = []    # trade stock list


class TradeStock(object):
    def __init__(self, trade_in, get):
        self.Trade = trade_in
        self.Get = get