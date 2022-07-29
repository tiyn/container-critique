# Container Critique

This is a blog based on Pythons Flask framework.
The blog is intended to be used to review and critique things.

## Features/To-Dos

- [ ] Plain text support for blog entries
  - [ ] HTML files (.html)
  - [ ] Markdown Files (.md)
- [ ] Infinite-scroll blog page
- [ ] Archive page
  - [ ] Months as headings
  - [ ] Links to scrolling blog page
  - [ ] Links to standalone article
- [ ] Standalone article page
  - [ ] Links to scrolling blog page
- [ ] RSS feed
- [ ] Navigation
  - [ ] Header
  - [ ] Footer
- [ ] Switchable CSS
  - [ ] CSS dark-theme
  - [ ] CSS light-theme
- [ ] Config file
- [ ] Docker installation
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

| Volume-Name   | Container mount             | Description                                                  |
| ------------- | --------------------------- | ------------------------------------------------------------ |
| `config-file` | `/blog/src/config.py`       | Config file                                                  |
| `entries`     | `/blog/src/templates/entry` | Directory for blog entries                                   |
| `css`         | `/blog/src/static/css`      | (optional) Directory for css files                           |
| `html`        | `/blog/src/templates`       | (optional) Directory for templates (entry-volume not needed) |

#### Ports

Set the following ports with the -p tag.

| Container-Port | Recommended outside port | Protocol | Description |
| -------------- | ------------------------ | -------- | ----------- |
| `5000`         | `80`                     | TCP      | HTTP port   |

#### Example run-command

An example run command is shown in `rebuild.sh`.
