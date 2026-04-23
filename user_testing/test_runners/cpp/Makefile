CXX = g++
CXXFLAGS = -std=c++17 -O0 -I.
PCH_SRC = helpers.hpp
PCH_OUT = helpers.hpp.gch
OBJ = helpers.o main.o
TARGET = app

all: $(TARGET)

# Link the final binary
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(TARGET)

# Generate the .gch from helpers.hpp
# It automatically includes json.hpp because of the #include inside it
$(PCH_OUT): $(PCH_SRC) json.hpp
  $(CXX) $(CXXFLAGS) -x c++-header -c $(PCH_SRC) -o $(PCH_OUT)

# Compile .cpp files into .o files
# We make them depend on PCH_OUT to ensure the cache is ready first
%.o: %.cpp $(PCH_OUT)
  $(CXX) $(CXXFLAGS) -c $< -o $@
