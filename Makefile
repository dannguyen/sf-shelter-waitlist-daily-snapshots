.DEFAULT_GOAL := ALL
.PHONY : clean ALL


ALL: wrangle
	git add --all
	git commit --allow-empty-message
	git push

wrangle: data/wrangled/sf-shelter-waitlist.csv

data/wrangled/sf-shelter-waitlist.csv:
	./scripts/wrangle.py

clean:
	@rm data/wrangled/sf-shelter-waitlist.csv
