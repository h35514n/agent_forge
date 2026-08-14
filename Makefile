FINAL_MD=report/report.md
FINAL_PDF=report.pdf

.PHONY: report

report:
	pandoc -f markdown -t pdf $(FINAL_MD) -o $(FINAL_PDF)

clean:
	rm -f $(FINAL_PDF)
