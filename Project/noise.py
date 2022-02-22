import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.utils import shuffle
import extract_features

from scipy.io import savemat
infile = open('brain_singals_df.pkl','rb')
raw_data = pickle.load(infile)
infile.close()
#print(raw_data)

#Signal Analysis for one single data
def signal_analysis():
    inp= np.array(raw_data.iloc[0,2:482])
    
    t = np.linspace(1,480,480)
    
    plt.plot(t, inp)
    plt.title('Signal')
    plt.ylabel('Voltage (V)')
    plt.xlabel('Time (s)')
    plt.show()
    
    xWatts = inp ** 2
    
    
    
    # Set a target SNR
    targetSNRdb = 20
    
    signalAverageInWatts = np.mean(xWatts)
    signalAvgdB = 10 * np.log10(signalAverageInWatts)

    noise_avg_db = signalAvgdB - targetSNRdb
    noiseAvgWatts = 10 ** (noise_avg_db / 10)
    # Generate a sample of white noise
    mean_noise = 0
    noiseVolts = np.random.normal(mean_noise, np.sqrt(noiseAvgWatts), len(xWatts))

    yVolts = inp + noiseVolts
    
    # Plot signal with noise
    plt.plot(t, yVolts)
    plt.title('Signal with noise')
    plt.ylabel('Voltage (V)')
    plt.xlabel('Time (s)')
    plt.show()

signal_analysis()


originalData= np.array(raw_data.iloc[:,2:482])
commonData = raw_data.loc[:,'People':'Class']
noise = np.random.normal(0, .1, originalData.shape)
newSignal = originalData + noise
print(newSignal.shape)


df_noise_gen = pd.DataFrame(newSignal)
commonData.reset_index(drop=True, inplace=True)
df_noise_gen.reset_index(drop=True, inplace=True)
final_df = pd.concat([commonData,df_noise_gen],axis = 1)
final_df = shuffle(final_df)

noisFeatureDataFrame = extract_features.extract(final_df)
noisFeatureDataFrame.dropna()

temp = noisFeatureDataFrame.loc[:,'Hurst':'PFD']
print(temp.shape)
temp = temp.to_numpy()
fake_data = {'data':''}
print(temp)
y_test = noisFeatureDataFrame['Class']
fake_data['data'] = temp
print(fake_data)
savemat("fake_signal_1.mat", fake_data)