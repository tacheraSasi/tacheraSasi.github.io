HUGO ?= hugo
PORT ?= 1314
NAME ?= my-new-post

# Match CI (.github/workflows/hugo.yaml): the theme's npm deps (postcss-cli,
# autoprefixer) must be on PATH for Hugo's postCSS resource step.
export PATH := $(CURDIR)/themes/hugo-texify3/node_modules/.bin:$(PATH)

.PHONY: all build serve draft setup clean new

setup:
	./setup.sh

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
