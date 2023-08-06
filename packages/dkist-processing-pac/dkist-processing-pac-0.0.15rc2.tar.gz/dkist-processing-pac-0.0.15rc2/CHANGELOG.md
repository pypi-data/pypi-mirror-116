# Changelog
All notable changes to this project will be documented here.

This project adheres (or at least attempts to) to [Semantic Versioning](http://semver.org).

## Upcoming
### Changed
 - Fit recipe split into init val file and file with fit switches
 - Updated noise estimation to use noise floor instead of readnoise
 - Removed all mention of linear retarded from code
 - Removed generation of blank *Cal objects for instruments. No instruments need these anymore.
 - Better handling of NaN values in Drawers
 - Initial values for all parameters now printed during fit status header
 - Replaced debug.py with debug.sh, which is conda env aware
 - Get instrument header keys from actual instrument pipeline modules

### Added
 - Debug function to quickly setup the variables/objects used for a fit
 - Ability to specify position during Drawer's `plot_curves`
 - Ability to add random (or constant) dark signal to synthetic data
 - Option to set global retardance values during GroupCal fits

### Fixed
 - Tiny bug that caused error when remaking the testing data

## 0.14.4 - 2020.10.26
### Added
 - Better cleanup of multiprocessing resources at the end of fits
 - ``__del__`` methods to CU and TM parameter classes
 - Option to save any dummy polcal *Cal objects in a directory other than the fake raw data dir

### Changed
 - Default shape of fake CryoNIRSP data

### Fixed
 - Better(?) date parsing from FITS headers
 - Ability to deal with MemoryError on large fake data arrays
 - Obstime conflict on fake DLNIRSP data

## 0.14.3 - 2020.07.16
### Added
 - Revived sin perturbation to S_in in fake data and made it more complete (phase, noise)

### Fixed
 - VTF fake data now actually has 4 modulation states

## 0.14.2 - 2020.05.18
### Fixed
 - ``queue.get`` now will timeout and try again if it gets hung
 - Wait to push on to the multiproc queue if the queue has a lot of results waiting in it

### Added
 - Ability to stop multiproc fitting with keyboard interrupt and still save current results

### Changed
 - Replaced "defaults.ini" with "constants.yml"
 - Removed `dkist_data_model` dependency

## 0.14.1 - 2020.05.01
### Added
 - More suffix awareness in `gen_fake_data`
 - Catch NaN errors during fitting and record garbage results in this case, instead of dying
 - "super_name" option to `FittingFramework` that will precede any other thread names
 
### Changed
 - Default suffix is now "FITS"

## 0.14.0 - 2020.4.2
### Added
 - VTF instrument keywords
 - Ability to generate fake VTF data
 - ``noprint`` option that suppresses live updates of free parameters

### Changed
 - Initial value of I_sys now taken from data clear measurements
 - Modulation matrix is now fit directly with Mx4 variables
 - Temporary TM and CU fit par files are initialized with data header
 - Updated telescope parameter database
 - Default fit uses ``leastsq`` and recipes have no bounds
 - Error raised if Clear Flux is too low

### Fixed
 - TM fit output files now preserve input data headers
 - Improved error handling in `TelescopeModel.load_from_database`
 - Small bug that prevent make dlnirsp data with ``--no-dhs``
 - Better/correct error reporting if recipe is missing required keyword
 - Better formatting of fit status strings

## 0.13.0 - 2020.1.28
### Added
 - Very basic framework for computing uncertainties from data and using them to weight fits
 - Can give optional ``value`` entries to (x, tau) parameters in fitting recipe 
 - Fit recipe common option for setting global values of ``t_ret`` and ``t_pol``
 
### Changed
 - All SPEC-0122 keywords now live in a single file
 - SPEC-0122 keywords updated to Rev. B
 - All operations now done as 64-bit floating point
 - Telescope geometry calculation for fake data is more correct
 
### Fixed
  - Bad PROC name when saving fit statistics in multi-thread mode
  
## 0.12.1 - 2019.11.18
### Added
 - ``--no-dhs`` option to `pac_fake_data` that produces PA&C Module-ready data
 
### Changed
 - Don't use dark CS step as reference image when loading Drawer from dir
 
### Fixed
 - Failing tests caused by addition of dark CS steps

## 0.12.0 - 2019.11.14
### Added 
 - Fake Calibration Sequences are generated with dark frames
 - Read Noise command line option to `gen_fake_data`
 - `pac_fake_data` shell entry point. Finally!
 
### Changed
 - Don't make blank cals for CryoNIRSP
 - `print_truth` now defaults to looking for "truth.pkl"

## 0.11.4 - 2019.11.11
### Changed
 - Fake data and baseline recipe updated for optically contacted retarder with magnitude of 82.8 degrees
 - Changed default modulation matrix for DL-NIRSP to be DH's "O540"
 - `tag` now reports line numbers
 - Output of FitCUParams now has header copied from input Drawer
 
### Added
 - Can make legacy 2D fake data
 - PolCal generation for CryoNIRSP
 - Drawer ingestion of CryoNIRSP header values
 
### Fixed
 - Error in how parallactic angle is applied in calculation of inverse TM
 - MCMC stuff updated for 3D data
 - `pac_demod_err` now uses default telescope_db

## 0.11.3 - 2019.09.17
### Changed
 - DL-NIRSP data's size is inferred from mask

### Fixed
 - Added manual `__version__` to package

## 0.11.2 - 2019.09.09
### Changed
 - Removed astropy_helpers dependency

## 0.11.1 - 2019.09.06
### Added
 - Collection of Calibration Sequences that can be used to make fake Drawers
 
### Changed
 - ViSP fake data default to 3D

### Fixed
 - Bug in modulator state identification in fake Cal frames
 - Fake data instrument and CAM headers stay as those defined in gen_fake_data
 - ViSP data are made at 588 nm, the same as used by ViSP_Pipeline's `gen_fake_data`

## 0.11.0 - 2019.08.16
### Changed
 - All fitting and demodulation modules now assume 3D input data
 - \[CU|TM\]_params shapes are correctly updated when loaded from FITS
 - `pac_demod` assumes default package telescope_db
 - Better/more complete cleanup of \[CU|TM\]_param temp file

## 0.10.2 - 2019.08.07
### Changed
 - Multiproc splits up total number of fits over a fixed number of threads
 - Much improved files-open performance when saving CU/TM intermediate parameters
 - Updated tests
 
### Added
 - PolCal generation for DLNIRSP

## 0.10.1 - 2019.6.19
### Changed
 - Updated code for sunpy > 1.0
 - Updated testing for astropy > 3.0

## 0.10.0 - 2019.5.20
### Added
 - Ability to specify fit recipe via command line `-m` option
 - Table angle automatically tracks parallactic and can be offset by fixed amount
 - Fits can now be parallelized over each SoCC in Drawer
 - Ability to specify detector read noise in synthetic data
 - Tex-ification of Telescope Model parameters
 - Save parameters after _every_ SoCC fit
 - Fitting recipe for Optically Contacted retarder
 - Can specify custom modulation matrix when generating synthetic data
 - Ability to have sinusoidal perturbation in I_sys in synthetic data

### Changed
 - `gen_fake_data` now part of main package
 - Updated telescope_db and placed in main package
 - M36 fitter now saves CU parameters in addition to TM parameters
 - Noise in synthetic data is now specified as SNR
 - All randomized synthetic parameters (but not noise) can be seeded for repeatability
 - Equation for mirror Mueller matrix no longer "glows"
 - Normalization of modulation matrix is now always with the same modulation state
 - Can now specify TM parameter ranges in fitting recipes

### Fixed
 - Removed extraneous linear_ret argument from command line calls
 - Raise correct error when specified fitting recipe is not found (finally!)

## 0.9.3 - 2019.3.12
### Fixed
 - Correct DKIST longitude for parallactic angle and fake data generation
 
### Changed
 - Removed PAC__999 (CS Step #) from synthetic data headers
 - Default start time no longer the same as ViSP_Pipeline's default start time

## 0.9.2 - 2018.1.8
### Fixed
 - Required auxiliary files (e.g., fitting recipes) are now correctly included when installing

## 0.9.1 - 2019.1.7
### Fixed
 - Fake Cals now have required VISP_YYY header value
 - Fixed overflow error in some fake data generation

### Changed
 - Truth pickles now contain M12 values
 - Updated fake data defaults to jive with standard ViSP fake data
 - Updated online docs

## 0.9.0 - 2018.12.21
### Fixed
 - Don't try to correct intensity trend on blank PCD when adding PCDs
 - Don't try to load 'fitaux' directory when looking for files
 - Parameters with negative limits now have limits expanded correctly

### Added
 - Updated PolCal Model based on Nov. 2018 discussions:
   - Transmission of polarizer and retarder as parameter
   - Parameterization of S_in = I_sys \[1, Q_in, U_in, V_in\]
   - Switches to control application of M12, TM when computing S_out
 - Options to change fake data based on Nov. 2018 model discussions (see above)
 - Function to use clear measurements to remove intensity trends within CS
 - Dresser class to hold Drawer (nee PCD) objects
 - CUModelParams class to hold best-fit CU model parameters
 - CalibrationSequence can now load parameters from dictionary

### Changed
 - Only update free parameters in status message. Fixed parameters are printed once
 - Truth pickles from gen_fake_data are now stored and printed as dictionaries
 - Finally(!) give a useful error when no files are found
 - Major refactor of common fitting code and specific uses of it
 - Moved linear retarder model into normal CU Model code
 - Better texification of MCMC plot labels
 - Sped up fits

## 0.8.2 - 2018.11.6
### Fixed
 - Case of config file options is now preserved
 
### Changed
 - `telescope_db` in optional config file takes precedence over ``-t`` option when calling from command line
 - Only compute S once during each fit iteration

## 0.8.1 - 2018.10.23
### Fixed
 - No longer assume that 'fit_b' will always be specified in main() call

## 0.8.0 - 2018.10.02
### Added
 - Framework to compute and monitor X12 from continuum polarization info provided by IPAs
 - Baseline method to fit \tau_12 mirror parameter
 - Can now specify telescope_db on the command line when calling pac_* scripts
 - Online documentation

## 0.7.0 - 2018.09.19
### Fixed
 - Testing data is now in the proper format
 - Remove unneeded (sometimes error-causing) 'fit_b' keyword if not using a linear retarder
 - Updated gen_fake_linear_data to use new dkist_data_model

### Added
 - MCMC analysis of previous PA&C fits
 - Generation of Demodulation uncertainty based on MCMC analysis
 - Ability to generate fake uncertainty frames for fake Calibration objects
 - Ability to read FITS dates in either 'fits' or 'iso' format
 - Option to include parallactic rotation in inverse TM matrix
 - Ability to generate DHS-style data with linear retarder

### Changed
 - Minimization is now done with an lmfit.Minimizer object so that this object can be captured for further analysis (e.g., QA)

## 0.6.0 - 2018.07.13
### Changed
 - Updated interaction with dkist_data_model to line up with commit 93a86c5 of that package

## 0.5.3 - 2018.07.13
### Fixed
 - Removed FS-breaking special characters from fake data file names
 - Default argument to -N (noise) parameter on gen_fake_data command line interface no longer breaks program

### Added
 - Option to specify noise level when calling gen_fake_data from the command line

## 0.5.2 - 2018.06.01
### Added
 - Ability to generate DHS-style ViSP SoCCs for use by ViSP_Pipeline
 - Quick ViSP SoCC generation command line script

## 0.5.1 - 2018.05.09
### Fixed
 - Fake linear retarder data are now generated with correct py values

### Added
 - Option to fit/keep fixed the linear retarder's diattenuation parameter, b
 - Option to fit/keep fixed b in fake linear retarder data

### Changed
 - Better attempts at correct SoCC/CS terms

## 0.5.0 - 2018.05.09
### Changed
 - CU model updated based on C. Beck's April 2018 documents
 - Calibration Sequence recipes updated based on C. Beck's April 2018 documents

### Added
 - Option to choose between linear and elliptical retarder in CU model fits
 - Lookup table for polarizer py values

## 0.4.0 - 2018.05.02
### Added
 - User can choose to not include M12 in inverse Telescope Model
 - Fake ViSP data now have useful, non-random SPEC-0122 header entries
 - Can generate fake ViSP *Cal files that don't affect PAC data

## 0.3.0 - 2018.04.20
### Changed
 - Total passthrough of PCD headers to demodulation matrices
 - Fitting status messages are now truncated to fit in current terminal. To a point.
 - Fitting status messages don't display when running as a child of a multiprocessing Processs

## 0.2.0 - 2018.03.27
### Fixed
 - GOS angles used to create fake data are no longer totally wrong (radian/degree error)

### Added
 - Can use the same modulation used to create AdW's fake ViSP data
 - Test function to explore parameter space for a single fit

### Changed
 - Support for SPEC-0122 style fake data
 - Slightly loosened tolerance on check of correct telescope inverse matrix
 - Telescope geometry and GOS element angles are now expected to be degrees, a la SPEC-0122
 - Higher precision in optical element Mueller Matrix calculations

## 0.1.0 - 2018.03.07
Initial release