import time
import json

from .utils import get_pokemon_rarity, get_pokemon_name
from pogom.utils import get_args
from datetime import datetime
from commands import getstatusoutput

legend = ["snorlax", "lapras", "kangaskhan", "ditto", "articuno", "zapdos", "moltres", "mewtwo", "mew"]
rare = ["abra", "geodude", "ekans", "growlithe", "machop", "porygon", "diglett", "mankey", "hitmonchan", "kadabra", "hitmonlee", "pikachu", "rhyhorn", "graveler", "arbok", "cubone", "exeggcute", "chansey", "koffing", "grimer", "arcanine", "dratini", "tangela", "machoke", "farfetch", "mr_mime", "omanyte", "bulbasaur", "dugtrio", "primeape", "charmander", "squirtle", "rhydon", "kabuto", "snorlax", "onix", "pinsir", "kabutops", "aerodactyl", "alakazam", "ivysaur", "raichu", "machamp", "gengar", "exeggutor", "marowak", "lickitung", "gyarados", "wartortle", "victreebel", "golem", "muk", "weezing", "kangaskhan", "lapras", "charmeleon", "charizard", "magmar", "ditto", "omastar", "dragonair", "dragonite", "venusaur", "blastoise", "articuno", "zapdos", "moltres", "mewtwo", "mew"]
common = ["rattata", "meowth", "magnemite", "voltorb", "gastly", "caterpie", "weedle", "nidoran_male", "nidoran_female", "vulpix", "zubat", "drowzee", "ponyta", "pidgey", "raticate", "eevee", "paras", "oddish", "jigglypuff", "persian", "bellsprout", "venonat", "poliwag", "magneton", "staryu", "kakuna", "electrode", "krabby", "magikarp", "slowpoke", "metapod", "goldeen", "spearow", "psyduck", "sandshrew", "jynx", "haunter", "pidgeotto", "electabuzz", "doduo", "tentacool", "golbat", "shellder", "ninetales", "horsea", "rapidash", "fearow", "nidorina", "parasect", "starmie", "wigglytuff", "hypno", "seaking", "nidorino", "flareon", "gloom", "jolteon", "golduck", "dodrio", "kingler", "butterfree", "clefairy", "poliwhirl", "tentacruel", "beedrill", "seel", "cloyster", "seadra", "sandslash", "scyther", "nidoqueen", "venomoth", "weepinbell", "dewgong", "pidgeot", "nidoking", "vaporeon", "vileplume", "poliwrath", "slowbro", "clefable", "tauros"]

args = get_args()

def utc2local (utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
    return utc + offset

def printPokemon(id, lat, lng, itime):
    if args.display_in_console:
        pokemon_name = get_pokemon_name(id).lower()
        pokemon_rarity = get_pokemon_rarity(id).lower()
        pokemon_id = str(id)
        if pokemon_name not in common:
            timeLeft = itime - datetime.utcnow()
            print("======================================\n Name: %s\n Rarity: %s\n Coord: (%f,%f)\n ID: %s \n Remaining Time: %s\n======================================" % (
                pokemon_name.encode('utf-8'), pokemon_rarity.encode('utf-8'), lat, lng, pokemon_id, str(timeLeft)))

        notifySlack(pokemon_name, lat, lng, itime)


def notifySlack(pokemon_name, lat, lng, itime):
    if pokemon_name in rare:
        channel = '#rare'
    elif pokemon_name in legend:
        channel = '#legend'
    else:
        return

    disappear_time = utc2local(itime).strftime('%Y-%m-%d %H:%M:%S')
    path = "http://maps.google.com/?q=" + str(lat) + "," + str(lng)
    text = "<" + path + "|" + pokemon_name + "> disappears @ " + disappear_time
    payload = json.dumps({
      'channel': channel,
      'username': 'poke-notifier',
      'text': text,
      'icon_emoji': ':ghost:'
    })
    url = "https://hooks.slack.com/services/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"
    cmd = "curl -s -X POST --data-urlencode 'payload=" + payload + "' " + url + " > /dev/null"
    try:
        getstatusoutput(cmd)
    except Exception, e:
        log(e)
