#!/usr/bin/env python3
"""
Demo script to showcase key insights from the Medical Appointments dataset.
This script runs a quick analysis and displays interesting findings.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_medical_appointments():
    """
    Perform quick analysis of the medical appointments dataset and display key insights.
    """
    print("🏥 Medical Appointments Dashboard - Key Insights Demo")
    print("=" * 60)
    
    # Load the dataset
    print("📊 Loading dataset...")
    df = pd.read_csv('medical_appointments.csv')
    
    # Basic preprocessing
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    df['DaysWaiting'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
    df['NoShow_Binary'] = (df['No-show'] == 'Yes').astype(int)
    
    # Dataset overview
    print(f"\n📈 Dataset Overview:")
    print(f"   • Total appointments: {len(df):,}")
    print(f"   • Date range: {df['AppointmentDay'].min().strftime('%Y-%m-%d')} to {df['AppointmentDay'].max().strftime('%Y-%m-%d')}")
    print(f"   • Unique patients: {df['PatientId'].nunique():,}")
    print(f"   • Unique neighborhoods: {df['Neighbourhood'].nunique()}")
    
    # Key statistics
    no_show_rate = (df['NoShow_Binary'].sum() / len(df)) * 100
    show_rate = 100 - no_show_rate
    avg_age = df['Age'].mean()
    avg_waiting = df['DaysWaiting'].mean()
    
    print(f"\n🎯 Key Statistics:")
    print(f"   • Show-up rate: {show_rate:.1f}%")
    print(f"   • No-show rate: {no_show_rate:.1f}%")
    print(f"   • Average patient age: {avg_age:.1f} years")
    print(f"   • Average waiting time: {avg_waiting:.1f} days")
    
    # Gender analysis
    gender_stats = df.groupby('Gender')['NoShow_Binary'].agg(['count', 'mean']).round(3)
    print(f"\n👥 Gender Analysis:")
    for gender in ['F', 'M']:
        if gender in gender_stats.index:
            count = gender_stats.loc[gender, 'count']
            rate = gender_stats.loc[gender, 'mean'] * 100
            gender_name = 'Female' if gender == 'F' else 'Male'
            print(f"   • {gender_name}: {count:,} appointments, {rate:.1f}% no-show rate")
    
    # Age group analysis
    age_bins = [0, 18, 36, 56, 120]
    age_labels = ['Children (0-17)', 'Young Adults (18-35)', 'Middle-aged (36-55)', 'Seniors (56+)']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
    
    age_stats = df.groupby('AgeGroup')['NoShow_Binary'].agg(['count', 'mean']).round(3)
    print(f"\n🎂 Age Group Analysis:")
    for age_group in age_labels:
        if age_group in age_stats.index:
            count = age_stats.loc[age_group, 'count']
            rate = age_stats.loc[age_group, 'mean'] * 100
            print(f"   • {age_group}: {count:,} appointments, {rate:.1f}% no-show rate")
    
    # Medical conditions impact
    conditions = ['Hipertension', 'Diabetes', 'Alcoholism']
    print(f"\n🏥 Medical Conditions Impact:")
    for condition in conditions:
        with_condition = df[df[condition] == 1]['NoShow_Binary'].mean() * 100
        without_condition = df[df[condition] == 0]['NoShow_Binary'].mean() * 100
        total_with = df[condition].sum()
        print(f"   • {condition}:")
        print(f"     - With condition: {with_condition:.1f}% no-show ({total_with:,} patients)")
        print(f"     - Without condition: {without_condition:.1f}% no-show")
    
    # SMS and Scholarship impact
    sms_impact = df.groupby('SMS_received')['NoShow_Binary'].mean() * 100
    scholarship_impact = df.groupby('Scholarship')['NoShow_Binary'].mean() * 100
    
    print(f"\n📱 SMS and Support Impact:")
    print(f"   • SMS Reminder:")
    print(f"     - No SMS: {sms_impact[0]:.1f}% no-show")
    print(f"     - With SMS: {sms_impact[1]:.1f}% no-show")
    print(f"   • Scholarship (Financial Support):")
    print(f"     - No scholarship: {scholarship_impact[0]:.1f}% no-show")
    print(f"     - With scholarship: {scholarship_impact[1]:.1f}% no-show")
    
    # Waiting time analysis
    same_day = df[df['DaysWaiting'] == 0]
    same_day_no_show = (same_day['NoShow_Binary'].sum() / len(same_day)) * 100
    
    print(f"\n⏰ Waiting Time Insights:")
    print(f"   • Same-day appointments: {len(same_day):,} ({len(same_day)/len(df)*100:.1f}%)")
    print(f"   • Same-day no-show rate: {same_day_no_show:.1f}%")
    print(f"   • Maximum waiting time: {df['DaysWaiting'].max()} days")
    print(f"   • Median waiting time: {df['DaysWaiting'].median()} days")
    
    # Top neighborhoods with highest no-show rates
    neighborhood_stats = df.groupby('Neighbourhood').agg({
        'NoShow_Binary': ['count', 'mean']
    }).round(3)
    neighborhood_stats.columns = ['total_appointments', 'no_show_rate']
    neighborhood_stats = neighborhood_stats[neighborhood_stats['total_appointments'] >= 100]  # Filter for significant volume
    top_no_show_neighborhoods = neighborhood_stats.nlargest(5, 'no_show_rate')
    
    print(f"\n🏘️  Top 5 Neighborhoods with Highest No-Show Rates (min 100 appointments):")
    for i, (neighborhood, stats) in enumerate(top_no_show_neighborhoods.iterrows(), 1):
        print(f"   {i}. {neighborhood}: {stats['no_show_rate']*100:.1f}% ({stats['total_appointments']:.0f} appointments)")
    
    print(f"\n🚀 To explore these insights interactively, run:")
    print(f"   python3 app.py")
    print(f"   Then open: http://localhost:8050")
    print("=" * 60)

if __name__ == "__main__":
    try:
        analyze_medical_appointments()
    except FileNotFoundError:
        print("❌ Error: medical_appointments.csv not found!")
        print("Please ensure the dataset file is in the current directory.")
    except Exception as e:
        print(f"❌ Error: {e}")