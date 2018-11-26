tar:
	tar -cvf proj2.tgz Makefile phase1.py phase2.py queryDB.py singleQuery.py report.pdf README.txt

clean:
	rm -f ad.idx da.idx pr.idx te.idx ads.txt pdates.txt  prices.txt readyAds.txt readyPdates.txt readyPrices.txt readyTerms.txt records.xml sortedAds.txt sortedPdates.txt sortedPrices.txt sortedTerms.txt terms.txt
