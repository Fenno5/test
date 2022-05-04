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

# Lint as: python3
"""Writes Small Molecule Universe (SMU) files in custom Uni Basel format.

Used to write SMU entries from a protocol buffer to a SMU .dat file in Basel
format.
"""

import re

from smu import dataset_pb2
from smu.parser import smu_parser_lib
from smu.parser import smu_utils_lib


class DatFormatMismatchError(Exception):
  pass


class RegeneratedLinesError(DatFormatMismatchError):

  def __init__(self, missing_lines, excess_lines):
    super().__init__()
    self.missing_lines = missing_lines
    self.excess_lines = excess_lines

  def __str__(self):
    return 'missing_lines:\n{}\nexcess_lines:\n{}\n'.format(
        '\n'.join(self.missing_lines), '\n'.join(self.excess_lines))


class LineOrderError(DatFormatMismatchError):

  def __init__(self, index, original_line, regenerated_line):
    super().__init__()
    self.index = index
    self.original_line = original_line
    self.regenerated_line = regenerated_line

  def __str__(self):
    return 'At {}, original:\n{}\ngenerated:\n{}\n'.format(
        self.index, self.original_line, self.regenerated_line)


# So this is pretty exciting. Fortran uses NaN and Infinity instead of nan
# and inf in its output, so if we want to match, we have to use those. This
# is very hacky solution to that because it relies on after the fact string
# replacements but it was easier to get the spacing right this way.
# We'll only use this in places where we know one of these could show up
class _FortranFloat(float):

  def __format__(self, format_spec):
    return (super(_FortranFloat, self).__format__(format_spec)  # pytype: disable=attribute-error
            .replace('nan', 'NaN').replace('     -inf', '-Infinity').replace(
                '     inf', 'Infinity'))


class SmuWriter:
  """A class to gather a SMU protocol buffer into a Basel-formatted string."""

  def __init__(self, annotate):
    """Initializes SMU7Writer.

    Args:
      annotate: bool, whether to provide annotations of the source proto fields
    """
    self.annotate = annotate

  def _conformer_index_string(self, conformer):
    if conformer.original_conformer_index == -1:
      return '*****'
    else:
      return str(conformer.original_conformer_index).rjust(5)

  def get_stage1_header(self, conformer):
    """Returns formatted header (separator and first line).

    This is for the stage1 format, which just contains the results of geometry
    optimization

    Args:
      conformer: dataset_pb2.Conformer.

    Returns:
      A multiline string representation of the header.
    """
    num_atoms = len(conformer.bond_topologies[0].atoms)
    result = smu_parser_lib.SEPARATOR_LINE + '\n'
    if self.annotate:
      result += ('# From original_conformer_index, topology, bond_topology_id, '
                 'error_{nstat1, nstatc, nstatt, frequences} conformer_id\n')
    errors = conformer.properties.errors
    result += '{:5s}{:5d}{:5d}{:5d}{:5d}{:5d}     {:s}\n'.format(
        self._conformer_index_string(conformer), errors.error_nstat1,
        errors.error_nstatc, errors.error_nstatt, errors.error_frequencies,
        num_atoms, smu_utils_lib.get_original_label(conformer))
    return result

  def get_stage2_header(self, conformer):
    """Returns formatted header (separator and first line).

    This is for the stage2 format which is at the end of the pipeline.

    Args:
      conformer: dataset_pb2.Conformer.

    Returns:
      A multiline string representation of the header.
    """
    num_atoms = len(conformer.bond_topologies[0].atoms)
    result = smu_parser_lib.SEPARATOR_LINE + '\n'
    if self.annotate:
      result += ('# From original_conformer_index, topology, '
                 'bond_topology_id, conformer_id\n')
    result += '{:s}{:5d}     {:s}\n'.format(
      self._conformer_index_string(conformer), num_atoms,
      smu_utils_lib.get_original_label(conformer))
    return result

  def get_database(self, conformer):
    """Returns the line indicating which database this conformer goes to.

    Args:
      conformer: A Conformer protocol buffer message.

    Returns:
      String
    """
    if conformer.which_database == dataset_pb2.STANDARD:
      return 'Database   standard\n'
    elif (conformer.which_database == dataset_pb2.COMPLETE or
          conformer.which_database == dataset_pb2.UNSPECIFIED):
      return 'Database   complete\n'
    raise ValueError('Bad which_database: {}'.format(conformer.which_database))

  def get_error_codes(self, properties):
    """Returns a section of error/warning codes (as defined by Uni Basel).

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation
    """
    result = ''
    if self.annotate:
      result += '# From errors\n'

    result += 'Status     {:4d}\n'.format(properties.errors.status)
    result += 'Warn_T1    {:4d}{:4d}\n'.format(properties.errors.warn_t1,
                                               properties.errors.warn_t1_excess)
    result += 'Warn_BSE   {:4d}{:4d}\n'.format(
        properties.errors.warn_bse_b5_b6, properties.errors.warn_bse_cccsd_b5)
    result += 'Warn_EXC   {:4d}{:4d}{:4d}\n'.format(
        properties.errors.warn_exc_lowest_excitation,
        properties.errors.warn_exc_smallest_oscillator,
        properties.errors.warn_exc_largest_oscillator)
    result += 'Warn_VIB   {:4d}{:4d}\n'.format(
        properties.errors.warn_vib_linearity,
        properties.errors.warn_vib_imaginary)
    result += 'Warn_NEG   {:4d}\n'.format(properties.errors.warn_num_neg)

    return result

  def get_adjacency_code_and_hydrogens(self, topology):
    """Returns adjacency code and number of hydrogens bonded to heavy atoms.

    Args:
      topology: A BondTopology protocol buffer message.

    Returns:
      A multiline string representation of adjacency code and hydrogen numbers.
    """
    adjacency_matrix = smu_utils_lib.compute_adjacency_matrix(topology)
    side_length = len(adjacency_matrix)
    result = ''
    if self.annotate:
      result += '# From topology\n'
    result += '     '
    for i in range(0, side_length):
      for j in range(i + 1, side_length):
        result += str(adjacency_matrix[i][j])
    result += '\n     '
    num_bonded_hydrogens = smu_utils_lib.compute_bonded_hydrogens(
        topology, adjacency_matrix)
    return result + ''.join(str(item) for item in num_bonded_hydrogens) + '\n'

  def get_ids(self, conformer, stage):
    """Returns lines with identifiers.

    This include the smiles string, the file, and the ID line.
    We meed to know the stage because the SMU1 special cases are handled
    differently in the two stages.

    Args:
      conformer: dataset_pb2.Conformer
      stage: 'stage1' or 'stage2'

    Returns:
      A multiline string representation of id lines.
    """
    result = ''
    if self.annotate:
      result += '# From smiles\n'
    result += conformer.bond_topologies[0].smiles + '\n'
    if self.annotate:
      result += '# From topology\n'
    result += smu_utils_lib.get_composition(conformer.bond_topologies[0]) + '\n'
    if self.annotate:
      result += '# From bond_topology_id, conformer_id\n'
    bond_topology_id = conformer.bond_topologies[-1].bond_topology_id
    # Special case SMU1. Fun.
    if smu_utils_lib.special_case_dat_id_from_bt_id(bond_topology_id):
      if stage == 'stage1':
        bond_topology_id = 0
      elif stage == 'stage2':
        bond_topology_id = smu_utils_lib.special_case_dat_id_from_bt_id(
            bond_topology_id)
      else:
        raise ValueError(f'Unknown stage {stage}')
    result += 'ID{:8d}{:8d}\n'.format(bond_topology_id,
                                      conformer.conformer_id % 1000)
    return result

  def get_system(self, properties):
    """Returns information about cluster on which computations were performed.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation.
    """
    result = ''
    if self.annotate:
      result += '# From compute_cluster_info\n'
    result += properties.compute_cluster_info
    return result

  def get_stage1_timings(self, properties):
    """Returns recorded timings for different computation steps.

    This is for the stage1 format, which just contains the results of geometry
    optimization

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of timings for different computations.
    """
    result = 'TIMINGS'

    def get_stat(s):
      for statistic in properties.calculation_statistics:
        if statistic.computing_location == s:
          return statistic.timings

    result += '{:>6s}{:>6s}'.format(get_stat('Geo'), get_stat('Force'))
    result += '    -1' * 8
    result += '\n'
    return result

  def get_stage2_timings(self, properties):
    """Returns recorded timings for different computation steps.

    This is for the stage2 format which is at the end of the pipeline.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of timings for different computations.
    """
    labels = '       '
    values = 'TIMINGS'
    for statistic in properties.calculation_statistics:
      labels += statistic.computing_location.rjust(6)
      values += statistic.timings.rjust(6)
    labels = labels.replace('Force', ' Force').replace(' CC', 'CC').replace(
        'Polar', '  Polar').replace('  IP', 'IP')
    result = ''
    if self.annotate:
      result += '# From calculation_statistics\n'
    result += labels
    result += '\n'
    result += values
    result += '\n'
    return result

  def get_bonds(self, topology, properties):
    """Returns a bond section with atom pairs and bond types.

    Args:
      topology: A BondTopology protocol buffer message.
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of bond atom pairs and bond types.
    """
    if properties.errors.status >= 4:
      return ''
    adjacency_matrix = smu_utils_lib.compute_adjacency_matrix(topology)
    bonds = []
    for bond in topology.bonds:
      # Bond type is a six-digit integer ABCDEF, where A and B are the atomic
      # numbers of the two atoms forming the bond, C is the bond order, D and E
      # are the free valencies on the two atoms, and F encodes the charge.
      atom_types = [topology.atoms[bond.atom_a], topology.atoms[bond.atom_b]]
      bond_type = '%d%d' % (
          smu_utils_lib.ATOM_TYPE_TO_ATOMIC_NUMBER[atom_types[0]],
          smu_utils_lib.ATOM_TYPE_TO_ATOMIC_NUMBER[atom_types[1]])
      # Hydrogen atoms are not in the adjacency matrix.
      bond_order = 1 if '1' in bond_type else adjacency_matrix[bond.atom_a][
          bond.atom_b]
      charge = 0
      for i in range(2):
        if atom_types[i] == dataset_pb2.BondTopology.ATOM_NPOS:
          charge += 1
        elif atom_types[i] == dataset_pb2.BondTopology.ATOM_ONEG:
          charge -= 1
      # A total charge of -1 is encoded by integer value 3.
      if charge == -1:
        charge = 3
      free_valencies = (smu_utils_lib.ATOM_TYPE_TO_MAX_BONDS[atom_types[0]] -
                        bond_order,
                        smu_utils_lib.ATOM_TYPE_TO_MAX_BONDS[atom_types[1]] -
                        bond_order)
      # TODO(kohlhoff): Bonds between nitrogen atoms have their free valencies
      # stored in descending order. Identify the root cause.
      if bond_type == '77' and free_valencies[1] > free_valencies[0]:
        free_valencies = (free_valencies[1], free_valencies[0])
      bond_type += '%d%d%d%d' % (bond_order, free_valencies[0],
                                 free_valencies[1], charge)
      bonds.append('BOND%s%s     TYPE%s\n' %
                   (str(bond.atom_a + 1).rjust(5),
                    str(bond.atom_b + 1).rjust(5), bond_type.rjust(8)))
    result = ''
    if self.annotate:
      result += '# From bond_topology\n'
    result += ''.join(bonds)
    return result

  _DEPRECATED_ENERGY_FIELDS = [
    [
      'E_ini/G_norm', 'initial_geometry_energy_deprecated',
      'initial_geometry_gradient_norm_deprecated'
    ],
    [
      'E_opt/G_norm',
      'optimized_geometry_energy_deprecated',
      'optimized_geometry_gradient_norm_deprecated'
    ]]

  def get_gradient_norms(self, conformer, spacer):
    """Returns initial and optimized geometry energies and gradient norms.

    Args:
      conformer: dataset_pb2.Conformer
      spacer: spacer after label (differs between stage1 and stage2)

    Returns:
      A multiline string representation of geometry energies and gradient norms.
    """
    result = ''
    if conformer.optimized_geometry.HasField('energy'):
      for label, geometry in [('E_ini/G_norm', conformer.initial_geometries[0]),
                              ('E_opt/G_norm', conformer.optimized_geometry)]:
        if self.annotate:
          result += '# From energy, gnorm\n'
        result += '{}{}{:11.6f}{:12.6f}\n'.format(
          label, spacer,
          geometry.energy.value,
          geometry.gnorm.value)
    elif conformer.properties.HasField('optimized_geometry_energy_deprecated'):
      for label, field_energy, field_norm in self._DEPRECATED_ENERGY_FIELDS:
        if self.annotate:
          result += '# From %s, %s\n' % (field_energy, field_norm)
        result += '{}{}{:11.6f}{:12.6f}\n'.format(
            label, spacer,
            getattr(conformer.properties, field_energy).value,
            getattr(conformer.properties, field_norm).value)
    else:
      raise ValueError('All conformers should have energies')
    return result

  def get_coordinates(self, topology, conformer):
    """Returns a section with a molecule's initial and optimized geometries.

    Args:
      topology: A BondTopology protocol buffer message.
      conformer: A Conformer protocol buffer message.

    Returns:
      A multiline string representation of geometries in Cartesian coordinates.
    """
    coordinates = ''
    if (conformer.initial_geometries and
        conformer.initial_geometries[0].atom_positions):
      if self.annotate:
        coordinates += '# From initial_geometry.atom_positions\n'
      for i, atom in enumerate(topology.atoms):
        positions = conformer.initial_geometries[0].atom_positions[i]

        coordinates += 'Initial Coords%s%s%s%s\n' % (
            str(smu_utils_lib.ATOM_TYPE_TO_ATOMIC_NUMBER[atom]).rjust(8),
            '{:f}'.format(positions.x).rjust(12), '{:f}'.format(
                positions.y).rjust(12), '{:f}'.format(positions.z).rjust(12))
    if (conformer.HasField('optimized_geometry') and
        conformer.optimized_geometry.atom_positions):
      if self.annotate:
        coordinates += '# From optimized_geometry.atom_positions\n'
      for i, atom in enumerate(topology.atoms):
        positions = conformer.optimized_geometry.atom_positions[i]
        coordinates += 'Optimized Coords%s%s%s%s\n' % (
            str(smu_utils_lib.ATOM_TYPE_TO_ATOMIC_NUMBER[atom]).rjust(6),
            '{:f}'.format(positions.x).rjust(12), '{:f}'.format(
                positions.y).rjust(12), '{:f}'.format(positions.z).rjust(12))
    return coordinates

  def get_rotational_constants(self, conformer):
    """Returns rotational constants vector (MHz).

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      A string representation of the rotational constants vector.
    """
    if conformer.optimized_geometry.HasField('rotcon'):
      annotate = '# From optimized_geometry.rotcon\n'
      vals = conformer.optimized_geometry.rotcon.value
      pass
    elif conformer.properties.HasField('rotational_constants_deprecated'):
      annotate = '# From rotational_constants_deprecated\n'
      constants = conformer.properties.rotational_constants_deprecated
      vals = (constants.x, constants.y, constants.z)
    else:
      return ''
    result = ''
    if self.annotate:
      result += '# From rotational_constants_deprecated\n'
    result += (
        'Rotational constants (MHz)  {:-20.3f}{:-20.3f}{:-20.3f}\n'.format(
          vals[0], vals[1], vals[2]))
    return result

  def get_symmetry_used(self, properties):
    """Returns whether symmetry was used in the computations.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A string defining whether symmetry was used.
    """
    if not properties.HasField('symmetry_used_in_calculation'):
      return ''
    result = ''
    if self.annotate:
      result += '# From symmetry_used_in_calculation\n'
    symmetry_used = properties.symmetry_used_in_calculation
    result += 'Symmetry used in calculation   ' + ('yes\n' if symmetry_used else
                                                   ' no\n')
    return result

  def get_frequencies_and_intensities(self, properties, header):
    """Returns harmonic frequencies and intensities.

    Args:
      properties: A Properties protocol buffer message.
      header: bool, whether to print a header line

    Returns:
      A multiline string representation of harmonic frequencies and intensities.
    """
    if len(properties.harmonic_frequencies.value) == 0:  # pylint: disable=g-explicit-length-test
      return ''
    result = ''
    if header:
      result += 'Frequencies and intensities\n'
    if self.annotate:
      result += '# From harmonic_frequencies, '
      result += 'magnitude/harmonic intensity/normal mode order\n'
    frequencies = properties.harmonic_frequencies.value
    for i in range(0, len(frequencies), 10):
      result += ''.join(
          '{:7.1f}'.format(value).rjust(7) for value in frequencies[i:i + 10])
      result += '\n'
    if self.annotate:
      result += '# From harmonic_intensities\n'
    intensities = properties.harmonic_intensities.value
    for i in range(0, len(intensities), 10):
      result += ''.join(
          '{:7.1f}'.format(value).rjust(7) for value in intensities[i:i + 10])
      result += '\n'
    return result

  def get_gaussian_sanity_check(self, properties):
    """Returns gaussian sanity check section.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation
    """
    if not properties.HasField('gaussian_sanity_check'):
      return ''

    output_lines = ['Gaussian sanity check for FREQ/ELSTAT calculation\n']
    for prefix, fields in smu_parser_lib.GAUSSIAN_SANITY_CHECK_LINES:
      if self.annotate:
        output_lines.append('# From ' + ','.join(fields) + '\n')
      if len(fields) == 1:
        output_lines.append('{:30s}{:14.6f}\n'.format(
            prefix, getattr(properties.gaussian_sanity_check, fields[0])))
      elif len(fields) == 2:
        output_lines.append('{:30s}{:14.6f}{:14.6f}\n'.format(
            prefix, getattr(properties.gaussian_sanity_check, fields[0]),
            getattr(properties.gaussian_sanity_check, fields[1])))
      else:
        raise ValueError('Bad fields {fields} in _GAUSSIAN_SANITY_CHECK_LINES')

    return ''.join(output_lines)

  def get_normal_modes(self, properties):
    """Returns a repeated section containing a number of normal modes.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of the normal modes.
    """
    if len(properties.normal_modes) == 0:  # pylint: disable=g-explicit-length-test
      return ''
    result = 'Normal modes\n'
    if self.annotate:
      result += '# From normal_modes\n'
    for i, normal_modes in enumerate(properties.normal_modes):
      result += 'Mode%s\n' % str(i + 1).rjust(4)
      displacements = []
      for displacement in normal_modes.displacements:
        displacements += [displacement.x, displacement.y, displacement.z]
      for j in range(0, len(displacements), 10):
        result += ''.join('{:8.4f}'.format(value).rjust(8)
                          for value in displacements[j:j + 10])
        result += '\n'
    return result

  def get_properties(self, conformer):
    """Returns a variety of properties, in particular single point energies.

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      A multiline string representation of the labeled properties.
    """
    properties = conformer.properties
    float_line = '{:21s}{:-12.6f}\n'.format
    int_line = '{:21s}{:-5d}\n'.format
    result = ''
    for label, field in smu_parser_lib.PROPERTIES_LABEL_FIELDS.items():
      if label in ['NIMAG', 'NUM_OPT']:
        if not properties.HasField(field):
          continue
        if self.annotate:
          result += '# From %s\n' % field
        result += int_line(label, getattr(properties, field))

      elif label == 'NUCREP':
        value = None
        if conformer.optimized_geometry.HasField('enuc'):
          if self.annotate:
            result += '# From optimized_geometry.enuc\n'
          value = conformer.optimized_geometry.enuc.value
        elif properties.HasField('nuclear_repulsion_energy_deprecated'):
          if self.annotate:
            result += '# From nuclear_repulsion_energy_deprecated\n'
          value = properties.nuclear_repulsion_energy_deprecated.value
        if value is None:
          continue
        result += float_line(label, _FortranFloat(value))

      elif label == 'ZPE_unscaled':
        # This is just a special case because the number of significant digts is
        # different.
        if not properties.HasField(field):
          continue
        if self.annotate:
          result += '# From zpe_unscaled\n'
        result += 'ZPE_unscaled {:-16.2f}\n'.format(
            properties.zpe_unscaled.value)

      else:
        if not properties.HasField(field):
          continue
        if self.annotate:
          result += '# From %s\n' % field
        result += float_line(label,
                             _FortranFloat(getattr(properties, field).value))

    return result

  _T1_DIAGNOSTICS_FIELDS = [
      'diagnostics_t1_ccsd_2sp', 'diagnostics_t1_ccsd_2sd',
      'diagnostics_t1_ccsd_3psd'
  ]

  def get_diagnostics(self, properties):
    """Returns D1 diagnostics.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A string representation of the D1 and T1 diagnostics.
    """
    result = ''

    if properties.HasField('diagnostics_d1_ccsd_2sp'):
      if self.annotate:
        result += '# From diagnostics_d1_ccsd_2sp\n'
      result += ('D1DIAG    D1(CCSD/2sp) {:10.6f}\n'.format(
          properties.diagnostics_d1_ccsd_2sp.value))

    if properties.HasField(self._T1_DIAGNOSTICS_FIELDS[0]):
      if self.annotate:
        result += '# From %s\n' % ', '.join(self._T1_DIAGNOSTICS_FIELDS)
      result += (
          'T1DIAG    T1(CCSD/2sp) %s  T1(CCSD/2sd) %s  T1(CCSD/3Psd)%s\n' %
          tuple('{:.6f}'.format(getattr(properties, field).value).rjust(10)
                for field in self._T1_DIAGNOSTICS_FIELDS))

    return result

  def get_atomic_block(self, properties):
    """Returns block of ATOMIC2 properties.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A string representation of the ATOMIC2 related properties.
    """
    result = ''
    for label, (field,
                field_type) in smu_parser_lib.ATOMIC_LABEL_FIELDS.items():
      if not properties.HasField(field):
        continue
      if field_type == smu_parser_lib.Atomic2FieldTypes.STRING:
        if self.annotate:
          result += '# From %s\n' % field
        result += '{:20s}{:s}\n'.format(label, getattr(properties, field).value)
      elif field_type == smu_parser_lib.Atomic2FieldTypes.SCALAR:
        if self.annotate:
          result += '# From %s\n' % field
        # Different significant digits for some fields. Fun.
        if '_ENE_' in label:
          result += '{:16s}{:-17.6f}\n'.format(
              label, _FortranFloat(getattr(properties, field).value))
        else:
          result += '{:16s}{:-15.4f}\n'.format(
              label, _FortranFloat(getattr(properties, field).value))
      elif field_type == smu_parser_lib.Atomic2FieldTypes.TRIPLE:
        if self.annotate:
          result += '# From %s{,_um,_um_ci}\n' % field
        result += '{:17s}{:-12.2f}{:-12.2f}{:-12.2f}\n'.format(
            label, _FortranFloat(getattr(properties, field).value),
            _FortranFloat(getattr(properties, field + '_um').value),
            _FortranFloat(getattr(properties, field + '_um_ci').value))
      else:
        raise ValueError(
            'Atomic block unknown field types {}'.format(field_type))

    return result

  _HOMO_LUMO_LABEL_FIELDS = [
      ['PBE0/6-311Gd', 'pbe0_6_311gd'],
      ['PBE0/aug-pc-1', 'pbe0_aug_pc_1'],
      ['HF/6-31Gd', 'hf_6_31gd'],
      ['B3LYP/6-31++Gdp', 'b3lyp_6_31ppgdp'],
      ['B3LYP/aug-pcS-1', 'b3lyp_aug_pcs_1'],
      ['PBE0/6-31++Gdp', 'pbe0_6_31ppgdp'],
      ['PBE0/aug-pcS-1', 'pbe0_aug_pcs_1'],
      ['HF/TZVP', 'hf_tzvp'],
      ['HF/3', 'hf_3'],
      ['HF/4', 'hf_4'],
      ['HF/CVTZ', 'hf_cvtz'],
  ]

  def get_homo_lumo(self, properties):
    """Returns HOMO and LUMO values (at different levels of theory).

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of the HOMO/LUMO.
    """
    result = ''
    for label, field_stem in self._HOMO_LUMO_LABEL_FIELDS:
      homo_field = 'homo_' + field_stem
      lumo_field = 'lumo_' + field_stem
      if (not properties.HasField(homo_field) or
          not properties.HasField(lumo_field)):
        continue
      if self.annotate:
        result += '# From %s, %s\n' % (homo_field, lumo_field)
      result += 'HOMO/LUMO  %s%s%s\n' % (label.ljust(15), '{:.5f}'.format(
          getattr(properties, homo_field).value).rjust(11), '{:.5f}'.format(
              getattr(properties, lumo_field).value).rjust(11))

    return result

  def get_excitation_energies_and_oscillations(self, properties):
    """Returns excitation energies and length rep. osc.

    strengths at CC2/TZVP.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of the energies and oscillations.
    """
    if not properties.HasField('excitation_energies_cc2'):
      return ''
    result = smu_parser_lib.EXCITATION_HEADER + '\n'
    if self.annotate:
      result += ('# From excitation_energies_cc2, '
                 'excitation_oscillator_strengths_cc2\n')
    if len(properties.excitation_energies_cc2.value) != len(
        properties.excitation_oscillator_strengths_cc2.value):
      raise ValueError(
          'Unequal lengths for excitation energies (%d) and oscillations (%d)' %
          (len(properties.excitation_energies_cc2.value),
           len(properties.excitation_oscillator_strengths_cc2.value)))
    for i, (energy, oscillator_strength) in enumerate(
        zip(properties.excitation_energies_cc2.value,
            properties.excitation_oscillator_strengths_cc2.value)):
      result += '%s%s%s\n' % (str(i + 1).rjust(5),
                              '{:.5f}'.format(energy).rjust(18),
                              '{:.5f}'.format(oscillator_strength).rjust(16))
    return result

  def get_nmr_isotropic_shieldings(self, topology, properties):
    """Returns NMR isotropic shieldings (ppm) for different levels of theory.

    Args:
      topology: A BondTopology protocol buffer message.
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of the NMR isotropic shieldings.
    """
    result = ''
    for label, field in (
        smu_parser_lib.NMR_ISOTROPIC_SHIELDINGS_LABEL_FIELDS.items()):
      if not properties.HasField(field):
        continue
      if self.annotate:
        result += '# From %s\n' % field
      result += 'NMR isotropic shieldings (ppm): %s\n' % label
      for i, atom in enumerate(topology.atoms):
        result += '%s%s%s   +/-%s\n' % (
            str(i + 1).rjust(5),
            str(smu_utils_lib.ATOM_TYPE_TO_ATOMIC_NUMBER[atom]).rjust(5),
            '{:12.4f}'.format(getattr(properties, field).values[i]),
            '{:10.4f}'.format(getattr(properties, field).precision[i]))

    return result

  def get_partial_charges(self, topology, properties):
    """Returns formatted partial charges for different levels of theory.

    Args:
      topology: A BondTopology protocol buffer message.
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of the partial charges.
    """
    result = ''
    for label, field in smu_parser_lib.PARTIAL_CHARGES_LABEL_FIELDS.items():
      if not properties.HasField(field):
        continue
      result += 'Partial charges (e): %s\n' % label
      if self.annotate:
        result += '# From %s\n' % field
      for i, atom in enumerate(topology.atoms):
        result += '%s%s%s   +/-%s\n' % (
            str(i + 1).rjust(5),
            str(smu_utils_lib.ATOM_TYPE_TO_ATOMIC_NUMBER[atom]).rjust(5),
            '{:12.4f}'.format(getattr(properties, field).values[i]),
            '{:10.4f}'.format(getattr(properties, field).precision[i]))

    return result

  def format_for_tensors(self, label, val):
    return '   %s%s\n' % (label, '{:.5f}'.format(val).rjust(14))

  def get_rank2(self, prop):
    """Returns the output for a Rank2MolecularProperty.

    Args:
      prop: Rank2MolecularProperty

    Returns:
      string
    """
    out = ''
    if prop.matrix_values_deprecated:
      for label, val in zip(smu_parser_lib.RANK2_ENCODING_ORDER,
                            prop.matrix_values_deprecated):
        out += self.format_for_tensors(' ' + label, val)
    else:
      for label in smu_parser_lib.RANK2_ENCODING_ORDER:
        out += self.format_for_tensors(' ' + label, getattr(prop, label))
    return out

  def get_rank3(self, prop):
    """Returns the output for a Rank3MolecularProperty.

    Args:
      prop: Rank3MolecularProperty

    Returns:
      string
    """
    out = ''
    if prop.tensor_values_deprecated:
      for label, val in zip(smu_parser_lib.RANK3_ENCODING_ORDER,
                            prop.tensor_values_deprecated):
        out += self.format_for_tensors(label, val)
    else:
      for label in smu_parser_lib.RANK3_ENCODING_ORDER:
        out += self.format_for_tensors(label, getattr(prop, label))
    return out

  def get_polarizability(self, properties):
    """Returns dipole-dipole polarizability.

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of dipole-dipole polarizability.
    """
    if not properties.HasField('dipole_dipole_polarizability_pbe0_aug_pc_1'):
      return ''
    result = 'Polarizability (au):    PBE0/aug-pc-1\n'
    if self.annotate:
      result += '# From dipole_dipole_polarizability_pbe0_aug_pc_1\n'
    result += self.get_rank2(
      properties.dipole_dipole_polarizability_pbe0_aug_pc_1)
    return result

  def get_multipole_moments(self, properties):
    """Returns formatted Di-, Quadru-, and Octopole moments in (au).

    Args:
      properties: A Properties protocol buffer message.

    Returns:
      A multiline string representation of the multipole moments.
    """

    result = ''

    if properties.HasField('dipole_moment_pbe0_aug_pc_1'):
      result += 'Dipole moment (au):     PBE0/aug-pc-1\n'
      if self.annotate:
        result += '# From dipole_moment_pbe0_aug_pc_1\n'
      result += self.format_for_tensors('  x',
                                        properties.dipole_moment_pbe0_aug_pc_1.x)
      result += self.format_for_tensors('  y',
                                        properties.dipole_moment_pbe0_aug_pc_1.y)
      result += self.format_for_tensors('  z',
                                        properties.dipole_moment_pbe0_aug_pc_1.z)

    if properties.HasField('quadrupole_moment_pbe0_aug_pc_1'):
      result += 'Quadrupole moment (au): PBE0/aug-pc-1\n'
      if self.annotate:
        result += '# From quadrupole_moment_pbe0_aug_pc_1\n'
      result += self.get_rank2(properties.quadrupole_moment_pbe0_aug_pc_1)

    if properties.HasField('octopole_moment_pbe0_aug_pc_1'):
      result += 'Octopole moment (au):   PBE0/aug-pc-1\n'
      if self.annotate:
        result += '# From octopole_moment_pbe0_aug_pc_1\n'
      result += self.get_rank3(properties.octopole_moment_pbe0_aug_pc_1)

    if properties.HasField('dipole_moment_hf_6_31gd'):
      result += 'Dipole moment (au):     HF/6-31Gd\n'
      if self.annotate:
        result += '# From dipole_moment_hf\n'
      result += self.format_for_tensors('  x',
                                        properties.dipole_moment_hf_6_31gd.x)
      result += self.format_for_tensors('  y',
                                        properties.dipole_moment_hf_6_31gd.y)
      result += self.format_for_tensors('  z',
                                        properties.dipole_moment_hf_6_31gd.z)

    if properties.HasField('quadrupole_moment_hf_6_31gd'):
      result += 'Quadrupole moment (au): HF/6-31Gd\n'
      if self.annotate:
        result += '# From quadrupole_moment_hf_6_31gd\n'
      result += self.get_rank2(properties.quadrupole_moment_hf_6_31gd)

    if properties.HasField('octopole_moment_hf_6_31gd'):
      result += 'Octopole moment (au):   HF/6-31Gd\n'
      if self.annotate:
        result += '# From octopole_moment_hf_6_31gd\n'
      result += self.get_rank3(properties.octopole_moment_hf_6_31gd)

    return result

  def process_stage1_proto(self, conformer):
    """Return the contents of conformer as a string in SMU7 stage1 file format.

    This is for the stage1 format, which just contains the results of geometry
    optimization

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      A string representation of the protocol buffer in Uni Basel's file format.
    """
    contents = []

    properties = conformer.properties
    contents.append(self.get_stage1_header(conformer))
    contents.append(
        self.get_adjacency_code_and_hydrogens(conformer.bond_topologies[0]))
    contents.append(self.get_ids(conformer, 'stage1'))
    contents.append(self.get_system(properties))
    contents.append(self.get_stage1_timings(properties))
    contents.append(self.get_gradient_norms(conformer, spacer=' '))
    contents.append(
        self.get_coordinates(conformer.bond_topologies[0], conformer))
    contents.append(
        self.get_frequencies_and_intensities(properties, header=False))

    return ''.join(contents)

  def process_stage2_proto(self, conformer):
    """Return the contents of conformer as a string in SMU7 stage2 file format.

    This is for the stage2 format which is at the end of the pipeline.

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      A string representation of the protocol buffer in Uni Basel's file format.
    """
    contents = []

    properties = conformer.properties
    contents.append(self.get_stage2_header(conformer))
    contents.append(self.get_database(conformer))
    contents.append(self.get_error_codes(properties))
    contents.append(
        self.get_adjacency_code_and_hydrogens(conformer.bond_topologies[0]))
    contents.append(self.get_ids(conformer, 'stage2'))
    contents.append(self.get_system(properties))
    contents.append(self.get_stage2_timings(properties))
    contents.append(self.get_bonds(conformer.bond_topologies[0], properties))
    contents.append(self.get_gradient_norms(conformer, spacer='         '))
    contents.append(
        self.get_coordinates(conformer.bond_topologies[0], conformer))
    contents.append(self.get_rotational_constants(conformer))
    contents.append(self.get_symmetry_used(properties))
    contents.append(
        self.get_frequencies_and_intensities(properties, header=True))
    contents.append(self.get_gaussian_sanity_check(properties))
    contents.append(self.get_normal_modes(properties))
    contents.append(self.get_properties(conformer))
    contents.append(self.get_diagnostics(properties))
    contents.append(self.get_atomic_block(properties))
    contents.append(self.get_homo_lumo(properties))
    contents.append(self.get_excitation_energies_and_oscillations(properties))
    contents.append(
        self.get_nmr_isotropic_shieldings(conformer.bond_topologies[0],
                                          properties))
    contents.append(
        self.get_partial_charges(conformer.bond_topologies[0], properties))
    contents.append(self.get_polarizability(properties))
    contents.append(self.get_multipole_moments(properties))

    return ''.join(contents)


class Atomic2InputWriter:
  """From conformer, produces the input file for the (fortran) atomic2 code."""

  def __init__(self):
    pass

  def get_filename_for_atomic2_input(self, conformer, bond_topology_idx):
    """Returns the expected filename for an atomic input."""
    if bond_topology_idx:
      return '{}.{:06d}.{:03d}.{:02d}.inp'.format(
        smu_utils_lib.get_composition(
          conformer.bond_topologies[bond_topology_idx]),
        conformer.conformer_id // 1000,
        conformer.conformer_id % 1000,
        bond_topology_idx)
    else:
      return '{}.{:06d}.{:03d}.inp'.format(
        smu_utils_lib.get_composition(
          conformer.bond_topologies[bond_topology_idx]),
        conformer.conformer_id // 1000,
        conformer.conformer_id % 1000)

  def get_mol_block(self, conformer, bond_topology_idx):
    """Returns the MOL file block with atoms and bonds.

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      list of strings
    """
    contents = []
    contents.append('\n')
    contents.append('{:3d}{:3d}  0  0  0  0  0  0  0  0999 V2000\n'.format(
        len(conformer.bond_topologies[bond_topology_idx].atoms),
        len(conformer.bond_topologies[bond_topology_idx].bonds)))
    for atom_type, coords in zip(
        conformer.bond_topologies[bond_topology_idx].atoms,
        conformer.optimized_geometry.atom_positions):
      contents.append(
          '{:10.4f}{:10.4f}{:10.4f} {:s}   0  0  0  0  0  0  0  0  0  0  0  0\n'
          .format(
              smu_utils_lib.bohr_to_angstroms(coords.x),
              smu_utils_lib.bohr_to_angstroms(coords.y),
              smu_utils_lib.bohr_to_angstroms(coords.z),
              smu_utils_lib.ATOM_TYPE_TO_RDKIT[atom_type][0]))
    for bond in conformer.bond_topologies[bond_topology_idx].bonds:
      contents.append('{:3d}{:3d}{:3d}  0\n'.format(bond.atom_a + 1,
                                                    bond.atom_b + 1,
                                                    bond.bond_type))

    return contents

  def get_energies(self, conformer):
    """Returns the $energies block.

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      list of strings
    """
    contents = []
    contents.append('$energies\n')
    contents.append('#              HF              MP2          '
                    'CCSD         CCSD(T)        T1 diag\n')

    def format_field(field_name):
      return '{:15.7f}'.format(getattr(conformer.properties, field_name).value)

    contents.append('{:7s}'.format('3') +
                    format_field('single_point_energy_hf_3') +
                    format_field('single_point_energy_mp2_3') + '\n')
    contents.append('{:7s}'.format('4') +
                    format_field('single_point_energy_hf_4') +
                    format_field('single_point_energy_mp2_4') + '\n')
    contents.append('{:7s}'.format('2sp') +
                    format_field('single_point_energy_hf_2sp') +
                    format_field('single_point_energy_mp2_2sp') +
                    format_field('single_point_energy_ccsd_2sp') +
                    format_field('single_point_energy_ccsd_t_2sp') + '\n')
    contents.append('{:7s}'.format('2sd') +
                    format_field('single_point_energy_hf_2sd') +
                    format_field('single_point_energy_mp2_2sd') +
                    format_field('single_point_energy_ccsd_2sd') +
                    format_field('single_point_energy_ccsd_t_2sd') +
                    format_field('diagnostics_t1_ccsd_2sd') + '\n')
    contents.append('{:7s}'.format('3Psd') +
                    format_field('single_point_energy_hf_3psd') +
                    format_field('single_point_energy_mp2_3psd') +
                    format_field('single_point_energy_ccsd_3psd') + '\n')
    contents.append('{:7s}'.format('C3') +
                    format_field('single_point_energy_hf_cvtz') +
                    format_field('single_point_energy_mp2ful_cvtz') + '\n')
    contents.append('{:7s}'.format('(34)') +
                    format_field('single_point_energy_hf_34') +
                    format_field('single_point_energy_mp2_34') + '\n')

    return contents

  def get_frequencies(self, conformer):
    """Returns the $frequencies block.

    Note that the only non-zero frequencies are shown. Generally, each
    conformer will have 6 zero frequencies for the euclidean degrees of freedom
    but some will only have 5. Any other number is considered an error.

    Args:
      conformer: dataset_pb2.Conformer

    Returns:
      list of strings

    Raises:
      ValueError: if number of zero frequencies is other than 5 or 6
    """
    contents = []

    trimmed_frequencies = [
        v for v in conformer.properties.harmonic_frequencies.value if v != 0.0
    ]

    contents.append('$frequencies{:5d}{:5d}{:5d}\n'.format(
        len(trimmed_frequencies), 0, 0))
    line = ''
    for i, freq in enumerate(trimmed_frequencies):
      line += '{:8.2f}'.format(freq)
      if i % 10 == 9:
        contents.append(line + '\n')
        line = ''
    if line:
      contents.append(line + '\n')
    return contents

  def process(self, conformer, bond_topology_idx):
    """Creates the atomic input file for conformer."""
    if (conformer.properties.errors.status < 0 or
        conformer.properties.errors.status > 3 or
        # While we should check all the fields, this is conveinient shortcut.
        not conformer.properties.HasField('single_point_energy_hf_3') or
        not conformer.properties.HasField('single_point_energy_mp2_3')):
      raise ValueError(f'Conformer {conformer.conformer_id} is lacking required info '
                       'for generating atomic2 input. Maybe you need to query the complete DB?')

    contents = []
    contents.append(
      'SMU {}, RDKIT {}, bt {}({}/{}), geom opt\n'.format(
        conformer.conformer_id,
        conformer.bond_topologies[bond_topology_idx].smiles,
        conformer.bond_topologies[bond_topology_idx].bond_topology_id,
        bond_topology_idx + 1,
        len(conformer.bond_topologies)))
    contents.append(smu_utils_lib.get_original_label(conformer) + '\n')

    contents.extend(self.get_mol_block(conformer, bond_topology_idx))
    contents.extend(self.get_energies(conformer))
    contents.extend(self.get_frequencies(conformer))
    contents.append('$end\n')

    return ''.join(contents)


NEGATIVE_ZERO_RE = re.compile(r'-(0\.0+)\b')


def check_dat_formats_match(original, generated):
  """Checks whether a regenerated .dat format matches the original.

  There are several known cases where output can be non-meaningfully different.

  Args:
    original: list of lines of a .dat file
    generated: list of lines of regenerated .dat file

  Raises:
    WrongNumberOfLinesError: when lengths don't match
    RegeneratedLinesError: when regenerated files contains lines not in
      original
    LineOrderError: when regenerated lines are the same, but in the wrong order
  """

  def normalize_lines(lines):
    # The original file has several coordinates stored as -0.0, which creates
    # mismatches when compared with the corresponding 0.0 in generated files.
    lines = [NEGATIVE_ZERO_RE.sub(r' \1', s).rstrip() for s in lines]
    # This code removes any blank lines at the very end.
    cnt = 0
    while not lines[-(cnt + 1)]:
      cnt += 1
    if cnt == 0:
      return lines
    return lines[:-cnt]

  fixed_original = normalize_lines(original)
  fixed_generated = normalize_lines(generated)

  # Check if the modified lines match the original.
  missing_lines = set(fixed_original) - set(fixed_generated)
  excess_lines = set(fixed_generated) - set(fixed_original)
  if missing_lines or excess_lines:
    raise RegeneratedLinesError(missing_lines, excess_lines)

  # Now check the order of the lines generated
  for idx, (orig, regen) in enumerate(zip(fixed_original, fixed_generated)):
    if orig != regen:
      raise LineOrderError(idx, orig, regen)
