# AMR-TV

## Installation

Clone the repo:

`$ git clone git@github.com:ivansg44/AMR-TV.git amr-tv --recurse-submodules`

Build the docker image:

`$ docker-compose build`

### If there are issues building the image
You may run into issues building the image if you already tried building
adaptagrams locally, or if your adaptagrams submodule is out of date.

Clean things up:

`$ git submodule deinit -f .`

`$ git submodule update --init`

`$ git submodule update`

## Run AMR-TV

### Development

`$ docker-compose --file docker-compose.yaml
--file docker-compose.local.yaml up`

AMR-TV will be available at http://0.0.0.0:8050/.

Changes to Python files will be reflected on container restart.

### Production

`$ docker-compose up`
