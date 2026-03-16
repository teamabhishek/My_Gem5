from m5.objects import O3CPU

class Little(O3CPU):
    def __init__(self):
        super().__init__(
            fetchWidth=2,
            decodeWidth=2,
            renameWidth=2,
            issueWidth=2,
            commitWidth=2,
            robEntries=64,
            numPhysIntRegs=80,
            numPhysFloatRegs=80,
        )


class Big(O3CPU):
    def __init__(self):
        super().__init__(
            fetchWidth=8,
            decodeWidth=8,
            renameWidth=8,
            issueWidth=8,
            commitWidth=8,
            robEntries=256,
            numPhysIntRegs=256,
            numPhysFloatRegs=256,
        )