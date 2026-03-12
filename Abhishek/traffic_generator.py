from gem5.components.boards.test_board import TestBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.simulate.simulator import Simulator


# Cache hierarchy
cache = PrivateL1SharedL2CacheHierarchy(
    l1d_size="32kB",
    l1d_assoc=8,
    l1i_size="32kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
)

# Memory
memory = SingleChannelDDR3_1600(size="2GB")

# Traffic generator
generator = LinearGenerator(
    num_cores=1,
    rate="1GB/s",
    max_addr=2**20,
)

# Board
board = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache,
)

# Simulator
simulator = Simulator(board=board)

print("Starting simulation!")

simulator.run()

print("Simulation finished!")