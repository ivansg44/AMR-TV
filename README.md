# AMR-TV

## Create a virtual environment

You should use Python 3.9.

I use conda to create my environment:

`$ conda create --yes --name amr-tv python=3.9`

Activate the environment:

`$ conda activate amr-tv`

## Clone the repo

`(amr-tv) $ git clone git@github.com:ivansg44/AMR-TV.git amr-tv --recurse-submodules`

## Install AMR-TV pip requirements

Navigate into the cloned repo (make sure environment is activated!):

`(amr-tv) $ cd amr-tv`

Install pip requirements:

`(amr-tv) $ pip install -r requirements.txt`

## Set up adaptagrams

This library is used for node overlap removal in the zoomed out graph.

### Preamble

Adaptagrams uses autotools for set up. You **may** need to install them. If you
have MacOS and homebrew installed, you can install them as follows:

`(amr-tv) $ brew install libtool autoconf automake`

### Actual setup

Navigate into the following directory from the root of the cloned project:

`(amr-tv) $ cd adaptagrams/cola/`

Run the following script:

`(amr-tv) $ ./autogen.sh`

**You will see some warnings, and one test will likely fail. That is okay.**

Now, run the following command:

`(amr-tv) $ sudo make install`

And then, the following script:

`(amr-tv) $ ./buildPythonSWIG.sh`

Navigate back to the root of the cloned project:

`(amr-tv) $ cd ../..`

## Run AMR-TV

Run as follows:

`(amr-tv) $ python app.py`

AMR-TV will be available at http://127.0.0.1:8050/
