clean:
	find . -name "*.class" -type f -delete
	find . -name "*.exe" -type f -delete
	find . -name "*.o" -type f -delete
	find . -path "./problems/*/test.json" -type f -delete 