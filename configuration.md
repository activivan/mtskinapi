# Configuration

Minetest SkinAPI can be configured via the `config.ini` file. Possible configurations and categories are:



### `general`

- `game`
  - Insert game of Minetest World
  - No default, mandatory to be defined
  - Compatible games:
    - `minetest_game`: https://content.minetest.net/packages/Minetest/minetest_game/
    - `mineclone2`: https://content.minetest.net/packages/Wuzzy/mineclone2/
  - String
- `skin_mod`
  - Set skin mod for `minetest_game`
  - If using `minetest_game` mandatory to define
  - Compatible skin mods:
    - `simple_skins` by TenPlus1: https://content.minetest.net/packages/TenPlus1/simple_skins/
    - `skinsdb` by bell07: https://content.minetest.net/packages/bell07/skinsdb/
  - String



### `server`

- `wsgi_server`
  - Set WSGI Server
  - Default: `bjoern` 
  - More info in `README.md` "Using another WSGI Server" in "Running"
  - String
- `server_port`
  - Set Port of bjoern WSGI Server
  - Default: `3008`
  - Integer
- `server_host`
  - Set host of bjoern WSGI Server
  - Default: `0.0.0.0`
  - String




### `output`

- `image_format`
  - Set format of output images
  - Default: `PNG`
  - Possible options see Pillow Documentation: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
  - String
- `image_mode`
  - Set mode of output images
  - Default: `RGBA`
  - Possible options see Pillow Documentation: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
  - String