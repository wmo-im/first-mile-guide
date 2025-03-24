# WMO First Mile Data Collection Guide

## Overview

This directory manages the WMO First Mile Data Collection Guide documentation.

### Dependencies

Documentation is managed with [Asciidoctor](https://asciidoctor.org).

Link checking is managed with [asciidoc-link-check](https://www.npmjs.com/package/asciidoc-link-check).

PDF generation is managed with [asciidoctor-pdf](https://www.npmjs.com/package/asciidoctor-pdf).

```bash
apt-get install pandoc
npm install asciidoctor asciidoctor-pdf asciidoc-link-check
```

### Building the document

```bash
# create HTML (single page)
asciidoctor --trace -o first-mile-guide.html index.adoc
# create PDF
asciidoctor --trace -r asciidoctor-pdf --trace -b pdf -o first-mile-guide.pdf index.adoc
# create Word document
asciidoctor --trace --backend docbook --out-file - index.adoc | pandoc --from docbook --to docx --output first-mile-guide.docx
```

# check links
```bash
find . -name "???.adoc" -exec asciidoc-link-check -p -c asciidoc-link-check-config.json {} \;
```

**Note**: `Makefile` provides shortcuts to these commands if you are able to run `make`.
