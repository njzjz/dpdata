from dpdata.format import Format
try:
    import rdkit.Chem
except ModuleNotFoundError:
    pass
import dpdata.rdkit.utils


@Format.register("mol")
@Format.register("mol_file")
class MolFormat(Format):
    def from_bond_order_system(self, file_name, **kwargs):
        return rdkit.Chem.MolFromMolFile(file_name, sanitize=False, removeHs=False)
       

    def to_bond_order_system(self, mol, data, file_name, frame_idx=0, **kwargs):
        assert (frame_idx < self.get_nframes())
        rdkit.Chem.MolToMolFile(mol, file_name, confId=frame_idx)


@Format.register("sdf")
@Format.register("sdf_file")
class SdfFormat(Format):
    def from_bond_order_system(self, file_name, **kwargs):
        '''
        Note that it requires all molecules in .sdf file must be of the same topology
        '''
        mols = [m for m in rdkit.Chem.SDMolSupplier(file_name, sanitize=False, removeHs=False)]
        if len(mols) > 1:
            mol = dpdata.rdkit.utils.combine_molecules(mols)
        else:
            mol = mols[0]
        return mol
       
    def to_bond_order_system(self, mol, data, file_name, frame_idx=-1, **kwargs):
        sdf_writer = rdkit.Chem.SDWriter(file_name)
        if frame_idx == -1:
            for ii in range(data['coords'].shape[0]):
                sdf_writer.write(mol, confId=ii)
        else:
            assert (frame_idx < data['coords'].shape[0])
            sdf_writer.write(mol, confId=frame_idx)
        sdf_writer.close()