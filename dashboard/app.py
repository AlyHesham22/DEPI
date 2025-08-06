# Import necessary libraries for data manipulation, visualization, and dashboard creation
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

# ================================================================================================
# DATA LOADING AND PREPROCESSING FUNCTIONS
# ================================================================================================

def load_and_clean_data(file_path):
    """
    Load the medical appointments dataset and perform initial data cleaning.
    
    Args:
        file_path (str): Path to the CSV file containing the medical appointments data
    
    Returns:
        pandas.DataFrame: Cleaned and preprocessed dataset
    """
    # Load the dataset from CSV file
    df = pd.read_csv(file_path)
    
    # Display basic information about the dataset
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Convert date columns from string to datetime format for better manipulation
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    
    # Create new features for analysis
    # Calculate the number of days between scheduling and appointment
    df['DaysWaiting'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
    
    # Extract day of week from appointment date (0=Monday, 6=Sunday)
    df['DayOfWeek'] = df['AppointmentDay'].dt.dayofweek
    
    # Map day numbers to day names for better visualization
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['DayOfWeekName'] = df['DayOfWeek'].map(day_names)
    
    # Create age groups for better analysis
    # Define age bins: 0-17 (Children), 18-35 (Young Adults), 36-55 (Middle-aged), 56+ (Seniors)
    age_bins = [0, 18, 36, 56, 120]
    age_labels = ['Children (0-17)', 'Young Adults (18-35)', 'Middle-aged (36-55)', 'Seniors (56+)']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
    
    # Convert 'No-show' column to binary (1 for No-show, 0 for Show)
    df['NoShow_Binary'] = (df['No-show'] == 'Yes').astype(int)
    
    # Clean neighborhood names by removing extra spaces and standardizing format
    df['Neighbourhood'] = df['Neighbourhood'].str.strip().str.title()
    
    # Handle any missing values
    df = df.dropna()
    
    # Remove any rows with negative waiting days (data quality issue)
    df = df[df['DaysWaiting'] >= 0]
    
    # Remove any rows with unrealistic ages
    df = df[(df['Age'] >= 0) & (df['Age'] <= 120)]
    
    return df

def calculate_summary_statistics(df):
    """
    Calculate key summary statistics for the dashboard.
    
    Args:
        df (pandas.DataFrame): The cleaned dataset
    
    Returns:
        dict: Dictionary containing summary statistics
    """
    total_appointments = len(df)
    no_shows = df['NoShow_Binary'].sum()
    show_rate = ((total_appointments - no_shows) / total_appointments) * 100
    no_show_rate = (no_shows / total_appointments) * 100
    
    avg_age = df['Age'].mean()
    avg_waiting_days = df['DaysWaiting'].mean()
    
    # Gender distribution
    gender_counts = df['Gender'].value_counts()
    
    # Medical conditions prevalence
    conditions = ['Hipertension', 'Diabetes', 'Alcoholism']
    condition_stats = {}
    for condition in conditions:
        condition_stats[condition] = (df[condition].sum() / len(df)) * 100
    
    return {
        'total_appointments': total_appointments,
        'show_rate': show_rate,
        'no_show_rate': no_show_rate,
        'avg_age': avg_age,
        'avg_waiting_days': avg_waiting_days,
        'gender_counts': gender_counts,
        'condition_stats': condition_stats
    }

# ================================================================================================
# VISUALIZATION FUNCTIONS
# ================================================================================================

def create_no_show_overview_chart(df):
    """
    Create a pie chart showing the overall no-show vs show-up rates.
    
    Args:
        df (pandas.DataFrame): The dataset
    
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    # Calculate counts for show and no-show
    show_counts = df['No-show'].value_counts()
    
    # Create pie chart with custom colors
    fig = px.pie(
        values=show_counts.values,
        names=['Showed Up', 'No Show'],  # Rename for clarity
        title="Overall Appointment Attendance Rate",
        color_discrete_sequence=['#2E8B57', '#DC143C']  # Green for show, Red for no-show
    )
    
    # Update layout for better appearance
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font=dict(size=14),
        title_font=dict(size=18, family="Arial Black"),
        showlegend=True
    )
    
    return fig

def create_age_gender_analysis(df):
    """
    Create a grouped bar chart showing no-show rates by age group and gender.
    
    Args:
        df (pandas.DataFrame): The dataset
    
    Returns:
        plotly.graph_objects.Figure: Grouped bar chart figure
    """
    # Calculate no-show rates by age group and gender
    age_gender_stats = df.groupby(['AgeGroup', 'Gender'])['NoShow_Binary'].agg(['count', 'sum']).reset_index()
    age_gender_stats['NoShowRate'] = (age_gender_stats['sum'] / age_gender_stats['count']) * 100
    
    # Create grouped bar chart
    fig = px.bar(
        age_gender_stats,
        x='AgeGroup',
        y='NoShowRate',
        color='Gender',
        title='No-Show Rate by Age Group and Gender',
        labels={'NoShowRate': 'No-Show Rate (%)', 'AgeGroup': 'Age Group'},
        color_discrete_sequence=['#FF6B6B', '#4ECDC4']
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="No-Show Rate (%)",
        font=dict(size=12),
        title_font=dict(size=16, family="Arial Black"),
        legend=dict(title="Gender")
    )
    
    return fig

def create_day_of_week_analysis(df):
    """
    Create a bar chart showing appointment distribution and no-show rates by day of week.
    
    Args:
        df (pandas.DataFrame): The dataset
    
    Returns:
        plotly.graph_objects.Figure: Bar chart with secondary y-axis
    """
    # Calculate statistics by day of week
    day_stats = df.groupby('DayOfWeekName').agg({
        'AppointmentID': 'count',
        'NoShow_Binary': ['sum', 'mean']
    }).reset_index()
    
    # Flatten column names
    day_stats.columns = ['DayOfWeek', 'TotalAppointments', 'NoShows', 'NoShowRate']
    day_stats['NoShowRate'] = day_stats['NoShowRate'] * 100
    
    # Define the order of days for proper display
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_stats['DayOfWeek'] = pd.Categorical(day_stats['DayOfWeek'], categories=day_order, ordered=True)
    day_stats = day_stats.sort_values('DayOfWeek')
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bar chart for total appointments
    fig.add_trace(
        go.Bar(x=day_stats['DayOfWeek'], y=day_stats['TotalAppointments'],
               name='Total Appointments', marker_color='lightblue'),
        secondary_y=False,
    )
    
    # Add line chart for no-show rate
    fig.add_trace(
        go.Scatter(x=day_stats['DayOfWeek'], y=day_stats['NoShowRate'],
                   mode='lines+markers', name='No-Show Rate (%)',
                   line=dict(color='red', width=3), marker=dict(size=8)),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_xaxes(title_text="Day of Week")
    fig.update_yaxes(title_text="Number of Appointments", secondary_y=False)
    fig.update_yaxes(title_text="No-Show Rate (%)", secondary_y=True)
    fig.update_layout(title_text="Appointments and No-Show Rates by Day of Week")
    
    return fig

def create_waiting_time_analysis(df):
    """
    Create a histogram showing the relationship between waiting time and no-show rate.
    
    Args:
        df (pandas.DataFrame): The dataset
    
    Returns:
        plotly.graph_objects.Figure: Histogram figure
    """
    # Filter out extreme waiting times for better visualization (keep 95% of data)
    waiting_time_95th = df['DaysWaiting'].quantile(0.95)
    df_filtered = df[df['DaysWaiting'] <= waiting_time_95th]
    
    # Create histogram with different colors for show vs no-show
    fig = px.histogram(
        df_filtered,
        x='DaysWaiting',
        color='No-show',
        title='Distribution of Waiting Time by Attendance',
        labels={'DaysWaiting': 'Days Between Scheduling and Appointment', 'count': 'Number of Appointments'},
        nbins=30,
        color_discrete_sequence=['#2E8B57', '#DC143C']
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Days Waiting",
        yaxis_title="Number of Appointments",
        font=dict(size=12),
        title_font=dict(size=16, family="Arial Black"),
        bargap=0.1
    )
    
    return fig

def create_medical_conditions_analysis(df):
    """
    Create a grouped bar chart showing no-show rates for different medical conditions.
    
    Args:
        df (pandas.DataFrame): The dataset
    
    Returns:
        plotly.graph_objects.Figure: Grouped bar chart figure
    """
    # List of medical conditions to analyze
    conditions = ['Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']
    
    condition_stats = []
    
    # Calculate no-show rates for each condition
    for condition in conditions:
        # Patients with the condition
        with_condition = df[df[condition] == 1]['NoShow_Binary'].mean() * 100
        # Patients without the condition
        without_condition = df[df[condition] == 0]['NoShow_Binary'].mean() * 100
        
        condition_stats.extend([
            {'Condition': condition, 'Group': 'With Condition', 'NoShowRate': with_condition},
            {'Condition': condition, 'Group': 'Without Condition', 'NoShowRate': without_condition}
        ])
    
    condition_df = pd.DataFrame(condition_stats)
    
    # Create grouped bar chart
    fig = px.bar(
        condition_df,
        x='Condition',
        y='NoShowRate',
        color='Group',
        title='No-Show Rates by Medical Conditions',
        labels={'NoShowRate': 'No-Show Rate (%)', 'Condition': 'Medical Condition'},
        color_discrete_sequence=['#FF6B6B', '#4ECDC4'],
        barmode='group'
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Medical Condition",
        yaxis_title="No-Show Rate (%)",
        font=dict(size=12),
        title_font=dict(size=16, family="Arial Black"),
        legend=dict(title="Patient Group")
    )
    
    return fig

def create_neighborhood_analysis(df, top_n=15):
    """
    Create a bar chart showing no-show rates for top neighborhoods by appointment volume.
    
    Args:
        df (pandas.DataFrame): The dataset
        top_n (int): Number of top neighborhoods to display
    
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Calculate statistics by neighborhood
    neighborhood_stats = df.groupby('Neighbourhood').agg({
        'AppointmentID': 'count',
        'NoShow_Binary': 'mean'
    }).reset_index()
    
    neighborhood_stats.columns = ['Neighbourhood', 'TotalAppointments', 'NoShowRate']
    neighborhood_stats['NoShowRate'] = neighborhood_stats['NoShowRate'] * 100
    
    # Get top neighborhoods by appointment volume
    top_neighborhoods = neighborhood_stats.nlargest(top_n, 'TotalAppointments')
    
    # Create bar chart
    fig = px.bar(
        top_neighborhoods,
        x='NoShowRate',
        y='Neighbourhood',
        orientation='h',
        title=f'No-Show Rates in Top {top_n} Neighborhoods (by appointment volume)',
        labels={'NoShowRate': 'No-Show Rate (%)', 'Neighbourhood': 'Neighborhood'},
        color='NoShowRate',
        color_continuous_scale='RdYlBu_r'
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="No-Show Rate (%)",
        yaxis_title="Neighborhood",
        font=dict(size=10),
        title_font=dict(size=14, family="Arial Black"),
        height=600
    )
    
    return fig

def create_sms_scholarship_analysis(df):
    """
    Create a 2x2 subplot showing the impact of SMS and Scholarship on no-show rates.
    
    Args:
        df (pandas.DataFrame): The dataset
    
    Returns:
        plotly.graph_objects.Figure: Subplot figure
    """
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('SMS Impact on No-Show Rate', 'Scholarship Impact on No-Show Rate'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # SMS analysis
    sms_stats = df.groupby('SMS_received')['NoShow_Binary'].mean() * 100
    fig.add_trace(
        go.Bar(x=['No SMS', 'SMS Received'], y=sms_stats.values,
               name='SMS Impact', marker_color=['#FF6B6B', '#4ECDC4']),
        row=1, col=1
    )
    
    # Scholarship analysis
    scholarship_stats = df.groupby('Scholarship')['NoShow_Binary'].mean() * 100
    fig.add_trace(
        go.Bar(x=['No Scholarship', 'Has Scholarship'], y=scholarship_stats.values,
               name='Scholarship Impact', marker_color=['#FFD93D', '#6BCF7F']),
        row=1, col=2
    )
    
    # Update layout
    fig.update_xaxes(title_text="SMS Status", row=1, col=1)
    fig.update_xaxes(title_text="Scholarship Status", row=1, col=2)
    fig.update_yaxes(title_text="No-Show Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="No-Show Rate (%)", row=1, col=2)
    
    fig.update_layout(
        title_text="Impact of SMS and Scholarship on No-Show Rates",
        showlegend=False,
        font=dict(size=12),
        title_font=dict(size=16, family="Arial Black")
    )
    
    return fig

# ================================================================================================
# DASHBOARD LAYOUT AND STYLING
# ================================================================================================

# Load and preprocess the data
print("Loading and preprocessing data...")
df = load_and_clean_data('medical_appointments.csv')
stats = calculate_summary_statistics(df)
print("Data preprocessing completed!")

# Initialize the Dash application with Bootstrap theme for better styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the application title
app.title = "Medical Appointments Dashboard"

# Create the main layout of the dashboard
app.layout = dbc.Container([
    # Header section with title and description
    dbc.Row([
        dbc.Col([
            html.H1("🏥 Medical Appointments Dashboard", 
                   className="text-center mb-4",
                   style={'color': '#2E8B57', 'fontWeight': 'bold'}),
            html.P("Interactive analysis of medical appointment no-show patterns in Brazil",
                   className="text-center lead mb-4",
                   style={'color': '#666666'})
        ])
    ]),
    
    # Key statistics cards section
    dbc.Row([
        # Total appointments card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{stats['total_appointments']:,}", className="card-title text-primary"),
                    html.P("Total Appointments", className="card-text")
                ])
            ], className="mb-3")
        ], width=3),
        
        # Show rate card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{stats['show_rate']:.1f}%", className="card-title text-success"),
                    html.P("Show-up Rate", className="card-text")
                ])
            ], className="mb-3")
        ], width=3),
        
        # Average age card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{stats['avg_age']:.0f} years", className="card-title text-info"),
                    html.P("Average Patient Age", className="card-text")
                ])
            ], className="mb-3")
        ], width=3),
        
        # Average waiting days card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{stats['avg_waiting_days']:.0f} days", className="card-title text-warning"),
                    html.P("Average Waiting Time", className="card-text")
                ])
            ], className="mb-3")
        ], width=3)
    ], className="mb-4"),
    
    # Interactive filters section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Interactive Filters"),
                dbc.CardBody([
                    dbc.Row([
                        # Age group filter
                        dbc.Col([
                            html.Label("Age Group:", className="form-label"),
                            dcc.Dropdown(
                                id='age-group-filter',
                                options=[
                                    {'label': 'All Age Groups', 'value': 'all'},
                                    {'label': 'Children (0-17)', 'value': 'Children (0-17)'},
                                    {'label': 'Young Adults (18-35)', 'value': 'Young Adults (18-35)'},
                                    {'label': 'Middle-aged (36-55)', 'value': 'Middle-aged (36-55)'},
                                    {'label': 'Seniors (56+)', 'value': 'Seniors (56+)'}
                                ],
                                value='all',
                                className="mb-2"
                            )
                        ], width=4),
                        
                        # Gender filter
                        dbc.Col([
                            html.Label("Gender:", className="form-label"),
                            dcc.Dropdown(
                                id='gender-filter',
                                options=[
                                    {'label': 'All Genders', 'value': 'all'},
                                    {'label': 'Female', 'value': 'F'},
                                    {'label': 'Male', 'value': 'M'}
                                ],
                                value='all',
                                className="mb-2"
                            )
                        ], width=4),
                        
                        # Waiting days slider
                        dbc.Col([
                            html.Label("Maximum Waiting Days:", className="form-label"),
                            dcc.Slider(
                                id='waiting-days-slider',
                                min=0,
                                max=int(df['DaysWaiting'].quantile(0.95)),
                                step=1,
                                value=int(df['DaysWaiting'].quantile(0.95)),
                                marks={
                                    0: '0',
                                    7: '1 week',
                                    30: '1 month',
                                    int(df['DaysWaiting'].quantile(0.95)): f"{int(df['DaysWaiting'].quantile(0.95))} days"
                                },
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ], width=4)
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Main visualizations section
    dbc.Row([
        # Overall no-show rate pie chart
        dbc.Col([
            dcc.Graph(
                id='no-show-overview',
                figure=create_no_show_overview_chart(df)
            )
        ], width=6),
        
        # Age and gender analysis
        dbc.Col([
            dcc.Graph(
                id='age-gender-analysis',
                figure=create_age_gender_analysis(df)
            )
        ], width=6)
    ], className="mb-4"),
    
    # Day of week and waiting time analysis
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='day-of-week-analysis',
                figure=create_day_of_week_analysis(df)
            )
        ], width=12)
    ], className="mb-4"),
    
    # Waiting time distribution
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='waiting-time-analysis',
                figure=create_waiting_time_analysis(df)
            )
        ], width=12)
    ], className="mb-4"),
    
    # Medical conditions and SMS/Scholarship analysis
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='medical-conditions-analysis',
                figure=create_medical_conditions_analysis(df)
            )
        ], width=6),
        
        dbc.Col([
            dcc.Graph(
                id='sms-scholarship-analysis',
                figure=create_sms_scholarship_analysis(df)
            )
        ], width=6)
    ], className="mb-4"),
    
    # Neighborhood analysis
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='neighborhood-analysis',
                figure=create_neighborhood_analysis(df)
            )
        ], width=12)
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("📊 Dashboard created with Dash and Plotly | Data source: Kaggle Medical Appointments No-Show Dataset",
                   className="text-center text-muted small")
        ])
    ])
], fluid=True)

# ================================================================================================
# INTERACTIVE CALLBACKS
# ================================================================================================

@app.callback(
    [Output('no-show-overview', 'figure'),
     Output('age-gender-analysis', 'figure'),
     Output('waiting-time-analysis', 'figure'),
     Output('medical-conditions-analysis', 'figure')],
    [Input('age-group-filter', 'value'),
     Input('gender-filter', 'value'),
     Input('waiting-days-slider', 'value')]
)
def update_charts(age_group, gender, max_waiting_days):
    """
    Update charts based on filter selections.
    This callback function responds to changes in the filter controls and updates
    the visualizations accordingly.
    
    Args:
        age_group (str): Selected age group filter value
        gender (str): Selected gender filter value
        max_waiting_days (int): Maximum waiting days from slider
    
    Returns:
        tuple: Updated figures for the charts
    """
    # Start with the full dataset
    filtered_df = df.copy()
    
    # Apply age group filter
    if age_group != 'all':
        filtered_df = filtered_df[filtered_df['AgeGroup'] == age_group]
    
    # Apply gender filter
    if gender != 'all':
        filtered_df = filtered_df[filtered_df['Gender'] == gender]
    
    # Apply waiting days filter
    filtered_df = filtered_df[filtered_df['DaysWaiting'] <= max_waiting_days]
    
    # Update charts with filtered data
    no_show_fig = create_no_show_overview_chart(filtered_df)
    age_gender_fig = create_age_gender_analysis(filtered_df)
    waiting_time_fig = create_waiting_time_analysis(filtered_df)
    medical_conditions_fig = create_medical_conditions_analysis(filtered_df)
    
    return no_show_fig, age_gender_fig, waiting_time_fig, medical_conditions_fig

# ================================================================================================
# APPLICATION ENTRY POINT
# ================================================================================================

if __name__ == '__main__':
    """
    Run the Dash application.
    The application will start a local web server and open the dashboard in a browser.
    
    Parameters:
    - debug=True: Enables debug mode for development (auto-reloads on code changes)
    - host='0.0.0.0': Makes the app accessible from any IP address
    - port=8050: Port number for the web server
    """
    print("Starting the Medical Appointments Dashboard...")
    print("The dashboard will be available at: http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)