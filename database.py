import os
import pandas as pd

DATA_FILE = os.path.join(os.path.dirname(__file__), "tour_stats.csv")

def load_data():
    
    
    df = pd.read_csv(DATA_FILE)
    return df


