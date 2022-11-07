#!/bin/sh

GEOMS="""
initial_geometry_energy initial_geometry_energy_deprecated
initial_geometry_gradient_norm initial_geometry_gradient_norm_deprecated
optimized_geometry_energy optimized_geometry_energy_deprecated
optimized_geometry_gradient_norm optimized_geometry_gradient_norm_deprecated
rotational_constants rotational_constants_deprecated
nuclear_repulsion_energy nuclear_repulsion_energy_deprecated
"""

# Done manually on just a few files
#molecule rdkit_molecule
# Molecule RDKitMolecule
M_TO_RM="""
SmuMolecule TopologyMolecule
smu_molecule topology_molecule
"""

CONFORMER="""
Conformer Molecule
conformer molecule
CONFORMER MOLECULE
Chem.Molecule Chem.Conformer
AddMolecule AddConformer
.GetMolecule .GetConformer
"""

CONFORMER_PART2="""
confid molid
conf_id mol_id
cid mid
conf mol
molidence confidence
molig config
amid acid
mollicting conflicting
mollict conflict
molormer conformer
"""

FATE_PART1="""
Molecule.FATE Properties.FATE
.fate .properties.errors.fate
"""

FATE_PART2="""
Molecule.FateCategory Properties.FateCategory
"""

FATE_PART3="""
FATE_GEOMETRY_OPTIMIZATION_PROBLEM FATE_FAILURE_GEO_OPT
FATE_DISASSOCIATED FATE_FAILURE_TOPOLOGY_CHECK
FATE_DISCARDED_OTHER FATE_FAILURE_STAGE2
FATE_NO_CALCULATION_RESULTS FATE_FAILURE_NO_RESULTS
FATE_CALCULATION_WITH_SERIOUS_ERROR FATE_ERROR_SERIOUS
FATE_CALCULATION_WITH_MAJOR_ERROR FATE_ERROR_MAJOR
FATE_CALCULATION_WITH_MODERATE_ERROR FATE_ERROR_MODERATE
FATE_CALCULATION_WITH_WARNING_SERIOUS FATE_SUCCESS_ALL_WARNING_SERIOUS
FATE_CALCULATION_WITH_WARNING_VIBRATIONAL FATE_SUCCESS_ALL_WARNING_MEDIUM_VIB
FATE_SUCCESS FATE_SUCCESS_ALL_WARNING_LOW
"""

FATE_PART4="""
FATE_SUCCESS_ALL_WARNING_LOW_ALL FATE_SUCCESS_ALL
"""

WHICH_DB="""
which_database which_database_deprecated
"""

SIMPLE_FIELDS="""
molecule_id mol_id
smiles_openbabel smiles_openbabel
topology_id topo_id
duplicate_of duplicates_found
duplicated_by duplicate_of
warn_t1 warn_t1
warn_t1_excess warn_delta_t1
warn_bse_b5_b6 warn_bse_b6
warn_bse_cccsd_b5 warn_bse_eccsd
warn_exc_lowest_excitation warn_exc_ene
warn_exc_smallest_oscillator warn_exc_osmin
warn_exc_largest_oscillator warn_exc_osmax
warn_vib_linearity warn_vib_linear
warn_vib_imaginary warn_vib_imag
warn_num_neg warn_bsr_neg
bond_topology_id topo_id
rotcon brot
harmonic_frequencies vib_freq
harmonic_intensities vib_intens
zpe_unscaled vib_zpe
normal_modes vib_mode
bond_separation_energy_atomic_b5_um_ci at2_um_b5_ereac_unc
bond_separation_energy_atomic_b5_um at2_um_b5_ereac
bond_separation_energy_atomic_b5 at2_std_b5_ereac
bond_separation_energy_atomic_b6_um_ci at2_um_b6_ereac_unc
bond_separation_energy_atomic_b6_um at2_um_b6_ereac
bond_separation_energy_atomic_b6 at2_std_b6_ereac
bond_separation_energy_eccsd_um_ci at2_um_eccsd_ereac_unc
bond_separation_energy_eccsd_um at2_um_eccsd_ereac
bond_separation_energy_eccsd at2_std_eccsd_ereac
atomization_energy_excluding_zpe_atomic_b5_um_ci at2_um_b5_eae_unc
atomization_energy_excluding_zpe_atomic_b5_um at2_um_b5_eae
atomization_energy_excluding_zpe_atomic_b5 at2_std_b5_eae
atomization_energy_excluding_zpe_atomic_b6_um_ci at2_um_b6_eae_unc
atomization_energy_excluding_zpe_atomic_b6_um at2_um_b6_eae
atomization_energy_excluding_zpe_atomic_b6 at2_std_b6_eae
atomization_energy_excluding_zpe_eccsd_um_ci at2_um_eccsd_eae_unc
atomization_energy_excluding_zpe_eccsd_um at2_um_eccsd_eae
atomization_energy_excluding_zpe_eccsd at2_std_eccsd_eae
atomization_energy_including_zpe_atomic_b5_um_ci at2_um_b5_ea0_unc
atomization_energy_including_zpe_atomic_b5_um at2_um_b5_ea0
atomization_energy_including_zpe_atomic_b5 at2_std_b5_ea0
atomization_energy_including_zpe_atomic_b6_um_ci at2_um_b6_ea0_unc
atomization_energy_including_zpe_atomic_b6_um at2_um_b6_ea0
atomization_energy_including_zpe_atomic_b6 at2_std_b6_ea0
atomization_energy_including_zpe_eccsd_um_ci at2_um_eccsd_ea0_unc
atomization_energy_including_zpe_eccsd_um at2_um_eccsd_ea0
atomization_energy_including_zpe_eccsd at2_std_eccsd_ea0
enthalpy_of_formation_0k_atomic_b5_um_ci at2_um_b5_hf0_unc
enthalpy_of_formation_0k_atomic_b5_um at2_um_b5_hf0
enthalpy_of_formation_0k_atomic_b5 at2_std_b5_hf0
enthalpy_of_formation_0k_atomic_b6_um_ci at2_um_b6_hf0_unc
enthalpy_of_formation_0k_atomic_b6_um at2_um_b6_hf0
enthalpy_of_formation_0k_atomic_b6 at2_std_b6_hf0
enthalpy_of_formation_0k_eccsd_um_ci at2_um_eccsd_hf0_unc
enthalpy_of_formation_0k_eccsd_um at2_um_eccsd_hf0
enthalpy_of_formation_0k_eccsd at2_std_eccsd_hf0
enthalpy_of_formation_298k_atomic_b5_um_ci at2_um_b5_hf298_unc
enthalpy_of_formation_298k_atomic_b5_um at2_um_b5_hf298
enthalpy_of_formation_298k_atomic_b5 at2_std_b5_hf298
enthalpy_of_formation_298k_atomic_b6_um_ci at2_um_b6_hf298_unc
enthalpy_of_formation_298k_atomic_b6_um at2_um_b6_hf298
enthalpy_of_formation_298k_atomic_b6 at2_std_b6_hf298
enthalpy_of_formation_298k_eccsd_um_ci at2_um_eccsd_hf298_unc
enthalpy_of_formation_298k_eccsd_um at2_um_eccsd_hf298
enthalpy_of_formation_298k_eccsd at2_std_eccsd_hf298
bond_separation_reaction_left at2_gen_bsr_left
bond_separation_reaction_right at2_gen_bsr_right
diagnostics_t1_ccsd_2sp_excess at2_gen_t1_exc
zpe_atomic_um_ci at2_um_zpe_unc
zpe_atomic_um at2_um_zpe
zpe_atomic at2_std_zpe
diagnostics_d1_ccsd_2sp wf_diag_d1_2sp
diagnostics_t1_ccsd_2sp wf_diag_t1_2sp
diagnostics_t1_ccsd_2sd wf_diag_t1_2sd
diagnostics_t1_ccsd_3psd wf_diag_t1_3psd
dipole_moment_hf_6_31gd elec_dip_hf_631gd
dipole_moment_pbe0_aug_pc_1 elec_dip_pbe0_augpc1
quadrupole_moment_hf_6_31gd elec_qua_hf_631gd
quadrupole_moment_pbe0_aug_pc_1 elec_qua_pbe0_augpc1
octopole_moment_hf_6_31gd elec_oct_hf_631gd
octopole_moment_pbe0_aug_pc_1 elec_oct_pbe0_augpc1
dipole_dipole_polarizability_pbe0_aug_pc_1 elec_pol_pbe0_augpc1
partial_charges_esp_fit_hf_6_31gd chg_esp_hf_631gd
partial_charges_esp_fit_pbe0_aug_pc_1 chg_esp_pbe0_augpc1
partial_charges_mulliken_hf_6_31gd chg_mul_hf_631gd
partial_charges_mulliken_pbe0_aug_pc_1 chg_mul_pbe0_augpc1
partial_charges_loewdin_hf_6_31gd chg_loe_hf_631gd
partial_charges_loewdin_pbe0_aug_pc_1 chg_loe_pbe0_augpc1
partial_charges_natural_nbo_hf_6_31gd chg_nat_hf_631gd
partial_charges_natural_nbo_pbe0_aug_pc_1 chg_nat_pbe0_augpc1
nmr_isotropic_shielding_b3lyp_6_31ppgdp nmr_b3lyp_631ppgdp
nmr_isotropic_shielding_b3lyp_aug_pcs_1 nmr_b3lyp_augpcs1
nmr_isotropic_shielding_pbe0_6_31ppgdp nmr_pbe0_631ppgdp
nmr_isotropic_shielding_pbe0_aug_pcs_1 nmr_pbe0_augpcs1
excitation_energies_cc2 exc_ene_cc2_tzvp
excitation_oscillator_strengths_cc2 exc_os_cc2_tzvp
homo_hf_3 orb_ehomo_hf_3
homo_hf_4 orb_ehomo_hf_4
homo_hf_6_31gd orb_ehomo_hf_631gd
homo_hf_cvtz orb_ehomo_hf_cvtz
homo_hf_tzvp orb_ehomo_hf_tzvp
homo_b3lyp_6_31ppgdp orb_ehomo_b3lyp_631ppgdp
homo_b3lyp_aug_pcs_1 orb_ehomo_b3lyp_augpcs1
homo_pbe0_6_31ppgdp orb_ehomo_pbe0_631ppgdp
homo_pbe0_6_311gd orb_ehomo_pbe0_6311gd
homo_pbe0_aug_pc_1 orb_ehomo_pbe0_augpc1
homo_pbe0_aug_pcs_1 orb_ehomo_pbe0_augpcs1
lumo_hf_3 orb_elumo_hf_3
lumo_hf_4 orb_elumo_hf_4
lumo_hf_6_31gd orb_elumo_hf_631gd
lumo_hf_cvtz orb_elumo_hf_cvtz
lumo_hf_tzvp orb_elumo_hf_tzvp
lumo_b3lyp_6_31ppgdp orb_elumo_b3lyp_631ppgdp
lumo_b3lyp_aug_pcs_1 orb_elumo_b3lyp_augpcs1
lumo_pbe0_6_31ppgdp orb_elumo_pbe0_631ppgdp
lumo_pbe0_6_311gd orb_elumo_pbe0_6311gd
lumo_pbe0_aug_pc_1 orb_elumo_pbe0_augpc1
lumo_pbe0_aug_pcs_1 orb_elumo_pbe0_augpcs1
single_point_energy_pbe0_6_311gd spe_check_pbe0_6311gd_tmol
single_point_energy_pbe0_6_311gd_mrcc spe_check_pbe0_6311gd_mrcc
single_point_energy_pbe0_6_311gd_orca spe_check_pbe0_6311gd_orca
single_point_energy_pbe0_6_311gd_cat spe_cation_pbe0_6311gd_tmol
single_point_energy_pbe0_6_311gd_cat_mrcc spe_cation_pbe0_6311gd_mrcc
single_point_energy_pbe0_6_311gd_cat_orca spe_cation_pbe0_6311gd_orca
single_point_energy_atomic_b5 spe_comp_b5
single_point_energy_atomic_b6 spe_comp_b6
single_point_energy_eccsd spe_comp_eccsd
single_point_energy_hf_2sp spe_std_hf_2sp
single_point_energy_hf_2sd spe_std_hf_2sd
single_point_energy_hf_3psd spe_std_hf_3psd
single_point_energy_hf_3 spe_std_hf_3
single_point_energy_hf_4 spe_std_hf_4
single_point_energy_hf_34 spe_std_hf_34
single_point_energy_hf_6_31gd spe_std_hf_631gd
single_point_energy_hf_tzvp spe_std_hf_tzvp
single_point_energy_hf_cvtz spe_std_hf_cvtz
single_point_energy_mp2_2sp spe_std_mp2_2sp
single_point_energy_mp2_2sd spe_std_mp2_2sd
single_point_energy_mp2_3psd spe_std_mp2_3psd
single_point_energy_mp2_3 spe_std_mp2_3
single_point_energy_mp2_4 spe_std_mp2_4
single_point_energy_mp2_34 spe_std_mp2_34
single_point_energy_mp2_tzvp spe_std_mp2_tzvp
single_point_energy_mp2ful_cvtz spe_std_mp2full_cvtz
single_point_energy_cc2_tzvp spe_std_cc2_tzvp
single_point_energy_ccsd_2sp spe_std_ccsd_2sp
single_point_energy_ccsd_2sd spe_std_ccsd_2sd
single_point_energy_ccsd_3psd spe_std_ccsd_3psd
single_point_energy_ccsd_t_2sp spe_std_ccsd_t_2sp
single_point_energy_ccsd_t_2sd spe_std_ccsd_t_2sd
single_point_energy_b3lyp_6_31ppgdp spe_std_b3lyp_631ppgdp
single_point_energy_b3lyp_aug_pcs_1 spe_std_b3lyp_augpcs1
single_point_energy_pbe0_6_31ppgdp spe_std_pbe0_631ppgdp
single_point_energy_pbe0_aug_pc_1 spe_std_pbe0_augpc1
single_point_energy_pbe0_aug_pcs_1 spe_std_pbe0_augpcs1
single_point_energy_pbe0d3_6_311gd spe_std_pbe0d3_6311gd
"""

COMPLEX_FIELDS="""
errors calc
atoms atom
bonds bond
source info
bond_topologies bond_topo
"""

THIS_REPLACE="${SIMPLE_FIELDS}"
#ARGS="-i"
ARGS=""

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
FILES=$(find ${SCRIPT_DIR}/.. -type f -maxdepth 4 | grep -v venv | grep -v dataset_pb2.py | grep -v rename.sh | egrep -v '\.(cc|h|pyc)$' | grep -v '~$')

#for f in ${FILES}; do
#    echo "$f"
#done

while IFS= read -r line; do
    if [ -z "$line" ]; then
       continue
    fi
    repl=($line)
    #echo "X: ${repl[0]}"
    #echo "Y: ${repl[1]}"
    "${HOME}/bin/multi-repl" ${ARGS} "${repl[0]}" "${repl[1]}" $FILES < /dev/tty
done <<< "$THIS_REPLACE"