import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm

k1 = np.__version__
k2 = pd.__version__
k3= matplotlib.__version__
k4= sm.__version__

print(f"numpy sürümü: {k1}, pandas sürümü: {k2}, matplotlib sürümü: {k3}, statmodels sürümü: {k4}")