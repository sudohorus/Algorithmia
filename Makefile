#compiler
CXX = g++

#compiler flags
CXXFLAGS = -Wall -std=c++11

#target executable
TARGET = algorithmia

#source files
SRC = src/main.cpp

#output directory
BUILD_DIR = build

#default target
all: $(BUILD_DIR)/$(TARGET)

#build target
$(BUILD_DIR)/$(TARGET): $(SRC)
	@mkdir -p $(BUILD_DIR)  #create build directory if it doesn't exist
	$(CXX) $(CXXFLAGS) -o $(BUILD_DIR)/$(TARGET) $(SRC)

#clean up build files
clean:
	rm -rf $(BUILD_DIR)
