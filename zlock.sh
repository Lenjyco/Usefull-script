#! /bin/bash
# Dependencies:
# imagemagick
# i3lock

#IMAGE=$HOME/.i3/vim.png
WHITE=$HOME/.i3/white.png
cp $WHITE /tmp/lock.png
IMAGE=/tmp/lock.png
#curl $(curl -sL https://c.xkcd.com/random/comic/ | grep "https://imgs" | rev | cut -d\  -f1 | rev) > $HOME/.i3/random.png
curl $(curl -sL "http://foodporndaily.com/pictures/$(node -e "var tab = JSON.parse(process.argv[1]);var ran = Math.floor((Math.random() * Object.keys(tab).length) + 1);console.log(tab[ran])" $(curl -sL http://foodporndaily.com/ | grep "var randomSlugs = " | cut -d= -f 2 | sed "s/;//g"))" | grep "\"mainPhoto\"" | cut -d\" -f 4) > $HOME/.i3/random.png

#lock icon
ICON=$HOME/.i3/random.png

#if lock icon
convert $IMAGE $ICON -gravity center -composite -matte $IMAGE

i3lock -i $IMAGE
