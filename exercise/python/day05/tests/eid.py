from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict


def control_key(eid_prefix: int) -> int:
    return 97 - (eid_prefix % 97)


class Sex(Enum):
    Sloubi = 1
    Gagna = 2
    Catact = 3


@dataclass(frozen=True)
class Elf:
    name: str
    sex: Sex
    year_of_birth: int


class ElvesSetPort(ABC):
    @abstractmethod
    def by_eid(self, eid: str) -> Elf:
        pass

    @abstractmethod
    def all_by_eid(self) -> Dict[str, Elf]:
        pass

    @abstractmethod
    def save(self, eid: str, elf: Elf):
        pass


class ElfQuery:
    def __init__(self, elves_set: ElvesSetPort):
        self.elves_set = elves_set

    def by_id(self, eid: str) -> Elf:
        if control_key(int(eid) // 100) != int(eid) % 100:
            raise EidNotValid
        return self.elves_set.by_eid(eid)

    def all_by_eid(self) -> Dict[str, Elf]:
        return self.elves_set.all_by_eid()


class ElfRegister:
    def __init__(self, elves_set: ElvesSetPort):
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


class ElfDoesNotExist(Exception):
    pass


class EidNotValid(Exception):
    pass
