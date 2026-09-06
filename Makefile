# Portfolio — build and serve. Everything runs through uv; nothing is installed
# into your system Python.
UV = uv run --python 3.12 --with 'pelican>=4.9' --with 'markdown>=3.6'

.PHONY: all palettes contrast syndicate html serve publish clean

all: html

palettes:      ## regenerate the six palettes from the table in tools/palettes.py
	@python3 tools/palettes.py

contrast: palettes  ## WCAG audit of every palette; the build fails if one regresses
	@cd tools && python3 contrast.py

syndicate:     ## refresh the three most recent blog posts (cached on failure)
	@python3 tools/syndicate.py

html: palettes contrast syndicate
	@$(UV) pelican content -s pelicanconf.py -o output

serve: html
	@$(UV) pelican --listen --autoreload content -s pelicanconf.py -o output -p 8000

publish: palettes contrast syndicate
	@$(UV) pelican content -s publishconf.py -o output

clean:
	@rm -rf output
