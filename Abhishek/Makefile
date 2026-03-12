# Path to gem5 directory
GEM5_PATH = /home/abhishek-pathak/Documents/Research/Practical/gem5

# Target ISA
ISA = arm64

# Cross compiler
GXX = aarch64-linux-gnu-g++

# Default target
all: static dynamic

# Static binary
static:
	$(GXX) -o annotate-static annotate.cpp -static \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-lm5

# Dynamic binary
dynamic:
	$(GXX) -o annotate-dynamic annotate.cpp \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-lm5

# Clean binaries
clean:
	rm -f annotate-static annotate-dynamic