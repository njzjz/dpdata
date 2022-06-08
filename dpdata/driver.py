"""Driver plugin system."""
from typing import Callable, TYPE_CHECKING

from .plugin import Plugin
from abc import ABC, abstractmethod

import dpdata

if TYPE_CHECKING:
    import ase

class Driver(ABC):
    """The base class for a driver plugin. A driver can
    label a pure System to generate the LabeledSystem.

    See Also
    --------
    dpdata.plugins.deepmd.DPDriver : an example of Driver
    """
    __DriverPlugin = Plugin()

    @staticmethod
    def register(key: str) -> Callable:
        """Register a driver plugin. Used as decorators.
        
        Parameter
        ---------
        key: str
            key of the plugin.
        
        Returns
        -------
        Callable
            decorator of a class

        Examples
        --------
        >>> @Driver.register("some_driver")
        ... class SomeDriver(Driver):
        ...     pass
        """
        return Driver.__DriverPlugin.register(key)

    @staticmethod
    def get_driver(key: str) -> "Driver":
        """Get a driver plugin.
        
        Parameter
        ---------
        key: str
            key of the plugin.
        
        Returns
        -------
        Driver
            the specific driver class
        
        Raises
        ------
        RuntimeError
            if the requested driver is not implemented
        """
        try:
            return Driver.__DriverPlugin.plugins[key]
        except KeyError as e:
            raise RuntimeError('Unknown driver: ' + key) from e
    
    def __init__(self, *args, **kwargs) -> None:
        """Setup the driver."""

    @abstractmethod
    def label(self, data: dict) -> dict:
        """Label a system data. Returns new data with energy, forces, and virials.
        
        Parameters
        ----------
        data : dict
            data with coordinates and atom types
        
        Returns
        -------
        dict
            labeled data with energies and forces
        """
        return NotImplemented

    def minimize(self, data: dict) -> dict:
        """Minimize the geometry.

        If not implemented, this method calls ASE to minimize.

        Parameters
        ----------
        data : dict
            data with coordinates and atom types
        
        Returns
        -------
        dict
            labeled data with minimized coordinates, energies, and forces
        """
        from ase.optimize import BFGS
        
        system = dpdata.System(data=data)
        # list[Atoms]
        structures = system.to_ase_structure()
        labeled_system = dpdata.LabeledSystem()
        for atoms in structures:
            atoms.calc = self.ase_calculator
            dyn = BFGS(atoms)
            dyn.run(fmax=5e-3)
            ls = dpdata.LabeledSystem(atoms, fmt="ase/structure")
            labeled_system.append(ls)
        return labeled_system.data

    @property
    def ase_calculator(self) -> "ase.calculators.calculator.Calculator":
        """Returns an ase calculator based on this driver."""
        from .ase_calculator import DPDataCalculator
        return DPDataCalculator(self)


@Driver.register("hybrid")
class HybridDriver(Driver):
    def __init__(self, drivers: dict) -> None:
        self.drivers = []
        for key, driver in drivers.items():
            if isinstance(driver, Driver):
                self.drivers.append(driver)
            elif isinstance(driver, dict):
                self.drivers.append(Driver.get_driver(key)(**driver))
            else:
                raise TypeError("driver should be Driver or dict")

    def label(self, data: dict) -> dict:
        for ii, driver in enumerate(self.drivers):
            lb_data = driver.label(data)
            if ii == 0:
                labeled_data = lb_data
            else:
                labeled_data['energies'] += lb_data ['energies']
                labeled_data['forces'] += lb_data ['forces']
        return labeled_data