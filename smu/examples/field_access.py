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
"""Basic access to different kinds of fields."""

from smu import smu_sqlite

db = smu_sqlite.SMUSQLite('20220621_standard.sqlite')

#-----------------------------------------------------------------------------
# This is an arbitrary choice of the molecule to use.
#-----------------------------------------------------------------------------
molecule = db.find_by_molecule_id(57001)

print('We will examine molecule with id', molecule.molecule_id)

print('The computed properties are generally in the .properties field')

print()
print('Scalar values are access by name (note the .value suffix),',
      'like this single point energy: ',
      molecule.properties.single_point_energy_atomic_b5.value)

print()
print('Fields with repeated values',
      'like harmonic_intensities and excitation_energies_cc2)',
      'use an index with [] on the repeated values')

print('The 0th and 6th harmonic_intensities:',
      molecule.properties.harmonic_intensities.value[0],
      molecule.properties.harmonic_intensities.value[6])

print('Or you can iterate over all of them')
for value in molecule.properties.excitation_energies_cc2.value:
  print('Excitation energy:', value)

print('Or just ask how many excitation_energies_cc2 there are:',
      len(molecule.properties.excitation_energies_cc2.value))

print()
print(
    'Some fields like dipole_moment_pbe0_aug_pc_1 have explicit x,y,z components'
)

print(molecule.properties.dipole_moment_pbe0_aug_pc_1.x,
      molecule.properties.dipole_moment_pbe0_aug_pc_1.y,
      molecule.properties.dipole_moment_pbe0_aug_pc_1.z)

print()
print('Some fields are higher order tensors, with similar named components')

print('polarizability is a rank 2 tensor')
print(molecule.properties.dipole_dipole_polarizability_pbe0_aug_pc_1.xx,
      molecule.properties.dipole_dipole_polarizability_pbe0_aug_pc_1.yy,
      molecule.properties.dipole_dipole_polarizability_pbe0_aug_pc_1.zz,
      molecule.properties.dipole_dipole_polarizability_pbe0_aug_pc_1.xy,
      molecule.properties.dipole_dipole_polarizability_pbe0_aug_pc_1.xz,
      molecule.properties.dipole_dipole_polarizability_pbe0_aug_pc_1.yz)

print('octopole moment is a rank 3 tensor')
print(molecule.properties.octopole_moment_pbe0_aug_pc_1.xxx,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.yyy,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.zzz,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.xxy,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.xxz,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.xyy,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.yyz,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.xzz,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.yzz,
      molecule.properties.octopole_moment_pbe0_aug_pc_1.xyz)

print()
print('A couple of important fields are not inside "properties"')

geometry = molecule.optimized_geometry
print('For example, the optimized geometry has an energy of',
      geometry.energy.value,
      'and positions for',
      len(geometry.atom_positions),
      'atoms and the first atom x-coordinate is',
      geometry.atom_positions[0].x)

print()
print('In addition to looking at dataset.proto for field documentation,',
      'you can just print a given molecule to see what fields are available')

print(molecule)
