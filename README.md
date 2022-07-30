# Container Critique

This is a blog based on Pythons Flask framework.
The blog is intended to be used to review and critique things.

## Features/To-Dos


- [x] Accounts
  - [x] Login
  - [x] Logout
  - [x] Register
- [ ] Review blog entries
  - [x] Writing entries
  - [ ] Editing entries
  - [ ] Deleting entries
- [x] Infinite-scroll blog page
- [x] Archive page
  - [x] Months as headings
  - [x] Links to scrolling blog page
  - [x] Links to standalone article
- [x] Standalone article page
  - [x] Links to scrolling blog page
- [x] RSS feed
- [ ] Eye candy
  - [ ] Star rating
  - [ ] Rich text editor
- [x] Navigation
  - [x] Header
  - [x] Footer
- [x] Switchable CSS
  - [x] CSS dark-theme
  - [x] CSS light-theme
- [x] Docker installation
- [ ] Logo

## Usage

## Deployment

### PIP/Python

- `git clone https://github.com/tiyn/container-critique`
- `cd container-critique/src`
- edit the `config.py` file according to your needs
- `pip3install -r requirements.txt` - install depenencies
- run `python app.py`
- blog is available on port 5000

### Docker

Make sure you copy an example `config.py` and edit it before running the container.
The `config.py` can be found in the `src` folder.

#### Volumes

Set the following volumes with the -v tag.

| Volume-Name   | Container mount        | Description                        |
| ------------- | ---------------------- | ---------------------------------- |
| `config-file` | `/blog/config.py`  | Config file                        |
| `data`        | `/blog/data`       | Directory for data                 |
| `css`         | `/blog/static/css` | (optional) Directory for css files |

#### Ports

Set the following ports with the -p tag.

| Container-Port | Recommended outside port | Protocol | Description |
| -------------- | ------------------------ | -------- | ----------- |
| `5000`         | `80`                     | TCP      | HTTP port   |

#### Example run-command

An example run command is shown in `rebuild.sh`.
