from typing import Dict, List

import pytest

from exercise.python.day05.tests.eid import control_key, Sex, Elf, ElvesSetPort, ElfQuery, ElfRegister, ElfDoesNotExist, \
    EidNotValid


#### Test list
# - [x] enregistrer la naissance d'un nouvel elfe
# - [x] calculer à la main l'identifiant d'un premier elfe né en 1984 de sexe Sloubi -> 18400108
# - [x] créer une fonction permettant de calculer le complément d'un elfe
# - [x] identifier un elfe via son EID
# - [x] lister tous les elfes par nom et EID
# - [x] dire si un EID n'est pas valide pour un elfe
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
# - [x] Bug : on ne récupère pas les elfes par leur eid. Il est codé en dur
# - [.] Introduire une notion de Port
# - [ ] Organiser les fichiers


class ElvesSetInMemory(ElvesSetPort):
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

    def all_by_eid(self) -> Dict[str, Elf]:
        return {**self.elf_register}



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
    (Sex.Sloubi, 1984, "Pipon", "18400108"),
    (Sex.Sloubi, 1985, "Pipou", "18500175"),
    (Sex.Gagna, 1986, "Pipette", "28600152"),
    (Sex.Catact, 1987, "Pipelette", "38700129"),
])
def test_register_when_elf_is_born(register_elf: ElfRegister, elves_set : ElvesSetInMemory, sex: Sex, year_of_birth: int, name: str, expected_eid, ):
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



@pytest.mark.parametrize("eid, expected_elf", [
    ("28400214", Elf(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)),
    ("18400108", Elf(name="Pipon", sex=Sex.Sloubi, year_of_birth=1984)),
])
def test_get_elf_by_eid(register_elf: ElfRegister, elves_set : ElvesSetInMemory, elf_query: ElfQuery, eid: str, expected_elf: Elf):
    # GIVEN
    register_elf.execute(name="Pipon", sex=Sex.Sloubi, year_of_birth=1984)
    register_elf.execute(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)

    # WHEN

    # THEN
    assert elf_query.by_id(eid) == expected_elf


def test_tell_when_elf_does_not_exist(elf_query: ElfQuery):
    # WHEN
    with pytest.raises(ElfDoesNotExist):
        elf_query.by_id("28400214")




def test_tell_when_eid_is_not_valid(elf_query: ElfQuery):
    # WHEN
    with pytest.raises(EidNotValid):
        elf_query.by_id("10000000")


def test_get_all_elves_by_eid(register_elf: ElfRegister, elves_set : ElvesSetInMemory, elf_query: ElfQuery):
    # GIVEN
    register_elf.execute(name="Pipon", sex=Sex.Sloubi, year_of_birth=1984)
    register_elf.execute(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)

    # WHEN

    # THEN
    assert elf_query.all_by_eid() == {"18400108": Elf(name="Pipon", sex=Sex.Sloubi, year_of_birth=1984), "28400214": Elf(name="Pipounette", sex=Sex.Gagna, year_of_birth=1984)}