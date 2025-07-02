# AMR-TV

[Introduction slide set](introduction_slide_set.pdf)

## Installation

Clone the repo and submodules:

`$ git clone git@github.com:ivansg44/AMR-TV.git amr-tv --recurse-submodules`

`$ cd amr-tv`

**Linux and macOS users only:** Use the dependency manager
[pixi](https://pixi.sh/latest/installation/) to install AMR-TV:

`$ pixi install`

`$ pixi compile`

AMR-TV will be available at http://0.0.0.0:8050/.

**Windows users:** you can skip to the Docker section.

## Usage

Use the dependency manager [pixi](https://pixi.sh/latest/installation/) to
run AMR-TV after installing:

`$ pixi run app`

## Docker

You can also run the application through [Docker](https://www.docker.com/):

`$ docker-compose build`

`$ docker-compose up`

AMR-TV will be available at http://0.0.0.0:8050/.
