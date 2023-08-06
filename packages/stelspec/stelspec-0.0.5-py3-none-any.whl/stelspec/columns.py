desc_so_ccf = {
'seq' : 'A number used to uniquely identify an entry in the database. This internal sequence number is actually the SOPHIE sequence number multiplied by 10. In case of n duplicates (due to disk problems on pcsophie) we add n to the SOPHIE sequence number for each occurrence.',
'bjd' : 'The barycentric julian date (julian date corrected to the barycenter of the solar system) at the middle of the exposure is provided for the fully public observations. For the observations with temporary limited access, the field is NULL.',

'sseq' : 'Sequence number of the series, defined as the sequence number of the first observation of the series.',
'slen' : 'Effective length of the series. It can be smaller than nexp (scheduled length).',
'nexp' : 'Scheduled length of the series. Some observers schedule long series and interrupt them when their goal is reached, or when some incident (like bad weather) commands it.',
'expno' : 'Index of a given observation in a series, starting from 1 for the first observation.',

'mask' : 'Name of the digital mask used to measure the radial velocity by cross-correlation (operation done in pixel space using the e2ds wavelength-calibrated spectrum). A mask is made of box-shaped "emission lines" corresponding to several thousand weak neutral metallic lines. The width of each box is specified by theoretical right and left wavelengths (at zero velocity) adapted to the strength of each line. The most frequently used masks are optimized for spectral types F0, G2, K0, K5, M4 and M5 and were originally designed for ELODIE and later adapted from HARPS.',
'ccf_offline' : 'A value of "0" indicates a standard automatic cross-correlation covering a ± 30 km/s interval, while a value of "1" is shown if the observer used the off-line DRS facility to derive cross-correlations with other masks and/or using other velocity windows.',
'rv' : 'Radial velocity measured by fitting a gaussian to the average cross-correlation function (CCF) over all orders having a satisfactory S/N ratio, and is corrected to the barycenter of the Solar System (km/s).',
'err' : 'estimated 1-sigma error on CCF radial velocity, derived from contrast and FWHM, best for S/N < 100.',
'dvrms' : 'Estimated 1-sigma radial-velocity uncertainty, based on photon noise alone, good for S/N > 100.',
'fwhm' : 'Full width at half maximum of the CCF dip (km/s). This is the FWHM of the average line profile for weak neutral metallic lines. Abnormally large fwhm values coupled with low contrast indicate no meaningful correlation was achieved. Double-peaked ccf (spectroscopic binaries, chance alignments) are not handled correctly in the automatic pipeline.', 
'span' : 'Bisector velocity span, a measure of line asymmetry (km/s). It represents the difference in line center between the top and bottom of the line profile. Is used to detect radial velocity changes due to motions (moving star spots) over the stellar surface.',
'maxcpp' : 'The maximum number of counts/pixel in the average CCF (expressed in electrons) is used to compute errors based on photon noise. Larger values indicate a better S/N ratio.',
'contrast' : 'Contrast of the CCF, expressed as percent depth of dip (%). This is a measure of the strength of the average weak neutral metallic absorption line profile, relative to the local normalized continuum.',
'lines' : 'Number of absorption lines used to compute the CCF. Orders with poor S/N ratio are not included in the final calculation.',
    
'sn26' : 'Gives the signal-to-noise ratio achieved at the center of order 26 [out of orders 0-38], corresponding to 5550 Å (near the center of the V band).',
'obstype' : 'The type of observation is assigned during the archiving process to distinguish between various types of observations on the sky: SCI, for a regular science exposure, TST, for tests, like for example to focus the telescope, and CAL for calibration, for example exposures on the blue sky.',
}

desc_so_spec = {
'seq' : desc_so_ccf['seq'],
'bjd' : desc_so_ccf['bjd'],
'sseq' : desc_so_ccf['sseq'],
'slen' : desc_so_ccf['slen'],
'nexp' : desc_so_ccf['nexp'],
'expno' : desc_so_ccf['expno'],
'sn26': desc_so_ccf['sn26'],
'mode' : 'Indicates whether the HE (high efficiency) or HR (high resolution) mode was used. See the spectrograph web page for details on the fiber throughput and corresponding spectral resolution.',
'obstype' : desc_so_ccf['obstype'],
'fiber_B' : 'This parameter indicates how the second fiber in a given A,B pair was used. Fiber_A contains the target spectrum. Possible values for fiber_B can be : DARK (no light admitted), SKY (exposure to the sky background) or WAVE (simultaneous Thorium-Argon lamp calibration). For 90% of SOPHIE spectra the second fiber contains the spectrum of either the sky (40%) or the Thorium-Argon calibration lamp (60%) depending on the scientific program.',
'exptime' : 'Actual exposure time in seconds.'
}

# ELODIE manual : Data reduction user's manual
# http://www.obs-hp.fr/guide/elodie/manuser2.html
desc_el_ccf = {
'datenuit': 'date of the beginning of the night of observation',
'imanum' : 'running number of the spectrum within the night (given in column dataset).',
'imatyp' : 'describes the focal plane configuration used for the observations. http://atlas.obs-hp.fr/elodie/500/imatyp.html',
'jdb' : 'Truncated barycentric julian date of mid-exposure (BJD-2400000.0).',
'exptim' : 'Exposure length; total cumulated exposure time expressed in seconds.',
'coment' : 'Optional comments on the finished exposure.',
'masque' : 'indicates which mask was used in the numerical cross-correlation. http://atlas.obs-hp.fr/elodie/500/mask.html',
'sn' : 'Signal to noise ratio; the mean signal to noise ratio per pixel in the spectral order number 47, i.e. near 555 nm, computed at the telescope by the data reduction software.',
'vfit' : 'barycentric radial velocity (km/s) derived from fitting a gaussian to the profile obtained from cross-correlating the extracted s2d spectrum with a numerical mask. Masks exist for F0 and K0 spectral types. Additional masks for A and M stars have been used. http://atlas.obs-hp.fr/elodie/500/vfit.html',
'sigfit' : 'sigma of the gaussian fitted to the cross-correlation profile.',
'ampfit' : 'amplitude of the gaussian curve fitted to the cross-correlation profile.',
'ctefit' : 'Normalized CCF continuum.'
}

desc_el_spec = {
'dataset' : desc_el_ccf['datenuit'],
'imanum' : desc_el_ccf['imanum'],
'data' : 'name of fits file',
'imatyp' : desc_el_ccf['imatyp'],
'exptime' : desc_el_ccf['exptim'],
'sn' : desc_el_ccf['sn'],
'vfit' : desc_el_ccf['vfit'],
'sigfit' : desc_el_ccf['sigfit'],
'ampfit' : desc_el_ccf['ampfit']
}
