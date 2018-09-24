#!/bin/bash
{
  set -e

  # Grab current directory name
  DIR="$( pwd )"

  # delete old gsecrets bin if exists
  rm -f /usr/local/bin/gsecrets
  ln -s "$DIR/cli.sh" /usr/local/bin/gsecrets

  # test the CLI
  gsecrets --help
}