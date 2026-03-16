#Implement a processor with a single out of order core

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from m5.objects import ArmO3CPU
from m5.objects import TournamentBP
class MyOutOfOrderCore(BaseCPUCore):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        super().__init__(ArmO3CPU(), ISA.ARM)
        self.core.fetchWidth = width
        self.core.decodeWidth = width
        self.core.renameWidth = width
        self.core.issueWidth = width
        self.core.wbWidth = width
        self.core.commitWidth = width

        self.core.numROBEntries = rob_size
        self.core.numPhysIntRegs = num_int_regs
        self.core.numPhysFloatRegs = num_fp_regs

        self.core.branchPred = TournamentBP()

        self.core.LQEntries = 128
        self.core.SQEntries = 128


class MyOutOfOrderProcessor(BaseCPUProcessor):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        cores = [MyOutOfOrderCore(width, rob_size, num_int_regs, num_fp_regs)]

        #In case we need two cores
        #cores = [MyOutOfOrderCore(width, rob_size, num_int_regs, num_fp_regs),
        #       MyOutOfOrderCore(width, rob_size, num_int_regs, num_fp_regs)]
        super().__init__(cores)

my_ooo_processor = MyOutOfOrderProcessor(
    width=8, rob_size=192, num_int_regs=256, num_fp_regs=256
)

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)

memory = SingleChannelDDR4_2400(size='2GB')

board = SimpleBoard(
    clk_freq="3GHz",
    processor=my_ooo_processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_workload(obtain_resource("arm-gapbs-bfs-run"))

simulator = Simulator(board=board)
simulator.run()