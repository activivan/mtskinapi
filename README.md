# Minetest SkinAPI

Created by activivan



The Minetest SkinAPI allows you to customize your Minetest Web Projects! You can easily get the head, a bust or a body preview of a Minetest skin from just the player name! You can even set the size of the result! It supports the most common skin mods as well as MineClone 2. Using Python Pillow and Flask it's fast and lightweight. Just drop it into your world folder and get started!



## Installation

#### Downloading Minetest SkinAPI

Minetest SkinAPI needs to be put into the world folder of the world it should use the data of. You can use git to clone this repository into your desired world folder. For example:

```shell
cd minetest/worlds/myworld
git clone https://github.com/activivan/mtskinapi.git
```

#### Installing requirements

After downloading Minetest SkinAPI, let's install the required python modules. Navigate into the `mtskinapi` folder you just downloaded into your world folder. Then type into the command prompt:

```shell
pip3 install -r requirements.txt
```

#### Editing Configuration

Minetest SkinAPI can be configured via the `config.ini` file. Some configurations are mandatory to be defined. We will now go through these. All possible configurations can be seen in the `configuration.md` file.

##### `general` Category

To work, Minetest SkinAPI needs to know what game and what skin mod you are using. Currently, two games are being supported:

- `minetest_game`: https://content.minetest.net/packages/Minetest/minetest_game/
- `mineclone2`: https://content.minetest.net/packages/Wuzzy/mineclone2/

You can set the game with:

```ini
game = minetest_game
```

As skin mods for the `minetest_game` are currently supported:

-  TenPlus1's `simple_skins` mod: https://content.minetest.net/packages/TenPlus1/simple_skins/
-  bell07's `skinsdb` mod: https://content.minetest.net/packages/bell07/skinsdb/

You can set the skin mod with:

```ini
skin_mod = simple_skins
```

*Note: If you are using `mineclone2` you do not need to define a skins mod as one is already in the game - if you define a skin mod nevertheless it will just be ignored*



## Running

To run your Minetest SkinAPI installation, we recommend using the bjoern WSGI Server (what to consider to run Minetest SkinAPI on another WSGI Server (e.g. Gunicorn) can be found below). Unfortunately, it only works with Linux systems, but as most of Minetest Servers are running on Linux this should be fine. The following steps are how you would do that on Ubuntu - if you are on another Linux Distribution, the steps may be similar. 

#### Installing bjoern

To install bjoern, you first need to install `libev`:

```shell
sudo apt-get install libev-dev
```

Now install bjoern itself with pip:

```shell
pip3 install bjoern
```

*Note: If you use another Linux Distribution, this might help you: https://github.com/jonashaag/bjoern/wiki/Installation*

#### Installing and using screen

To run Minetest SkinAPI in the background (what you want - otherwise it would block your terminal) it's recommend to use screen. Screen allows you to multiplex your terminal into virtual terminals, so you can run Minetest SkinAPI in a virtual terminal.

To install screen, type this into the command prompt:

```shell
sudo apt-get install screen
```

Now lets create a screen for Minetest SkinAPI. To do that type:

```shel
screen -S mtskinapi
```

You should be automatically attached to this new screen. Now, make sure that you are in the directory of the Minetest SkinAPI and start it by typing:

```shell
python3 app.py
```

You should be done! Your Minetest SkinAPI is running on the IP and Port you set in the configuration. Default is: `0.0.0.0:3008`

#### Helpful commands

- If you want to stop the server, simply do `CTRL+C`

- To start it again, just type `python3 app.py`

- To leave the screen, so you can continue using your normal terminal, press `CTRL+A` and then `D`

- To enter the screen again, type `screen -r mtskinapi` 

  *Note: After you restarted your system, you will have to create a new screen!*

It may be helpful to take a look at the screen documentation: https://www.gnu.org/software/screen/manual/screen.html

#### Using another WSGI Server

To use another WSGI Server like Gunicorn, you will first have to set this in the `config.ini` file, as the default Minetest SkinAPI WSGI Server is bjoern. The entry must be in the `server` category and has the key `wsgi_server`. You can set it to anything but not `bjoern` if you don't want to use bjoern. For example, if you want to use Gunicorn, you can type following to start Minetest SkinAPI (Gunicorn must be installed):

```shell
gunicorn -w 4 -b 0.0.0.0:3008 app:skinapi
```

(WSGI Application (Flask) has the name of `skinapi`)



## API usage

You can see an API documentation on the base url of your running app.

#### Head

You can get the Head of a Player using following API structure:

````
http://127.0.0.1:3008/head/playername
````

You can also simply set the size of the result. Just add the width in pixels:

```
http://example.com:3008/head/playername/width
```

#### Bust

To get a Bust of a Player, use following API structure:

````
http://example.com:3008/bust/playername
````

Busts can also be resized. Add this time the height in pixels:

````
http://example.com:3008/bust/playername/height
````

#### Body

You can also get a full body preview using following API structure:

````
http://example.com:3008/body/playername
````

Here it's also possible to set the size of the result. As with the bust you simply need to add the height in pixels:

````
http://example.com:3008/body/playername/height
````

#### Skin

Using following API structure you can get the full skin of a player:

````
http://example.com:3008/skin/playername
````



## License

Minetest SkinAPI © 2021 by [activivan](https://github.com/activivan) is licensed under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)



#### You are free to

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.

#### Under the following terms

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

- **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

#### Notices

- You do not have to comply with the license for elements of the material  in the public domain or where your use is permitted by an applicable exception or limitation.
- No warranties are given. The license may not give you all of the  permissions necessary for your intended use. For example, other rights  such as publicity, privacy, or moral rights may limit how you use the material.



For more details:

https://creativecommons.org/licenses/by-sa/4.0/