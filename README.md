# AMR-TV

## Installation

Clone the repo and submodules:

`$ git clone git@github.com:ivansg44/AMR-TV.git amr-tv --recurse-submodules`

`$ cd amr-tv`

### Linux and macOs users

Use the dependency manager [pixi](https://pixi.sh/latest/installation/) to
install and compile AMR-TV:

`$ pixi install --locked`

`$ pixi run compile`

Now you can run AMR-TV with:

`$ pixi run start`

AMR-TV will be available at http://0.0.0.0:8050/.

### Windows users

You can run the application through [Docker](https://www.docker.com/):

`$ docker-compose build`

`$ docker-compose up`

AMR-TV will be available at http://0.0.0.0:8050/.

#### If there are issues building the image:

You may run into issues building the image if you tried compiling locally
earlier.

Clean things up:

`$ git submodule deinit -f .`

`$ git submodule update --init`

And try again.
