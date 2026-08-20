HUGO ?= hugo
PORT ?= 1314
NAME ?= my-new-post

.PHONY: all build serve draft clean new

all: build

build:
	$(HUGO) --gc --minify

serve:
	$(HUGO) server --bind 127.0.0.1 -p $(PORT)

draft:
	$(HUGO) server --bind 127.0.0.1 -p $(PORT) --buildDrafts

clean:
	rm -rf public resources .hugo_build.lock

new:
	$(HUGO) new posts/$(NAME).md
