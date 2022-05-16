# coding=utf-8
# Copyright 2022 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright 2022 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for smu_sqlite."""

import os
import tempfile

from absl.testing import absltest

from smu import dataset_pb2
from smu import smu_sqlite
from smu.geometry import bond_length_distribution
from smu.parser import smu_utils_lib


class SmuSqliteTest(absltest.TestCase):
  """Tests for smu_sqlite.

  Some notes about the conformer and bond topoology ids used in the tests:
  In the real dataset, bond topologies are a number between 1 and ~900k.
  Conformer ids are a bond topology id * 1000 + id(between 000 and 999). So the
  smallest conformer id we could see is 1000 and the largest is ~900999.
  Therefore, throughout these tests, we use conformer ids in the low thousands
  with small number % 1000. For exemple, create_db uses 2001, 4001, 6001, 8001
  That creates single digit bond topology ids.
  """

  def setUp(self):
    super(SmuSqliteTest, self).setUp()
    self.db_filename = os.path.join(tempfile.mkdtemp(), 'smu_test.sqlite')

  def add_bond_topology_to_conformer(self, conformer, btid, source):
    # We'll use a simple rule for making smiles. The SMILES is just btid
    # number of Cs
    def make_connectivity_matrix(num_c):
      if num_c == 2:
        return '1'
      return '1' + ('0' * (num_c - 2)) + make_connectivity_matrix(num_c - 1)

    if btid == 1:
      bt = smu_utils_lib.create_bond_topology('C', '', '4')
    else:
      bt = smu_utils_lib.create_bond_topology('C' * btid,
                                              make_connectivity_matrix(btid),
                                              '3' + ('2' * (btid - 2)) + '3')
    bt.bond_topology_id = btid
    bt.smiles = 'C' * btid
    bt.source = source
    conformer.bond_topologies.append(bt)

  def make_fake_conformer(self, cid):
    conformer = dataset_pb2.Conformer()
    conformer.conformer_id = cid
    self.add_bond_topology_to_conformer(conformer, cid // 1000,
                                        dataset_pb2.BondTopology.SOURCE_ITC)
    return conformer

  def encode_conformers(self, conformers):
    return [c.SerializeToString() for c in conformers]

  def create_db(self):
    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')
    db.bulk_insert(
        self.encode_conformers([
            self.make_fake_conformer(cid) for cid in range(2001, 10001, 2000)
        ]))
    return db

  def create_db_with_multiple_bond_topology(self):
    # We'll set up 3 CIDS with one or more btids associated with them.
    # cid: 1000 -> btid 1
    # cid: 2000 -> btid 2, 1
    # cid: 3000 -> btid 3, 1, 2
    conf1 = self.make_fake_conformer(1000)
    conf2 = self.make_fake_conformer(2000)
    self.add_bond_topology_to_conformer(conf2, 1,
                                        dataset_pb2.BondTopology.SOURCE_ITC)

    conf3 = self.make_fake_conformer(3000)
    self.add_bond_topology_to_conformer(conf3, 1,
                                        dataset_pb2.BondTopology.SOURCE_ITC)
    self.add_bond_topology_to_conformer(conf3, 2,
                                        dataset_pb2.BondTopology.SOURCE_ITC)

    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')
    db.bulk_insert(self.encode_conformers([conf1, conf2, conf3]))

    return db

  def test_find_bond_topology_id_for_smiles(self):
    db = self.create_db()

    self.assertEqual(db.find_bond_topology_id_for_smiles('CC'), 2)
    with self.assertRaises(KeyError):
      db.find_bond_topology_id_for_smiles('DoesNotExist')

  def test_get_smiles_to_id_dict(self):
    db = self.create_db()

    self.assertEqual(db.get_smiles_id_dict(),
                     {'CC': 2,
                      'CCCC': 4,
                      'CCCCCC': 6,
                      'CCCCCCCC': 8,
                      })

  def test_bulk_insert_smiles(self):
    db = self.create_db()

    with self.assertRaises(KeyError):
      db.find_bond_topology_id_for_smiles('NewSmiles')

    db.bulk_insert_smiles([['FirstSmiles', 111], ['NewSmiles', 222]])
    self.assertEqual(db.find_bond_topology_id_for_smiles('NewSmiles'), 222)

  def test_find_by_conformer_id(self):
    db = self.create_db()

    got = db.find_by_conformer_id(4001)
    self.assertEqual(got.conformer_id, 4001)
    self.assertEqual(got.bond_topologies[0].smiles, 'CCCC')

  def test_key_errors(self):
    db = self.create_db()

    with self.assertRaises(KeyError):
      db.find_by_conformer_id(999)

  def test_write(self):
    create_db = self.create_db()
    del create_db

    db = smu_sqlite.SMUSQLite(self.db_filename, 'w')
    # The create_db makes conformer ids ending in 001. We'll add conformer ids
    # ending in 005 as the extra written ones to make it clear that they are
    # different.
    db.bulk_insert(
        self.encode_conformers([
            self.make_fake_conformer(cid) for cid in range(50005, 60005, 2000)
        ]))
    # Check an id that was already there
    self.assertEqual(db.find_by_conformer_id(4001).conformer_id, 4001)
    # Check an id that we added
    self.assertEqual(db.find_by_conformer_id(52005).conformer_id, 52005)

  def test_read(self):
    create_db = self.create_db()
    del create_db

    db = smu_sqlite.SMUSQLite(self.db_filename, 'r')
    with self.assertRaises(smu_sqlite.ReadOnlyError):
      db.bulk_insert(self.encode_conformers([self.make_fake_conformer(9999)]))

    with self.assertRaises(KeyError):
      db.find_by_conformer_id(9999)

    self.assertEqual(db.find_by_conformer_id(4001).conformer_id, 4001)

  def test_vaccum(self):
    db = self.create_db()
    self.assertEqual(db.find_by_conformer_id(2001).conformer_id,
                     2001)
    db.vacuum()
    self.assertEqual(db.find_by_conformer_id(2001).conformer_id,
                     2001)

  def test_smiles_iteration(self):
    db = self.create_db()

    iter = db.smiles_iter()
    self.assertEqual(('CC', 2), next(iter))
    self.assertEqual(('CCCC', 4), next(iter))
    self.assertEqual(('CCCCCC', 6), next(iter))
    self.assertEqual(('CCCCCCCC', 8), next(iter))
    with self.assertRaises(StopIteration):
      next(iter)

  def test_iteration(self):
    db = self.create_db()

    got_cids = [conformer.conformer_id for conformer in db]
    self.assertCountEqual(got_cids, [2001, 4001, 6001, 8001])

  def test_find_by_bond_topology_id_list(self):
    db = self.create_db_with_multiple_bond_topology()

    # Test the cases with 1, 2, and 3 results
    got_cids = [
        conf.conformer_id for conf in db.find_by_bond_topology_id_list(
          [3], smu_utils_lib.WhichTopologies.all)
    ]
    self.assertCountEqual(got_cids, [3000])

    got_cids = [
        conf.conformer_id for conf in db.find_by_bond_topology_id_list(
          [2], smu_utils_lib.WhichTopologies.all)
    ]
    self.assertCountEqual(got_cids, [2000, 3000])

    got_cids = [
        conf.conformer_id for conf in db.find_by_bond_topology_id_list(
          [1], smu_utils_lib.WhichTopologies.all)
    ]
    self.assertCountEqual(got_cids, [1000, 2000, 3000])

    # and test a non existent id
    self.assertEmpty(list(db.find_by_bond_topology_id_list(
      [999], smu_utils_lib.WhichTopologies.all)))

  def test_find_by_bond_topology_id_list_multi_arg(self):
    db = self.create_db()

    got_cids = [
        conf.conformer_id for conf in db.find_by_bond_topology_id_list(
          [2, 8], smu_utils_lib.WhichTopologies.all)
    ]
    # This is testing that we only get 55000 returned once
    self.assertCountEqual(got_cids, [2001, 8001])

  def test_find_by_bond_topology_id_unique_only(self):
    db = self.create_db()

    conf = self.make_fake_conformer(55000)
    self.add_bond_topology_to_conformer(conf, 55,
                                        dataset_pb2.BondTopology.SOURCE_ITC)
    db.bulk_insert(self.encode_conformers([conf]))

    got_cids = [
        conf.conformer_id for conf in db.find_by_bond_topology_id_list(
          [55], smu_utils_lib.WhichTopologies.all)
    ]
    # This is testing that we only get 55000 returned once
    self.assertCountEqual(got_cids, [55000])

  def test_find_by_bond_topology_id_source_filtering(self):
    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')
    # We'll make 2 conformers
    # 2001 with bt id 10 (ITC, STARTING) and bt id 11 (MLCR)
    # 4001 with bt id 10 (ITC), bt id 11 (ITC, STARTING), bt id 12 (CSD)
    # 6001 with bt id 12 (MLCR)
    conformers = []
    conformers.append(dataset_pb2.Conformer(conformer_id=2001))
    self.add_bond_topology_to_conformer(conformers[-1], 10,
                                        dataset_pb2.BondTopology.SOURCE_STARTING |
                                        dataset_pb2.BondTopology.SOURCE_ITC)
    self.add_bond_topology_to_conformer(conformers[-1], 11,
                                        dataset_pb2.BondTopology.SOURCE_MLCR)
    conformers.append(dataset_pb2.Conformer(conformer_id=4001))
    self.add_bond_topology_to_conformer(conformers[-1], 10,
                                        dataset_pb2.BondTopology.SOURCE_ITC)
    self.add_bond_topology_to_conformer(conformers[-1], 11,
                                        dataset_pb2.BondTopology.SOURCE_STARTING |
                                        dataset_pb2.BondTopology.SOURCE_ITC)
    self.add_bond_topology_to_conformer(conformers[-1], 12,
                                        dataset_pb2.BondTopology.SOURCE_CSD)
    conformers.append(dataset_pb2.Conformer(conformer_id=6001))
    self.add_bond_topology_to_conformer(conformers[-1], 12,
                                        dataset_pb2.BondTopology.SOURCE_MLCR)
    db.bulk_insert(self.encode_conformers(conformers))

    def ids_for(bt_id, which):
      return [c.conformer_id
              for c in db.find_by_bond_topology_id_list([bt_id], which)]

    self.assertEqual(ids_for(10, smu_utils_lib.WhichTopologies.all),
                     [2001, 4001])
    self.assertEqual(ids_for(11, smu_utils_lib.WhichTopologies.all),
                     [2001, 4001])
    self.assertEqual(ids_for(12, smu_utils_lib.WhichTopologies.all),
                     [4001, 6001])

    self.assertEqual(ids_for(10, smu_utils_lib.WhichTopologies.starting),
                     [2001])
    self.assertEqual(ids_for(11, smu_utils_lib.WhichTopologies.mlcr),
                     [2001])
    self.assertEqual(ids_for(12, smu_utils_lib.WhichTopologies.csd),
                     [4001])

    self.assertEmpty(ids_for(12, smu_utils_lib.WhichTopologies.itc))
    self.assertEmpty(ids_for(11, smu_utils_lib.WhichTopologies.csd))



  def test_find_by_smiles_list(self):
    db = self.create_db_with_multiple_bond_topology()

    # Test the cases with 1, 2, and 3 results
    got_cids = [
        conf.conformer_id for conf in db.find_by_smiles_list(
          ['CCC'], smu_utils_lib.WhichTopologies.all)
    ]
    self.assertCountEqual(got_cids, [3000])

    got_cids = [conf.conformer_id for conf in db.find_by_smiles_list(
      ['CC'], smu_utils_lib.WhichTopologies.all)]
    self.assertCountEqual(got_cids, [2000, 3000])

    got_cids = [conf.conformer_id for conf in db.find_by_smiles_list(
      ['C'], smu_utils_lib.WhichTopologies.all)]
    self.assertCountEqual(got_cids, [1000, 2000, 3000])

    # and test a non existent id
    self.assertEmpty(list(db.find_by_smiles_list(
      ['I do not exist'], smu_utils_lib.WhichTopologies.all)))

  def test_find_by_smiles_list_multi_arg(self):
    db = self.create_db()

    got_cids = [
        conf.conformer_id for conf in db.find_by_smiles_list(
          ['CC', 'CCCCCC'], smu_utils_lib.WhichTopologies.all)
    ]
    self.assertCountEqual(got_cids, [2001, 6001])

  def test_repeat_smiles_insert(self):
    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')
    db.bulk_insert(
        self.encode_conformers([
            self.make_fake_conformer(cid) for cid in [2001, 2002, 2003]
        ]))
    got_cids = [
        conformer.conformer_id for conformer in db.find_by_smiles_list(
          ['CC'], smu_utils_lib.WhichTopologies.all)
    ]
    self.assertCountEqual(got_cids, [2001, 2002, 2003])

  def test_find_by_expanded_stoichiometry_list(self):
    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')
    db.bulk_insert(
        self.encode_conformers(
            [self.make_fake_conformer(cid) for cid in [2001, 2002, 4004]]))

    got_cids = [
        conformer.conformer_id
        for conformer in db.find_by_expanded_stoichiometry_list(['(ch2)2(ch3)2'])
    ]
    self.assertCountEqual(got_cids, [4004])

    got_cids = [
        conformer.conformer_id
        for conformer in db.find_by_expanded_stoichiometry_list(['(ch3)2'])
    ]
    self.assertCountEqual(got_cids, [2001, 2002])

    got_cids = [
        conformer.conformer_id
        for conformer in db.find_by_expanded_stoichiometry_list(
            ['(ch2)2(ch3)2', '(ch3)2'])
    ]
    self.assertCountEqual(got_cids, [2001, 2002, 4004])

    self.assertEmpty(list(db.find_by_expanded_stoichiometry_list(['(nh)'])))

  def test_find_by_stoichiometry(self):
    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')
    db.bulk_insert(
        self.encode_conformers(
            [self.make_fake_conformer(cid) for cid in [2001, 2002, 4004]]))

    got_cids = [
        conformer.conformer_id
        for conformer in db.find_by_stoichiometry('c2h6')
    ]
    self.assertCountEqual(got_cids, [2001, 2002])

    got_cids = [
        conformer.conformer_id
        for conformer in db.find_by_stoichiometry('c4h10')
    ]
    self.assertCountEqual(got_cids, [4004])

    self.assertEmpty(list(db.find_by_stoichiometry('c3')))

    with self.assertRaises(smu_utils_lib.StoichiometryError):
      db.find_by_stoichiometry('P3Li')

  def test_find_by_topology(self):
    db = smu_sqlite.SMUSQLite(self.db_filename, 'c')

    # We'll make a pretty fake molecule. N2O2H2 with
    # the O at 0,0
    # the Ns at 1.1,0 and 0,1.1
    # The Hs right night to the Ns
    # We'll given it the ring topology to start and the symetric ring broken
    # topologies should be found.

    conformer = dataset_pb2.Conformer(conformer_id=9999,
                                      fate=dataset_pb2.Conformer.FATE_SUCCESS)
    bt = conformer.bond_topologies.add(smiles='N1NO1', bond_topology_id=100)
    geom = conformer.optimized_geometry.atom_positions

    bt.atoms.append(dataset_pb2.BondTopology.ATOM_O)
    geom.append(dataset_pb2.Geometry.AtomPos(x=0, y=0, z=0))

    bt.atoms.append(dataset_pb2.BondTopology.ATOM_N)
    geom.append(dataset_pb2.Geometry.AtomPos(x=0, y=1.1, z=0))
    bt.bonds.append(dataset_pb2.BondTopology.Bond(
      atom_a=0, atom_b=1, bond_type=dataset_pb2.BondTopology.BOND_SINGLE))
    bt.atoms.append(dataset_pb2.BondTopology.ATOM_N)
    geom.append(dataset_pb2.Geometry.AtomPos(x=1.1, y=0, z=0))
    bt.bonds.append(dataset_pb2.BondTopology.Bond(
      atom_a=0, atom_b=2, bond_type=dataset_pb2.BondTopology.BOND_SINGLE))
    bt.bonds.append(dataset_pb2.BondTopology.Bond(
      atom_a=1, atom_b=2, bond_type=dataset_pb2.BondTopology.BOND_SINGLE))

    bt.atoms.append(dataset_pb2.BondTopology.ATOM_H)
    geom.append(dataset_pb2.Geometry.AtomPos(x=0, y=1.2, z=0))
    bt.bonds.append(dataset_pb2.BondTopology.Bond(
      atom_a=1, atom_b=3, bond_type=dataset_pb2.BondTopology.BOND_SINGLE))
    bt.atoms.append(dataset_pb2.BondTopology.ATOM_H)
    geom.append(dataset_pb2.Geometry.AtomPos(x=1.2, y=0, z=0))
    bt.bonds.append(dataset_pb2.BondTopology.Bond(
      atom_a=2, atom_b=4, bond_type=dataset_pb2.BondTopology.BOND_SINGLE))

    for pos in geom:
      pos.x /= smu_utils_lib.BOHR_TO_ANGSTROMS
      pos.y /= smu_utils_lib.BOHR_TO_ANGSTROMS
      pos.z /= smu_utils_lib.BOHR_TO_ANGSTROMS

    db.bulk_insert([conformer.SerializeToString()])
    db.bulk_insert_smiles([['N1NO1', 100], ['N=[NH+][O-]', 101]])

    bond_lengths = bond_length_distribution.make_fake_empiricals()

    # We'll query by the topology that was in the DB then the one that wasn't
    for query_smiles in ['N1NO1', 'N=[NH+][O-]']:

      got = list(db.find_by_topology(query_smiles,
                                     bond_lengths=bond_lengths))
      self.assertLen(got, 1)
      self.assertCountEqual(
        [100, 101, 101],
        [bt.bond_topology_id for bt in got[0].bond_topologies])

  def test_find_bond_topology_id_by_smarts(self):
    db = self.create_db()

    # 5 carbons in a row will only match the 6 or 8 carbon bond topology
    self.assertEqual(list(db.find_bond_topology_id_by_smarts('CCCCC')),
                     [6, 8])

    with self.assertRaises(ValueError):
      got = list(db.find_bond_topology_id_by_smarts(']Broken)](Smarts'))


if __name__ == '__main__':
  absltest.main()
