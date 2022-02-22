import pyeeg
import pickle
import numpy as np
from scipy.stats import skew, kurtosis
import pywt

##ADD FEATURE EXTRACTION FUNCTIONS HERE

def petrosian_fractal_dimensions(line):
    pet_fract_dist = pyeeg.pfd(line)
    return pet_fract_dist

def hurst(line):
    hrst = pyeeg.hurst(line)
    return hrst

def fft_beta(line):
    sampling_rate = 160
    fft_val = np.absolute(np.fft.rfft(line))
    fft_freq = np.fft.rfftfreq(len(line), 1.0/sampling_rate)
    eeg_bands = {'Beta': (13, 30)}
    freq_ix = np.where((fft_freq >= eeg_bands['Beta'][0]) & (fft_freq <= eeg_bands['Beta'][1]))[0]
    beta_val= np.mean(fft_val[freq_ix])
    return beta_val

def zero_crossing(line):
        dat_grad = np.concatenate([[0], np.diff(-line)])
        signednp_g = np.sign(dat_grad[0:-1]*dat_grad[1:])
        dots = np.where(signednp_g<0)[0]
        if len(dots) > 0:
            pointofcross = max(dat_grad[dots + 1] - dat_grad[dots])
        else:
            pointofcross = 0
        newdat = (np.sum(np.abs(np.sign(dat_grad[1:])-np.sign(dat_grad[:-1])))) / (2*len(dat_grad))
        return (pointofcross ,newdat)

def discrete_Wavelet_Transform(line):
    (VAL1, VAL2) = pywt.dwt(line, 'bior3.5')
    return (np.var(VAL2) , skew(VAL2) , kurtosis(VAL2))
    
brainData = open("brain_singals_df.pkl","rb")
dataFrameData = pickle.load(brainData)
brainData.close()
features = dataFrameData.iloc[:,:2]
data = dataFrameData.iloc[:,2:]

## EXTRACT FEATURES INTO THE FOLLOWING DATAFRAME
features["Hurst"] = data.apply(lambda line: hurst(line), axis = 1)
features[['crossing','rate']]= data.apply(lambda line: zero_crossing(line), axis = 1, result_type = 'expand')
features['FFT_beta']= data.apply(lambda line: fft_beta(line), axis = 1)
features[['VAR', 'SKEW', 'KURTOSIS']]= data.apply(lambda line: discrete_Wavelet_Transform(line), axis = 1, result_type = 'expand')
features["PFD"] = data.apply(lambda line: petrosian_fractal_dimensions(line), axis = 1)

print(features)
with open("features_dataFrame.pkl", "wb") as file:
    pickle.dump(features, file)

def extract(data):
    features = data.iloc[:,:2]
    features["Hurst"] = data.apply(lambda line: hurst(line), axis = 1)
    features[['crossing','rate']]= data.apply(lambda line: zero_crossing(line), axis = 1, result_type = 'expand')
    features['FFT_beta']= data.apply(lambda line: fft_beta(line), axis = 1)
    features[['VAR', 'SKEW', 'KURTOSIS']]= data.apply(lambda line: discrete_Wavelet_Transform(line), axis = 1, result_type = 'expand')
    features["PFD"] = data.apply(lambda line: petrosian_fractal_dimensions(line), axis = 1)
    return features
