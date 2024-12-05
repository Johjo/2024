from enum import Enum
from typing import Dict

import pytest


#### Test list
# - [.] enregistrer la naissance d'un nouvel elfe
# - [x] calculer à la main l'identifiant d'un premier elfe né en 1984 de sexe Sloubi -> 18400108
# - [x] créer une fonction permettant de calculer le complément d'un elfe
# - [ ] identifier un elfe via son EID
# - [ ] lister tous les elfes par nom et EID
# - [ ] dire si un EID n'est pas valide pour un elfe
# - [ ] dire si un elfe n'existe pas pour un EID valide donné
# - [x] pouvoir enregistrer l'année de naissance d'un elf
# - [x] pouvoir enregistrer le sex d'un elf
# - [x] introduire le sex Gagna (2)
# - [x] introduire le sex Catact (3)
# - [x] calculer la clé de contrôle d'un elfe à la naissance
# - [x] introduire un repository




def control_key(eid_prefix: int) -> int:
    return 97 - (eid_prefix % 97)

@pytest.mark.parametrize("eid_prefix, expected_key", [
    (198007, 67),
    (184001, 8),
    (185001, 75),
    (286001, 52),
    (387001, 29),
])
def test_control_key(eid_prefix, expected_key):
    assert control_key(eid_prefix) == expected_key


class ElvesSetInMemory:
    def __init__(self) -> None:
        self.elf_register : Dict[str, str] = {}

    def save(self, eid: str, elf_name: str):
        self.elf_register[eid] = elf_name

    def name_by_eid(self, eid: str) -> str:
        return self.elf_register[eid]

class Sex(Enum):
    Sloubi = 1
    Gagna = 2
    Catact = 3


class ElfRegister:
    def __init__(self, elves_set: ElvesSetInMemory):
        self.elves_set = elves_set
    def execute(self, sex: Sex, year_of_birth: int,  name: str):
        eid_prefix = sex.value * 100000 + year_of_birth * 1000 + 1
        eid = f"{eid_prefix}{str(control_key(eid_prefix)).zfill(2)}"
        self.elves_set.save(eid, name)


@pytest.mark.parametrize("sex, year_of_birth, name, expected_eid", [
    (Sex.Sloubi, 84,  "Pipon", "18400108"),
    (Sex.Sloubi, 85, "Pipou", "18500175"),
    (Sex.Gagna, 86,  "Pipette", "28600152"),
    (Sex.Catact, 87, "Pipelette", "38700129"),
])
def test_register_when_elf_is_born(sex: Sex, year_of_birth: int,  name: str, expected_eid, ):
    # GIVEN
    elves_set = ElvesSetInMemory()
    register_elf = ElfRegister(elves_set=elves_set)

    # WHEN
    register_elf.execute()

    # THEN
    assert elves_set.name_by_eid(expected_eid) == name


