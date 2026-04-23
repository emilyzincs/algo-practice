CXX = g++
CXXFLAGS = -std=c++17 -O0 -I.
PCH_SRC = helpers.hpp
PCH_OUT = helpers.hpp.gch
OBJ = helpers.o runner.o
TARGET = runner.exe

all: $(TARGET)

# Link the final binary
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(TARGET)

# Generate the .gch from helpers.hpp
$(PCH_OUT): $(PCH_SRC) json.hpp
	$(CXX) $(CXXFLAGS) -x c++-header -c $(PCH_SRC) -o $(PCH_OUT)

# Compile .cpp files into .o files
%.o: %.cpp $(PCH_OUT)
	$(CXX) $(CXXFLAGS) -c $< -o $@