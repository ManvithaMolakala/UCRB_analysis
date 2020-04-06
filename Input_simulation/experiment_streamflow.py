from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import sys
#plt.switch_backend('agg')
#plt.ioff()
#
#design = str(sys.argv[1])

## load paleo data at Cisco
#Paleo = pd.read_csv('../Summary_info/Cisco_Recon_v_Observed_v_Stateline.csv')
#
## re-scale Cisco data to estimate data at CO-UT state line
#factor = np.nanmean(Paleo['ObservedNaturalStateline']/Paleo['ObservedNaturalCisco'])
#Paleo['ScaledNaturalCisco'] = Paleo['ObservedNaturalCisco']*factor
#Paleo['ScaledReconCisco'] = Paleo['ReconCisco']*factor

years = np.arange(1909, 2014)
years_s = np.arange(1950, 2014)

# Load historic data
historic_data = np.load('../Summary_info/historic_flows.npy')

# Load CMIP flows
CMIP3_flows = np.genfromtxt('../Summary_info/CMIP3_flows.csv', delimiter=',')
CMIP3_flows = np.reshape(CMIP3_flows, [112, 64, 12])
CMIP5_flows = np.genfromtxt('../Summary_info/CMIP5_flows.csv', delimiter=',')
CMIP5_flows = np.reshape(CMIP5_flows, [97, 64, 12])

# Load synthetic stationary flows
#baseCase = np.zeros([10, len(years),12])
#for k in range(10):       
#    synthetic_file = open('../' + design + '/Experiment_files/cm2015x_S0_'+str(k+1)+'.xbm', 'r')
#    all_split_data = [x.split('.') for x in synthetic_file.readlines()]
#    yearcount = 0
#    for i in range(16, len(all_split_data)):
#        row_data = []
#        row_data.extend(all_split_data[i][0].split())
#        if row_data[1] == '09163500':
#            data_to_write = [row_data[2]]+all_split_data[i][1:12]
#            baseCase[k,yearcount,:] = [int(j) for j in data_to_write]
#            yearcount+=1 
baseCase = np.load('../Summary_info/stationarysynthetic_flows.npy')

# Load synthetic nonstationary runs
#synthetic_flows = np.zeros([10000, len(years),12])
#for s in range(1000):
#    for k in range(10):       
#        synthetic_file = open('../' + design + '/Experiment_files/cm2015x_S'+str(s+1)+'_'+str(k+1)+'.xbm', 'r')
#        all_split_data = [x.split('.') for x in synthetic_file.readlines()]
#        yearcount = 0
#        for i in range(16, len(all_split_data)):
#            row_data = []
#            row_data.extend(all_split_data[i][0].split())
#            if row_data[1] == '09163500':
#                data_to_write = [row_data[2]]+all_split_data[i][1:12]
#                synthetic_flows[s*10+k,yearcount,:] = [int(j) for j in data_to_write]
#                yearcount+=1
            
#np.save('../Summary_info/'+design+'_flows.npy', synthetic_flows)

synthetic_flows = np.load('../Summary_info/'+design+'_flows.npy')

colors = ['#DD7373', '#305252', '#3C787E','#D0CD94', '#9597a3'][::-1] #'#AA1209'
labels=['Historic', 'Stationary synthetic', 'CMIP3', 'CMIP5', 'This experiment'][::-1] #'Paleo'
data = [historic_data, baseCase, CMIP3_flows, CMIP5_flows, synthetic_flows][::-1] #Paleo['ScaledReconCisco'][:429].values
   
# Figure in imperial units     
fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(111)
for i in range(4):
    ax.fill_between(range(12), np.min(np.min(data[i], axis=0),axis=0),
                    np.max(np.max(data[i], axis=0),axis=0), color=colors[i],
                    label=labels[i],alpha=0.8)
for i in range(4,len(data)):
    ax.fill_between(range(12), np.min(data[i], axis=0),
            np.max(data[i], axis=0), color=colors[i],
            label=labels[i],alpha=0.8)
ax.plot(range(12), historic_data[93,:], color='#AA1209', linewidth = 2, label='Water Year 2002')             
ax.set_yscale("log")               
ax.set_xlabel('Month',fontsize=16)
ax.set_ylabel('Flow at Last Node (af)',fontsize=16)
ax.set_xlim([0,11])
ax.tick_params(axis='both',labelsize=14)
ax.set_xticks(range(12))
ax.set_xticklabels(['O','N','D','J','F','M','A','M','J','J','A','S'])
handles, labels = plt.gca().get_legend_handles_labels()
labels, ids = np.unique(labels, return_index=True)
handles = [handles[i] for i in ids]
fig.subplots_adjust(bottom=0.2)
fig.legend(handles, labels, fontsize=16,loc='lower center',ncol=3)
ax.set_title('Streamflow across experiments',fontsize=18)
fig.savefig('../Summary_info/hydrograph_'+design+'_log.svg')

# Figure in metric units 
data_metric = [x*1233.4818 for x in data]   
fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(111)
for i in range(4):
    ax.fill_between(range(12), np.min(np.min(data_metric[i], axis=0),axis=0),
                    np.max(np.max(data_metric[i], axis=0),axis=0), color=colors[i],
                    label=labels[i],alpha=0.8)
for i in range(4,len(data_metric)):
    ax.fill_between(range(12), np.min(data_metric[i], axis=0),
            np.max(data_metric[i], axis=0), color=colors[i],
            label=labels[i],alpha=0.8)
ax.plot(range(12), historic_data[93,:]*1233.4818, color='#AA1209', linewidth = 2, label='Water Year 2002')             
ax.set_yscale("log")               
ax.set_xlabel('Month',fontsize=16)
ax.set_ylabel('Flow at Last Node ($m^3$)',fontsize=16)
ax.set_xlim([0,11])
ax.tick_params(axis='both',labelsize=14)
ax.set_xticks(range(12))
ax.set_xticklabels(['O','N','D','J','F','M','A','M','J','J','A','S'])
handles, labels = plt.gca().get_legend_handles_labels()
labels, ids = np.unique(labels, return_index=True)
handles = [handles[i] for i in ids]
fig.subplots_adjust(bottom=0.2)
fig.legend(handles, labels, fontsize=16,loc='lower center',ncol=3)
ax.set_title('Streamflow across experiments',fontsize=18)
fig.savefig('../Summary_info/hydrograph_'+design+'_log_metric.svg')