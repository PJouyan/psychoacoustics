def sines(f, phi=0, l=3, sr=44100, options=0, normalize=True, nround=10):
    '''
    f: integer or float: signal's frequency
       [[frequencies_1], [amplitudes_1], ...] (could also consist of one element)
    phi: 0: no phase difference
         [phases in radians]
    l: signal's length in seconds
    sr: signal's sampling rate
    options: 0: hearing the components simultaneously
             1: hearing the components individually and successively
    normalize: whether or not to normalize the signal to 1
    nround: number of decimal places for rounding the samples
    '''
    import numpy as np
    
    t = np.around(np.arange(int(l*sr))/sr, nround)
    
    if (type(f)==int or type(f)==float or type(f)==np.float64):
        return np.around(np.sin(2*np.pi*f*t + phi), nround)
    
    n = len(f[0])
    
    if not phi:
        phi = [0]*n
        
    if options==0:
        s = np.zeros(int(sr*l))
        for i in range(n):
            s += f[1][i]*sines(f=f[0][i], phi=phi[i], l=l, sr=sr, options=0, normalize=normalize, nround=nround)
        if normalize:
            return np.around(s/np.max(np.abs(s)), nround)
        else:
            return np.around(s, nround)
    
    elif options==1:
        s = np.zeros(int(sr*l*n))
        for i in range(n):
            seg = f[1][i]*sines(f=f[0][i], phi=phi[i], l=l, sr=sr, options=0, normalize=normalize, nround=nround)
            for j in range(int(sr*l)):
                s[int(i*sr*l)+j] = seg[j]
        if normalize:
            return np.around(s/np.max(np.abs(s)), nround)
        else:
            return np.around(s, nround)



def noise(f, l=3, sr=44100, normalize=True, nround=10):
    '''
    f: [f_low, f_high];
       [[f_low_1, f_high_1], ...] (could also consist of one element)
    '''
    import numpy as np
    import scipy.signal as signal
    
    white_noise = np.random.normal(0, 1, int(l*sr))
    white_noise /= np.max(np.abs(white_noise))
    
    nyquist = sr/2
    
    if type(f[0])!=list:
        
        f_low, f_high = f
        b, a = signal.butter(4, [f_low/nyquist, f_high/nyquist], btype='band')  # 4th-order Butterworth band-pass filter
        filtered_noise = signal.filtfilt(b, a, white_noise)
        
        if normalize:
            return np.around(filtered_noise/np.max(np.abs(filtered_noise)), nround)
        else:
            return np.around(filtered_noise, nround)
    
    else:
        
        filtered_noise = np.zeros(int(l*sr))
        
        for i in range(len(f)):
            filtered_noise += noise(f=f[i], l=l, sr=sr, normalize=normalize, nround=nround)  # normalization... ?
        
        if normalize:
            return np.around(filtered_noise/np.max(np.abs(filtered_noise)), nround)
        else:
            return np.around(filtered_noise, nround)



def read(name, dtype=0, normalize=False, nround=10):
    '''
    name: str; complete file name or path to file (only .wav)
    dtype: 0: keep the original data type
           numpy data types (np.float64, np.int64, etc)
    '''
    from scipy.io import wavfile
    import numpy as np
    
    sr, s = wavfile.read(name)
    
    if dtype!=0:
        s = np.array(s, dtype=dtype)
    
    if normalize:
        s = np.array(s, dtype='float64')
        s /= np.max(np.abs(s))
        s = np.around(s, nround)
    
    return s, sr



def play(*args, sr=44100, ap=True):
    '''
    *args: mono or stereo signals (to make a stereo signal use 'np.column_stack((s_left, s_right))')
    ap: autoplay
    '''
    import numpy as np
    import sounddevice as sd
    
    for arg in args:
        arg = np.array(arg)
        if ap==True:
            sd.play(arg, sr)
            sd.wait()
        else:
            ifplay = input('To play, enter "p":')
            if ifplay=='p':
                sd.play(arg, sr)
                sd.wait()
            else:
                return  # to improve...
    
    return



def adjust(s, l=[0.02]*2, sr=44100, r=1, nround=10):
    '''
    s: signal
    l: [l_beg, l_end]; lengths from the signal's beginning and end to be adjusted according to x^r
    r: >= 1
    '''
    import numpy as np
    
    s = np.array(s)
    
    ratios = np.array(list(np.linspace(0, 1, int(l[0]*sr))**r) + 
                      [1]*(len(s)-int(sum(l)*sr)) + 
                      list(np.linspace(0, 1, int(l[1]*sr))**r)[::-1])
    
    s *= ratios
    
    return np.around(s, nround)



def norm(s, factor=1, nround=10):
    '''
    factor: normalization factor
    '''
    import numpy as np
    
    s = np.array(s, dtype='float64')
    
    max_value = np.max(np.abs(s))
    s /= max_value/factor
    
    return np.around(s, nround)



def adjust_amp(s, ddb, nround=10):
    '''
    ddb: decibel change
    '''
    import numpy as np
    
    s = np.array(s)
    
    amp_factor = 10 ** (ddb / 20)
    s *= amp_factor
    
    max_value = np.max(np.abs(s))
    if max_value > 1.0:
        print('Warning: Exceeding the maximum amplitude (1.0).')
    
    return np.around(s, nround)



def intensity(s, nround=10):
    '''
    Calculate RMS intensity of signal
    '''
    import numpy as np
    
    s = np.array(s)
    
    rms_intensity = np.sqrt(np.mean(s**2))
    
    return np.around(rms_intensity, nround)