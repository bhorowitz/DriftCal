*DriftCal*
Calibration Routine for Driftscan Telescope Data

PURPOSE: A primarily purpose-built code for the absolute calibration of drifts of the Palomar QUEST Data. It can be extended for use with other driftscan data.

KEYWORDS: Astronomy, Calibration, Driftscan, QUEST

DESCRIPTION: A driftscan is a method of astronomical observation where the telescope is held at a fixed position and data is taken as the sky moves overhead. This produces an extremely thin strip of data (in general constant DEC and long RA), which is highly variable due to cloud cover and changes in sky brightness. This program corrects (provides a zero-point) for this by dividing each strip into segments based on RA and finding standard field stars from the UCAC database.

DEPENDANCIES: Various path dependancies are layed out in config.py. Most important is to have the UCAC catalog already installed. More information about this catalog can be found here: http://www.usno.navy.mil/USNO/astrometry/optical-IR-prod/ucac

PERLUTILS: There exists an early perl version of the code under PerlUTILS which can do every step of the calibration seperately (for troubleshooting purposes).

AUTHOR:
Benjamin Horowitz (Yale '14)
benjamin.a.horowitz@yale.edu 