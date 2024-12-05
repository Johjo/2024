import unittest

import pytest

#### Test list
# - [.] enregistrer la naissance d'un nouvel elfe
# - [.] calculer à la main l'identifiant d'un premier elfe né en 1984 de sexe Sloubi
# - [.] créer une fonction permettant de calculer le complément d'un elfe
# - [ ] identifier un elfe via son EID
# - [ ] lister tous les elfes par nom et EID
# - [ ] dire si un EID n'est pas valide pour un elfe
# - [ ] dire si un elfe n'existe pas pour un EID valide donné



def test_control_key():
    assert control_key(198007) == 67

