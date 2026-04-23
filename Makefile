all:
	@echo "Nothing to build by default. Use 'make clean' to clean."

clean:
	find . \( -name "*.class" -o -name "*.exe" -o -name "*.o" -o -name "*.gch" -o -name "runner.cpp" \) -type f -delete
	find . -path "./problems/*/test.json" -type f -delete