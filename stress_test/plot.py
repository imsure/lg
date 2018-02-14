import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os


data = np.loadtxt('response_time.txt', delimiter=' ')
times = data[:, 2]
avg = np.mean(times)
fig = plt.figure()
plt.hist(times, bins=50, color='y')
plt.xlabel('LeadGen Server Response Time (in ms)')
plt.ylabel('# of Hits')
plt.title('2000 API Requests Issued Concurrently from Metropia office\nAverage Response Time: {0:.2f} ms'.format(avg))
fig.savefig('runtime_metropia_office.png')
print('Average runtime:', avg)
