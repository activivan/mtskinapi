# Minetest Skin API
# Created by activivan

from configparser import ConfigParser
from pathlib import Path
import json
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO

# Configuration
configFile = "config.ini"
config = ConfigParser()
config.read(configFile)

game = config["general"].get("game")
mod = config["general"].get("skin_mod")

if game == None or mod == None and game != "mineclone2":
    print("[ERROR] Configuration incomplete! Read configuration.md for more information!")
    exit()

server_port = config["server"].get("server_port", 3008)
server_host = config["server"].get("server_host", "0.0.0.0")
wsgi_server = config["server"].get("wsgi_server", "bjoern")
image_format = config["output"].get("image_format", "PNG")
image_mode = config["output"].get("image_mode", "RGBA")

# Data
thisfile = Path(__file__).resolve()
worldfolder = thisfile.parents[1]
mtfolder = thisfile.parents[3]

defaultplayer = {
    "mineclone2": (mtfolder / "games" / "mineclone2" / "mods" / "PLAYER" / "mcl_player" / "models" / "character.png").resolve(),
    "minetest_game": (mtfolder / "games" / "minetest_game" / "mods" / "player_api" / "models" / "character.png").resolve()
}

locations = {
    "head": {
        "1": (8, 8),
        "2": (16, 16)
    },
    "chest": {
        "1": (20, 20),
        "2": (28, 32)
    },
    "arm": {
        "1": (44, 20),
        "2": (48, 32)
    },
    "leg": {
        "1": (4, 20),
        "2": (8, 32)
    }
}

# Open skin as Pillow image
def openSkin(path):
    img = Image.open(path)

    width = img.size[0]
    height = img.size[1]

    if width != 64 or height != 32:
        print("[ERROR] Incompatible skin Image")

    return img

# Crop skin part out of Pillow image
def cropPart(img, part):
    partImg = img.crop(locations[part]["1"] + locations[part]["2"])

    return partImg

# Create Bust from skin path
def makeBust(input):
    head = cropPart(openSkin(input), "head")
    chest = cropPart(openSkin(input), "chest")
    leftarm = cropPart(openSkin(input), "arm")
    rightarm = leftarm.transpose(method=Image.FLIP_LEFT_RIGHT)

    bust = Image.new(image_mode, (16, 20))

    bust.paste(head, (4, 0, 12, 8))
    bust.paste(chest, (4, 8, 12, 20))
    bust.paste(leftarm, (0, 8, 4, 20))
    bust.paste(rightarm, (12, 8, 16, 20))

    return bust

# Create Body preview from skin path
def makeBody(input):
    bust = makeBust(input)
    leftleg = cropPart(openSkin(input), "leg")
    rightleg = leftleg.transpose(method=Image.FLIP_LEFT_RIGHT)

    body = Image.new(image_mode, (16, 32))

    body.paste(bust, (0, 0, 16, 20))
    body.paste(leftleg, (4, 20, 8, 32))
    body.paste(rightleg, (8, 20, 12, 32))

    return body

# Connect to players.sqlite database
def connectDatabase():
    dbfile = worldfolder / "players.sqlite"

    conn = None

    try:
        conn = sqlite3.connect(dbfile.resolve())
    except Error as e:
        print(e)

    return conn

# Get MineClone 2 skin file path from ID
def getMclSkinPath(id):
    if id == "0":
        return defaultplayer["mineclone2"]
    else:
        skinfile = "mcl_skins_character_" + str(id) + ".png"
        skinpath = mtfolder / "games" / "mineclone2" / "mods" / "PLAYER" / "mcl_skins" / "textures" / skinfile

        return skinpath.resolve()

# Get MineClone 2 skin ID from playername
def getMclSkinId(name):
    conn = connectDatabase()

    sql = "SELECT value FROM player_metadata WHERE player = '" + name + "' and metadata = 'mcl_skins:skin_id'"

    cur = conn.cursor()
    cur.execute(sql)

    skinid = cur.fetchall()

    if len(skinid) == 0:
        return "0"
    else:
        return skinid[0][0]

# Get simple_skins skin filepath from filename
def getSimpleSkinsPath(filename):
    if filename == "0":
        return defaultplayer["minetest_game"]
    else:
        skinfile = filename + ".png"
        skinpath = mtfolder / "mods" / "simple_skins" / "textures" / skinfile

        return skinpath.resolve()

# Get simple_skins skin name from playername
def getSimpleSkinsName(playername):
    conn = connectDatabase()

    sql = "SELECT value FROM player_metadata WHERE player = '" + playername + "' and metadata = 'simple_skins:skin'"

    cur = conn.cursor()
    cur.execute(sql)

    skinname = cur.fetchall()

    if len(skinname) == 0:
        return "0"
    else:
        return skinname[0][0]

# Get skinsdb skin filepath from playername
def getSkinsDbPath(name):
    skinsdbpath = worldfolder / "mod_storage" / "skinsdb"
    skinsdbfile = open(skinsdbpath.resolve(), "r")
    skinsdb = json.loads(skinsdbfile.read())

    if name in skinsdb:
        texturespath = mtfolder / "mods" / "skinsdb" / "textures"
        skinname = skinsdb[name]
        skinfile = skinname + ".png"
        skinpath = texturespath / skinfile

        return skinpath.resolve()
    else:
        return defaultplayer["minetest_game"]

# Send Image Function
def sendImage(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, image_format)
    img_io.seek(0)
    return send_file(img_io, mimetype=Image.MIME[image_format])

# Flask API setup
skinapi = Flask(__name__)

@skinapi.route("/")
def index():
    return render_template("index.html", baseurl=request.base_url)

@skinapi.route("/head/<name>")
def head(name):
    if game == "mineclone2":
        head = cropPart(openSkin(getMclSkinPath(getMclSkinId(name))), "head")
    else:
        if mod == "simple_skins":
            head = cropPart(openSkin(getSimpleSkinsPath(getSimpleSkinsName(name))), "head")
        elif mod == "skinsdb":
            head = cropPart(openSkin(getSkinsDbPath(name)), "head")

    return sendImage(head)

@skinapi.route("/head/<name>/<int:width>")
def head_width(name, width):
    if game == "mineclone2":
        head = cropPart(openSkin(getMclSkinPath(getMclSkinId(name))), "head")
    else:
        if mod == "simple_skins":
            head = cropPart(openSkin(getSimpleSkinsPath(getSimpleSkinsName(name))), "head")
        elif mod == "skinsdb":
            head = cropPart(openSkin(getSkinsDbPath(name)), "head")

    head = head.resize((width, width), Image.NEAREST)
    return sendImage(head)

@skinapi.route("/bust/<name>")
def bust(name):
    if game == "mineclone2":
        bust = makeBust(getMclSkinPath(getMclSkinId(name)))
    else:
        if mod == "simple_skins":
            bust = makeBust(getSimpleSkinsPath(getSimpleSkinsName(name)))
        elif mod == "skinsdb":
            bust = makeBust(getSkinsDbPath(name))

    return sendImage(bust)

@skinapi.route("/bust/<name>/<int:height>")
def bust_height(name, height):
    if game == "mineclone2":
        bust = makeBust(getMclSkinPath(getMclSkinId(name)))
    else:
        if mod == "simple_skins":
            bust = makeBust(getSimpleSkinsPath(getSimpleSkinsName(name)))
        elif mod == "skinsdb":
            bust = makeBust(getSkinsDbPath(name))

    width = height * bust.size[0] / bust.size[1]
    bust = bust.resize((int(width), height), Image.NEAREST)
    return sendImage(bust)

@skinapi.route("/body/<name>")
def body(name):
    if game == "mineclone2":
        body = makeBody(getMclSkinPath(getMclSkinId(name)))
    else:
        if mod == "simple_skins":
            body = makeBody(getSimpleSkinsPath(getSimpleSkinsName(name)))
        elif mod == "skinsdb":
            body = makeBody(getSkinsDbPath(name))

    return sendImage(body)

@skinapi.route("/body/<name>/<int:height>")
def body_height(name, height):
    if game == "mineclone2":
        body = makeBody(getMclSkinPath(getMclSkinId(name)))
    else:
        if mod == "simple_skins":
            body = makeBody(getSimpleSkinsPath(getSimpleSkinsName(name)))
        elif mod == "skinsdb":
            body = makeBody(getSkinsDbPath(name))

    width = height * body.size[0] / body.size[1]
    body = body.resize((int(width), height), Image.NEAREST)
    return sendImage(body)

@skinapi.route("/skin/<name>")
def skin(name):
    if game == "mineclone2":
        skin = Image.open(getMclSkinPath(getMclSkinId(name)))
    else:
        if mod == "simple_skins":
            skin = Image.open(getSimpleSkinsPath(getSimpleSkinsName(name)))
        elif mod == "skinsdb":
            skin = Image.open(getSkinsDbPath(name))

    return sendImage(skin)

# Run Flask API
if __name__ == "__main__":
    if wsgi_server == "bjoern":
        import bjoern
        bjoern.run(skinapi, server_host, int(server_port))
    else:
        skinapi.run()