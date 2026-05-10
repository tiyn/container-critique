# Container Critique

<!-- ![container-critique-logo](container-critique.png) -->
<img src="container-critique.png" width="300">

Container Critique is a blog based on Pythons Flask framework.
The blog is intended to be used to review and critique movies, books and similar media.

## Features

- [x] User Management
  - [x] Registration
  - [x] Login
  - [x] Logout
  - [x] User profile page

- [x] Blog Functionality
  - [x] Create entries
  - [x] Edit entries
  - [x] Delete entries
  - [x] Standalone article pages
    - [x] Links back to main blog page
  - [x] Infinite-scroll main page
  - [x] Archive page
    - [x] Monthly grouping
    - [x] Links to main blog page
    - [x] Links to standalone articles

- [x] Search
  - [x] Full-text search

- [x] Syndication
  - [x] RSS feed

- [x] User Interface
  - [x] Responsive navigation
    - [x] Header
    - [x] Footer
  - [x] Rich text editor
  - [x] Star ratings
  - [x] Styling for common HTML tags
  - [x] Theme support
    - [x] Dark theme
    - [x] Light theme
  - [x] Logo

- [x] Deployment
  - [x] Basic Python
  - [x] Docker

## To-Dos

- [ ] Quality of Life Improvements
  - [ ] Improved UI for writing entries
  - [ ] Improved UI for editing entries
  - [ ] Improved UI for deleting entries
  - [ ] Improved UI for login flow

## Usage

## Deployment

### uv (Recommended Over PIP)

* install [uv](https://github.com/astral-sh/uv?utm_source=chatgpt.com)
* `git clone https://github.com/tiyn/container-critique`
* `cd container-critique`
* install the dependencies with `uv sync`
* edit the `src/config.py` file according to your needs
* run `uv run python src/app.py`
* blog is available on port 5000

### PIP/Python

* `git clone https://github.com/tiyn/container-critique`
* `cd container-critique/src`
* edit the `config.py` file according to your needs
* install dependencies with `pip install -r requirements.txt`
* run `python app.py`
* blog is available on port 5000

### Docker

Make sure you copy an example `config.py` and edit it before running the container.
The `config.py` can be found in the `src` folder.

#### Volumes

Set the following volumes with the -v tag.

| Volume-Name | Container mount | Description |
| ------------- | ---------------------- | ---------------------------------- |
| `config-file` | `/blog/config.py` | Config file |
| `data` | `/blog/data` | Directory for data |
| `css` | `/blog/static/css` | (optional) Directory for css files |

#### Ports

Set the following ports with the -p tag.

| Container-Port | Recommended outside port | Protocol | Description |
| -------------- | ------------------------ | -------- | ----------- |
| `5000` | `80` | TCP | HTTP port |

#### Example run-command

An example run command is shown in `rebuild.sh`.
