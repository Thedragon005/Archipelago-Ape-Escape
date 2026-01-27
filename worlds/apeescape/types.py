from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ApeEscapeShuffleData:
    er_pairings: Dict[str, str]