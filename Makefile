.DEFAULT_GOAL := ALL
.PHONY : clean ALL

ALL: wrangle wrap
	git add --all
	git commit -m "$$(date)"
	git push

wrap: wrangle
	./scripts/wrap.py

wrangle: data/wrangled/sf-shelter-waitlist.csv

data/wrangled/sf-shelter-waitlist.csv: data/collected
	./scripts/wrangle.py

clean:
	@rm data/wrangled/sf-shelter-waitlist.csv
