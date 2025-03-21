FILE_BASENAME=first-mile-guide-DRAFT

html:
	asciidoctor --trace -o ${FILE_BASENAME}.html index.adoc

pdf:
	asciidoctor -a allow-uri-read --trace -r asciidoctor-pdf --trace -b pdf -o ${FILE_BASENAME}.pdf index.adoc

docx:
	asciidoctor -a allow-uri-read --trace --backend docbook --out-file - index.adoc | pandoc --from docbook --to docx --output ${FILE_BASENAME}.docx

linkcheck:
	find . -name "???.adoc" -exec asciidoc-link-check -p -c ./asciidoc-link-check-config.json {} \;

clean:
	rm -f ${FILE_BASENAME}.{html,pdf,docx}

.PHONY: html pdf docx linkcheck clean
