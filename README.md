# AMR-TV

This is a work-in-progress for CPSC 547.

## Installation

`$ docker-compose build --force-rm`

`$ docker-compose run django python manage.py makemigrations`

`$ docker-compose run django python manage.py migrate`

`$ docker-compose up`

## Acknowledgements

Dockerized Django + Postgres setup inspired by [Cookiecutter Django][1]

[1]: https://github.com/pydanny/cookiecutter-django

## License

[MIT][2]

[2]: LICENSE.md
