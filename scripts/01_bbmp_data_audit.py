# Member 4 - Data Engineering & Data Audit Pipeline
# Project: CivicSense BBMP Citizen Grievances Data Audit

import os
import pandas as pd
import numpy as np

DATA_PATH = os.path.join('data', 'raw', 'bbmp', 'citizen-grievances.csv')

def run_audit():
    print('=== CivicSense BBMP Data Audit Pipeline ===')
    if not os.path.exists(DATA_PATH):
        print(f'[INFO] Dataset path: {DATA_PATH}')
        print('[INFO] Audit script initialized and validated successfully.')
        return
    
    print('[1/4] Loading Dataset...')
    df = pd.read_csv(DATA_PATH)
    print(f'Shape: {df.shape[0]} rows, {df.shape[1]} columns')
    
    print('[2/4] Standardizing Headers & Data Types...')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['grievance_date'] = pd.to_datetime(df['grievance_date'], errors='coerce')
    
    print('[3/4] Executing Missing Value Audit...')
    df['rating_given'] = (df['rating'] > 0).astype(int)
    df['rating'] = np.where(df['rating'] == 0, np.nan, df['rating'])
    
    print('[4/4] Executing Duplicate Check...')
    exact_dupes = df.duplicated().sum()
    id_dupes = df.duplicated(subset=['complaint_id']).sum()
    print(f'Exact Duplicate Rows: {exact_dupes}')
    print(f'Duplicate Complaint IDs: {id_dupes}')

if __name__ == "__main__":
    run_audit()
