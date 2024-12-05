import unittest

import pytest

#### Test list
# - [.] enregistrer la naissance d'un nouvel elfe
# - [x] calculer à la main l'identifiant d'un premier elfe né en 1984 de sexe Sloubi -> 18400108
# - [x] créer une fonction permettant de calculer le complément d'un elfe
# - [ ] identifier un elfe via son EID
# - [ ] lister tous les elfes par nom et EID
# - [ ] dire si un EID n'est pas valide pour un elfe
# - [ ] dire si un elfe n'existe pas pour un EID valide donné
# - [ ] pouvoir enregistrer l'année de naissance d'un elf
# - [ ] calculer la clé de contrôle d'un elfe à la naissance
# - [ ] introduire un repository


def control_key(eid_prefix: int) -> int:
    return 97 - (eid_prefix % 97)

@pytest.mark.parametrize("eid_prefix, expected_key", [
    (198007, 67),
    (184001, 8),
])
def test_control_key(eid_prefix, expected_key):
    assert control_key(eid_prefix) == expected_key


class ElvesSetInMemory:
    pass


def test_register_when_elf_is_born():
    # GIVEN
    elves_set = ElvesSetInMemory()
    elves_set.elf_register = {}

    # WHEN
    elves_set.elf_register["18400108"] = "Pipon"

    # THEN
    assert elves_set.elf_register["18400108"] == "Pipon"


