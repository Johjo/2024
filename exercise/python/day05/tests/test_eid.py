import unittest

import pytest
from attr import dataclass


#### Test list
# - [.] enregistrer la naissance d'un nouvel elfe
# - [x] calculer à la main l'identifiant d'un premier elfe né en 1984 de sexe Sloubi -> 18400108
# - [x] créer une fonction permettant de calculer le complément d'un elfe
# - [ ] identifier un elfe via son EID
# - [ ] lister tous les elfes par nom et EID
# - [ ] dire si un EID n'est pas valide pour un elfe
# - [ ] dire si un elfe n'existe pas pour un EID valide donné
# - [ ] pouvoir enregistrer l'année de naissance d'un elf
# - [.] calculer la clé de contrôle d'un elfe à la naissance
# - [x] introduire un repository



def control_key(eid_prefix: int) -> int:
    return 97 - (eid_prefix % 97)

@pytest.mark.parametrize("eid_prefix, expected_key", [
    (198007, 67),
    (184001, 8),
    (185001, 75),
])
def test_control_key(eid_prefix, expected_key):
    assert control_key(eid_prefix) == expected_key


class ElvesSetInMemory:
    def __init__(self) -> None:
        self.elf_register = {}

    def save(self, eid: str, elf_name: str):
        self.elf_register[eid] = elf_name

    def name_by_eid(self, eid: str) -> str:
        return self.elf_register[eid]

@pytest.mark.parametrize("eid_prefix, name, expected_eid", [
    ("184001", "Pipon", "18400108"),
    ("185001", "Pipou", "18500175"),
])
def test_register_when_elf_is_born(eid_prefix: str, name: str, expected_eid, ):
    # GIVEN
    elves_set = ElvesSetInMemory()

    # WHEN

    elves_set.save(expected_eid, name)

    # THEN
    assert elves_set.name_by_eid(expected_eid) == name


