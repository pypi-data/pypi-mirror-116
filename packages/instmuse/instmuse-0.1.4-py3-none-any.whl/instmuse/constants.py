import numuse.constants
import numuse.musical_system

EQUAL_TEMPERAMENT = musical_system = numuse.musical_system.RBMS_Approximation(
    440, numuse.constants.JUST_INTONATION_RATIOS, 2, 2 ** (1 / 12), 12
)
