from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
from pathlib import Path
import m5.debug
from gem5.simulate.exit_event import ExitEvent
import argparse
from m5.objects import RedirectPath
from m5.core import setInterpDir

parser = argparse.ArgumentParser()

parser.add_argument("--workload-type",
        help="if the workload is compiled as static or dynamic binary",
        type=str,
        required=True,
        choices=["static","dynamic"])

args = parser.parse_args()

if args.workload_type == "static":
    binary = Path("annotate-static")
else:
    binary = Path("annotate-dynamic")


cache = PrivateL1CacheHierarchy(
    l1d_size="64kB",
    l1i_size="64kB"
)

memory = SingleChannelDDR4_2400("1GB")

processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.ARM,
    num_cores=1
)

board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache
)

if (args.workload_type =="dynamic"):
    print("Time to redirect the library path")
    setInterpDir("/usr/aarch64-linux-gnu/")

    board.redirect_paths = [
        RedirectPath(
            app_path="/lib",
            host_paths=["/usr/aarch64-linux-gnu/lib"]
        )
    ]

board.set_se_binary_workload(
    binary=BinaryResource(local_path=binary.as_posix())
)

# define a workbegin handler
def workbegin_handler():
    print("Workbegin handler")
    m5.debug.flags["ExecAll"].enable()
    yield False

# define a workend handler
def workend_handler():
    print("Workend handler")
    print(simulator.get_last_exit_event_cause())
    m5.debug.flags["ExecAll"].disable()
    yield False

simulator = Simulator(
    board= board,
    on_exit_event= {
        ExitEvent.WORKBEGIN: workbegin_handler(),
        ExitEvent.WORKEND: workend_handler()
    })

simulator.run()

print("Simulation finished")