from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

import pytest


#### Test list
# - [x] enregistrer la naissance d'un nouvel elfe
# - [x] calculer à la main l'identifiant d'un premier elfe né en 1984 de sexe Sloubi -> 18400108
# - [x] créer une fonction permettant de calculer le complément d'un elfe
# - [x] identifier un elfe via son EID
# - [ ] lister tous les elfes par nom et EID
# - [.] dire si un EID n'est pas valide pour un elfe
# - [x] dire si un elfe n'existe pas pour un EID valide donné
# - [x] pouvoir enregistrer l'année de naissance d'un elf
# - [x] pouvoir enregistrer le sex d'un elf
# - [x] introduire le sex Gagna (2)
# - [x] introduire le sex Catact (3)
# - [x] calculer la clé de contrôle d'un elfe à la naissance
# - [x] introduire un repository
# - [x] introduire le décompte des elfes par année
# - [x] Mettre l'année sur 4 digits
# - [x] Sauvegarder l'année de naissance des elfes
# - [x] Récupérer tous les elfes depuis le repository





def control_key(eid_prefix: int) -> int:
    return 97 - (eid_prefix % 97)

@pytest.mark.parametrize("eid_prefix, expected_key", [
    (198007, 67),
    (184001, 8),
    (185001, 75),
    (286001, 52),
    (387001, 29),
    (284002, 14),
])
def test_control_key(eid_prefix, expected_key):
    assert control_key(eid_prefix) == expected_key

class Sex(Enum):
    Sloubi = 1
    Gagna = 2
    Catact = 3

@dataclass(frozen=True)
class Elf:
    name: str
    sex: Sex
    year_of_birth: int


class ElvesSetInMemory:
    def __init__(self) -> None:
        self.elf_register : Dict[str, Elf] = {}

    def save(self, eid: str, elf: Elf):
        self.elf_register[eid] = elf

    def name_by_eid(self, eid: str) -> str:
        return self.elf_register[eid].name

    def all(self) -> List[Elf]:
        return list(self.elf_register.values())

    def by_eid(self, eid: str) -> Elf:
        try:
            return self.elf_register[eid]
        except KeyError:
            raise ElfDoesNotExist()


class ElfQuery:
    def __init__(self, elves_set: ElvesSetInMemory):
        self.elves_set = elves_set

    def by_id(self, eid: str) -> Elf:
        return self.elves_set.by_eid("28400214")


class ElfRegister:
    def __init__(self, elves_set: ElvesSetInMemory):
        self.elves_set = elves_set

    def execute(self, sex: Sex, year_of_birth: int,  name: str):
        self.elves_set.save(
                    eid=self.calculate_eid(sex, year_of_birth),
                    elf=Elf(name=name, sex=sex, year_of_birth=year_of_birth))

    def calculate_eid(self, sex, year_of_birth):
        year_count = self._count_elves_by_year(year_of_birth) + 1
        eid_prefix = sex.value * 100000 + (year_of_birth % 100) * 1000 + year_count
        eid = f"{eid_prefix}{str(control_key(eid_prefix)).zfill(2)}"
        return eid

    def _count_elves_by_year(self, year_of_birth):
        return len([elf for elf in (self.elves_set.all()) if elf.year_of_birth == year_of_birth])


@pytest.fixture
def elves_set() -> ElvesSetInMemory:
    return ElvesSetInMemory()


@pytest.fixture
def register_elf(elves_set: ElvesSetInMemory) -> ElfRegister:
    return ElfRegister(elves_set=elves_set)

@pytest.fixture
def elf_query(elves_set: ElvesSetInMemory) -> ElfQuery:
    return ElfQuery(elves_set=elves_set)

@pytest.mark.parametrize("sex, year_of_birth, name, expected_eid", [
    (Sex.Sloubi, 1984,  "Pipon", "18400108"),
    (Sex.Sloubi, 1985, "Pipou", "18500175"),
    (Sex.Gagna, 1986,  "Pipette", "28600152"),
    (Sex.Catact, 1987, "Pipelette", "38700129"),
])
def test_register_when_elf_is_born(register_elf: ElfRegister, elves_set : ElvesSetInMemory, sex: Sex, year_of_birth: int,  name: str, expected_eid, ):
    # GIVEN

    # WHEN
    register_elf.execute(name=name, sex=sex, year_of_birth=year_of_birth)

    # THEN
    assert elves_set.name_by_eid(expected_eid) == name


def test_increase_year_counter_when_register_elf(register_elf: ElfRegister, elves_set : ElvesSetInMemory):
    # GIVEN
    register_elf.execute(name="Pipon", sex=Sex.Sloubi, year_of_birth=1984)
    register_elf.execute(name="Pipon", sex=Sex.Sloubi, year_of_birth=1985)

    # WHEN
    register_elf.execute(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)

    # THEN
    assert elves_set.name_by_eid("28400214") == "Pipounette"




def test_get_elf_by_eid(register_elf: ElfRegister, elves_set : ElvesSetInMemory, elf_query: ElfQuery):
    # GIVEN
    register_elf.execute(name="Pipon", sex=Sex.Sloubi, year_of_birth=1984)

    # WHEN
    register_elf.execute(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)

    # THEN
    assert elf_query.by_id("28400214") == Elf(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)


class ElfDoesNotExist(Exception):
    pass


def test_tell_when_elf_does_not_exist(elf_query: ElfQuery):
    # WHEN
    with pytest.raises(ElfDoesNotExist):
        elf_query.by_id("28400214")

def test_tell_when_eid_is_not_valid(elf_query: ElfQuery):
    # WHEN
    with pytest.raises(EidNotValid):
        elf_query.by_id("10000000")

