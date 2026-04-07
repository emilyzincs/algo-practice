clean:
	find . -name "*.class" -type f -delete
	find . -path "./problems/*/test.json" -type f -delete 