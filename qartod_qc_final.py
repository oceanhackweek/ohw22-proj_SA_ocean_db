# -*- coding: utf-8 -*-

## QARTOD workflow

#Access data (data sample: PNBOIA buoy)


import numpy as np
import pandas as pd
from ioos_qc.config import Config
from ioos_qc.streams import PandasStream
import datetime
from ioos_qc.config import QcConfig
import matplotlib.pyplot as plt
import scipy.stats

def apply_qc(inp_aux, tinp_aux, zinp_aux, config):
    qc = QcConfig(config)
    
    qc_results = qc.run(
        inp=inp_aux,
        tinp=tinp_aux,
        zinp=zinp_aux)

    return qc_results

def plot_results(data, variable_name, results, title, test_name):
    time = data.cf["time"]
    obs = data[variable_name]
    qc_test = results["qartod"][test_name]

    qc_pass = np.ma.masked_where(qc_test != 1, obs)
    qc_suspect = np.ma.masked_where(qc_test != 3, obs)
    qc_fail = np.ma.masked_where(qc_test != 4, obs)
    qc_notrun = np.ma.masked_where(qc_test != 2, obs)

    fig, ax = plt.subplots(figsize=(15, 3.75))
    fig.set_title = f"{test_name}: {title}"
    
    ax.set_xlabel("Time")
    ax.set_ylabel("Observation Value")

    kw = {"marker": "o", "linestyle": "none"}
    ax.plot(time, obs,  label="obs", color="#A6CEE3")
    ax.plot(time, qc_notrun, markersize=2, label="qc not run", color="gray", alpha=0.2, **kw)
    ax.plot(time, qc_pass, markersize=4, label="qc pass", color="green", alpha=0.5, **kw)
    ax.plot(time, qc_suspect, markersize=4, label="qc suspect", color="orange", alpha=0.7, **kw)
    ax.plot(time, qc_fail, markersize=6, label="qc fail", color="red", alpha=1.0, **kw)
    ax.grid(True)

# Buoys
buoys = ['abrolhos','alcatrazes','imbituba','noronha']

for b in buoys:
  # Open buoy
  ds = pd.read_csv(b+'.csv')
  #print(b)
  
  # Rename columns
  ds = ds.rename(columns={'swvht1': 'wvht', 'tp1': 'tp', 'wvdir1': 'wvdir'})

  # Start of QC
  flags_dict={}
  pd_flags={}

  for var in ['wvht', 'tp', 'wvdir']:
      
      if var == 'wvht':
          fail_span = [0.1, 19.9]
          suspect_span = [0.2, 16]
            
          #spike_test
          suspect_threshold_spike = 25
          fail_threshold_spike = 30
          
          # flat_test (forced to pass, values have to be checked)
          tolerance = 0
          suspect_threshold_flat = 2
          fail_threshold_flat = 3

      elif var == 'tp':
          fail_span = [1.7, 30]
          suspect_span = [1.9, 25]
          
          #spike_test
          suspect_threshold_spike = 40
          fail_threshold_spike = 50
          
          # flat_test (forced to pass, values have to be checked)
          tolerance = 0
          suspect_threshold_flat = 2
          fail_threshold_flat = 3


      qc_config = {
          "qartod": 
              {
              "gross_range_test": {"fail_span": fail_span, "suspect_span": suspect_span},

              "flat_line_test": {"tolerance": tolerance, "suspect_threshold": suspect_threshold_flat , "fail_threshold": fail_threshold_flat},

              "spike_test": {"suspect_threshold": suspect_threshold_spike, "fail_threshold": fail_threshold_spike},

             # "climatology_test": {},

              #"attenuated_signal_test": {},

              #"density_inversion_test": {},

              #"location_test": {},

              #"rate_of_change_test": {}

          }
      }

      
      if var == 'wvdir':
          fail_span = [0, 360]
          suspect_span = [0, 360]


          qc_config = {
              "qartod": 
                  {
                  "gross_range_test": {"fail_span": fail_span, "suspect_span": suspect_span},
              }
          }
      
      
      inp_in=ds[var]
      tinp_in=ds['date_time']
      zinp_in=ds[var]*0
      
      flags_dict[var] = apply_qc(inp_in, tinp_in, zinp_in, qc_config)
      
      ## Flag  grouping: if scores the same for all tests final flag is mantained, otherwise is labelled as bad data (e.g. 111 = 1, 999=9, 141 = 4)
      # 0 flag won't be applicable
      pd_flags[var] = pd.DataFrame(flags_dict[var]['qartod'])

      if var is not 'wvdir':
          aux = pd_flags[var].apply(lambda x: x.gross_range_test == x.flat_line_test == x.spike_test, axis = 1)
          pd_flags[var]['final_flags'] = 4
          for ind in np.where(aux==True)[0]:
              pd_flags[var]['final_flags'][ind] = int(pd_flags[var].gross_range_test[ind])
      
      else:
          pd_flags[var]['final_flags']=pd_flags[var].gross_range_test
        
  # New df with flags
  df = pd.DataFrame()

  df['obsv_id'] = ds.id
  df['pnboia_id'] = ds.buoy_id
  df['datetime'] = ds.date_time

  df['wvht'] = ds.wvht
  df['wvht_flag_pnboia'] = ds.flag_swvht1
  df['wvht_flag_qartod'] = pd_flags['wvht']['final_flags']

  df['tp'] = ds.tp
  df['tp_flag_pnboia'] = ds.flag_tp1
  df['tp_flag_qartod'] = pd_flags['tp']['final_flags']

  df['wvdir'] = ds.wvdir
  df['wvdir_flag_pnboia'] = ds.flag_wvdir1
  df['wvdir_flag_qartod'] = pd_flags['wvdir']['final_flags']

  df = df.set_index('obsv_id')

  df.to_csv(b+'_qc.csv', index=True)



