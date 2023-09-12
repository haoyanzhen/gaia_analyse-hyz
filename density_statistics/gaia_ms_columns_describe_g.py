import pandas as pd

dd = pd.read_csv('/media/hyz/dwarfcave/data/gaiaDR3/ms/GaiaSource_786097-786431.csv',comment='#',
                 usecols=['ra','dec','ra_error','dec_error','phot_g_mean_mag','phot_g_mean_flux_over_error',
                          'parallax','parallax_over_error','radial_velocity','radial_velocity_error','bp_rp',
                          'distance_gspphot','distance_gspphot_upper','ag_gspphot','ebpminrp_gspphot'],nrows=100000)
dd.describe().to_csv('gaia_ms_columns_describe.csv',float_format='%.03f')