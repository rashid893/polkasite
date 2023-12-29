import numpy as np
from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Supply
from .models import Delegate,DelegateUndelegateStatus,AprSave,WeeklyAprAverage
import bittensor
import pandas as pd
import requests
from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Delegate
from django.db.models import Avg
import subprocess
import os
import time
import re
import math
import time
import subprocess
import re
from datetime import timedelta
from django.utils import timezone

from celery import shared_task

# Example of using the function:
emissions_day = 2952  # example emissions per day
number_of_days_in_year = 365  # days in a year
total_stake_float = 4639675  # example total stake
compounds_per_day = 72  # example compounding periods per day


def calculate_apr_and_apy(emissions_day, number_of_days_in_year, total_stake_float, compounds_per_day):
    """
    Calculate the APR and APY given emissions per day, number of days in a year, total stake, 
    and number of compounding periods per day.

    Parameters:
    emissions_day (float): The amount of emissions per day
    number_of_days_in_year (int): The number of days in a year
    total_stake_float (float): The total stake
    compounds_per_day (int): The number of times the interest is compounded per day

    Returns:
    tuple: APR and APY represented as percentages
    """
    # Calculate APR
    validators_apr = (
        emissions_day * number_of_days_in_year / total_stake_float) * 100

    # Convert APR percentage to decimal
    apr_decimal = validators_apr / 100

    # Total compounding periods per year
    n = compounds_per_day * 365

    # Calculate APY using the formula
    apy_decimal = (1 + apr_decimal / n)**n - 1

    # Convert APY decimal to percentage
    validators_apy = apy_decimal * 100

    return validators_apr, validators_apy


# Example of using the function:
emissions_day = 2952  # example emissions per day
number_of_days_in_year = 365  # days in a year
total_stake_float = 4639675  # example total stake
compounds_per_day = 72  # example compounding periods per day

@shared_task
def fetch_and_save_data():
    # -*- coding: utf-8 -*-
    """Copy of tao_minning_shaukat.ipynb

    Automatically generated by Colaboratory.

    Original file is located at
        https://colab.research.google.com/drive/1jzG6JA2d5UA_iR5O0YnOnU2a546O-aKR
    """

    subtensor = bittensor.subtensor()

    url = "https://raw.githubusercontent.com/opentensor/bittensor-delegates/master/public/delegates.json"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data1 = response.json()

    # Assuming the data variable still holds the JSON
    data_list = []

    for key, value in data1.items():
        data_list.append([key, value['name'], value['url'],
                          value['description'], value['signature']])

    # Convert the list of lists to DataFrame
    columns = ["key", "name", "url", "description", "signature"]
    df = pd.DataFrame(data_list, columns=columns)

    df

    # Excel row Get block number 24
    block = subtensor.get_current_block()
    block

    # # Excel row number 25
    # balances = subtensor.get_balances()
    # # Removing τ and converting values to float row number 25 in excel
    # converted_balances = {k: float(str(v).replace("τ", "").replace(",", "")) for k, v in balances.items()}
    # count = sum(1 for value in converted_balances.values() if value >= 0.1)
    # count

    """# Get List of all validators and information"""

    all_delegates = subtensor.get_delegates()

    """Total stake"""

    total_stake_sum = sum(
        delegate_info.total_stake for delegate_info in all_delegates)
    # Convert the Balance object to a string
    total_stake_str = str(total_stake_sum)

    # Remove unwanted characters
    cleaned_total_stake_str = total_stake_str.replace("τ", "").replace(",", "")

    # Convert to a float
    total_stake_float = float(cleaned_total_stake_str)
    """nominators
    
    """

    nominators_count_list = [len(delegate_info.nominators)
                             for delegate_info in all_delegates]

    """Each validator stake"""

    total_stake_list = [
        delegate_info.total_stake for delegate_info in all_delegates]

    """Validators_APY"""

    # validators_apy = (3600 * 365 / total_stake_float) * 100

    apr, validators_apy = calculate_apr_and_apy(
        emissions_day, number_of_days_in_year, total_stake_float, compounds_per_day)

    staking_apy = validators_apy - (0.18 * validators_apy)

    # Step 1: Create a dictionary with each of the desired columns
    data_dict = {
        'hot_key': [delegate_info.hotkey_ss58 for delegate_info in all_delegates],
        'nominators': nominators_count_list,
        'total_stake': total_stake_list,
        # Broadcasting the same value to all rows
        'apy': [validators_apy for _ in all_delegates]
    }

    # Step 2: Use this dictionary to construct the DataFrame
    del_df = pd.DataFrame(data_dict)

    # Step 3: Add the 'benefits' column with the condition
    del_df['benefits'] = 0.18  # Initialize the column with empty strings
    del_df['tooltips'] = 'This Validator does not provide any reduction in commission fees.'

    # Defining the benefits string
    benefits_string = 0.0
    tooltip_string = "To benefit from a 0% commmission and generate 21.95% more TAO rewards, you need to own 3 Neurons. Details on FirstTensor website."

    # Update the 'benefits' column where 'hot_key' has the specified value
    hot_key_value = "5DvTpiniW9s3APmHRYn8FroUWyfnLtrsid5Mtn5EwMXHN2ed"
    del_df.loc[del_df['hot_key'] == hot_key_value,
               'benefits'] = benefits_string
    del_df.loc[del_df['hot_key'] == hot_key_value,
               'tooltips'] = tooltip_string

    # Filter rows in del_df based on df's 'key'
    filtered_del_df = del_df[del_df['hot_key'].isin(df['key'])]

    # Merge the dataframes side by side based on keys
    result_df = pd.merge(df, filtered_del_df, left_on='key',
                         right_on='hot_key', how='left').drop(columns='hot_key')
    result_df['nominators'].fillna(0, inplace=True)
    result_df.to_csv("test.csv",index=False)

    # Now, loop over the dataframe to save each row in the database
    for index, row in result_df.iterrows():
        delegate, created = Delegate.objects.get_or_create(key=row['key'])
        delegate.name = row['name']
        delegate.url = row['url']
        delegate.description = row['description']
        delegate.signature = row['signature']
        delegate.hot_key = row['key']
        if not np.isnan(row['nominators']):
            delegate.nominators = int(row['nominators'])
        else:
            delegate.nominators = None
        delegate.tooltips = row['tooltips']
        delegate.total_stake = row['total_stake']
        # delegate.apy = row['apy']
        delegate.benefits = row['benefits']
        delegate.save()

        # Fetching data from the API as you provided and save to Supply model
    response = requests.get("https://api.coingecko.com/api/v3/coins/bittensor")
    data = response.json()

    volume_24h = data["market_data"]["total_volume"]["usd"]
    current_price = data["market_data"]["current_price"]["usd"]
    price_change_24h = data["market_data"]["price_change_percentage_24h"]
    subtensor = bittensor.subtensor()
    circulating_supply = float(
    str(subtensor.total_issuance()).replace('τ', '').replace(',', '')) - 572399.00
    total_stakes = float(
    str(subtensor.total_stake()).replace('τ', '').replace(',', ''))
    market_cap = circulating_supply * current_price
    total_supply = 21000000.00
    percent_staked = (total_stakes / circulating_supply) * 100
    # Save the data in the Supply model
    try:
        supply_instance = Supply.objects.get(id=1)
    except Supply.DoesNotExist:
        supply_instance = Supply()

    supply_instance.volume_24h = volume_24h
    supply_instance.current_price = current_price
    supply_instance.change_24h = price_change_24h
    supply_instance.circulating_supply = circulating_supply
    supply_instance.total_stakes = total_stakes
    supply_instance.market_cap = market_cap
    supply_instance.total_supply = total_supply
    supply_instance.percent_staked = percent_staked
    supply_instance.save()


def get_all_delegates(request):

    delegates = Delegate.objects.all()

    delegate_list = []
    for delegate in delegates:
        delegate_dict = {
            'name': delegate.name,
            'details': {'url': delegate.url,
                        'hot_key': delegate.hot_key,
                        'description': delegate.description},
            'tooltip': delegate.tooltips,
            'signature': delegate.signature,
            'nominators': delegate.nominators,
            'total_stake': delegate.total_stake,
            'apr': delegate.apr,
            'apr_average':delegate.apr_average,
            'emission': delegate.emission,
            'reward': delegate.reward,
            
            'commission': delegate.benefits
        }
        delegate_list.append(delegate_dict)

    return HttpResponse(json.dumps(delegate_list, ensure_ascii=False), content_type='application/json')



def get_supply_data(request):
    supplies = Supply.objects.all().values(
        'volume_24h', 'current_price', 'change_24h',
        'circulating_supply', 'total_stakes', 'market_cap',
        'total_supply', 'percent_staked'
    )
    return JsonResponse(list(supplies), safe=False)

##############################Script Functions#####################################


def get_netuid_list():
    while True:
        try:
            output_bytes = subprocess.check_output(['btcli', 's', 'list'])
            output = output_bytes.decode('utf-8')
            matches = re.findall(r'^\s*(\d+)', output, re.MULTILINE)
            netuid_list = [int(match) for match in matches if int(match) != 0]
            netuid_list = netuid_list[:-1]
            return netuid_list
        except subprocess.CalledProcessError:
            pass  # Retry silently

def fetch_metagraph_data(netuid,max_attempts):
    attempt = 1
    while attempt <= max_attempts:
        try:
            output = subprocess.check_output(['btcli', 's', 'metagraph'], input=str(netuid).encode()).decode('utf-8')
            lines = output.split("\n")
            header_positions = []
            data = []
            
            for line in lines:
                if line.startswith("UID"):
                    header_positions = extract_column_positions(line)
                    break

            for line in lines:
                if line and line[0].isdigit():
                    row = [line[start:end].strip() for start, end in header_positions]
                    data.append(row)
                    
            df = pd.DataFrame(data, columns=["UID", "STAKE(τ)", "RANK", "TRUST", "CONSENSUS", "INCENTIVE", "DIVIDENDS", "EMISSION(ρ)", "VTRUST", "VAL", "UPDATED", "ACTIVE", "AXON", "HOTKEY", "COLDKEY"])
            df.to_csv(f'static/netuid{netuid}.csv', index=False)
            break
        except subprocess.CalledProcessError as e:
            time.sleep(5)
            attempt += 1
        except subprocess.WebSocketConnectionClosedException as e:
            time.sleep(5)
            attempt += 1

    if attempt > max_attempts:
        print(f"Failed to fetch metagraph data for UID {netuid} after {max_attempts} attempts.")

def process_metagraph_data(max_attempts=5, sleep_time=5):
    # Main logic
    
    # list_uid = get_netuid_list()
    list_uid = [1,2,3,4,5]


    for netuid in list_uid:
        fetch_metagraph_data(netuid,max_attempts)

    all_data = []
    for netuid in list_uid:
        filepath = f'static/netuid{netuid}.csv'
        try:
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                df['ACTIVE'] = pd.to_numeric(df['ACTIVE'], errors='coerce', downcast='integer')
                df['EMISSION(ρ)'] = pd.to_numeric(df['EMISSION(ρ)'], errors='coerce')
                df['DIVIDENDS'] = pd.to_numeric(df['DIVIDENDS'], errors='coerce')
                active_df = df[df['ACTIVE'] == 1]

                for _, row in active_df.iterrows():
                    print(row['HOTKEY'], row['COLDKEY'], row['EMISSION(ρ)'], row['DIVIDENDS'])
                    all_data.append([row['HOTKEY'], row['COLDKEY'], row['EMISSION(ρ)'], row['DIVIDENDS']])
                print(f"Processed file {filepath}")
        except Exception as e:
            print(f"Error processing file {filepath}. Error message: {e}")

    final_df = pd.DataFrame(all_data, columns=['HOTKEY', 'COLDKEY', 'EMISSION(ρ)', 'DIVIDENDS'])
    aggregated_df = final_df.groupby(['HOTKEY', 'COLDKEY']).agg({'EMISSION(ρ)': 'sum', 'DIVIDENDS': 'sum'}).reset_index()
    aggregated_df.to_csv('static/aggregated_emissions_dividends.csv', index=False)

def extract_column_positions(header_line):
    columns = ["UID", "STAKE(τ)", "RANK", "TRUST", "CONSENSUS", "INCENTIVE", "DIVIDENDS", "EMISSION(ρ)", "VTRUST", "VAL", "UPDATED", "ACTIVE", "AXON", "HOTKEY", "COLDKEY"]
    positions = []
    for col in columns:
        start = header_line.find(col)
        end = start + len(col)
        positions.append((start, end))
    return positions

def get_dividends_for_hotkey(hotkey, netuid, dominance_dict):
    try:
        # Load the specific netuid CSV file
        df = pd.read_csv(f'static/netuid{netuid}.csv')
        # Filter for the specific hotkey
        hotkey_row = df[df['HOTKEY'] == hotkey]
        if not hotkey_row.empty:
            return hotkey_row['DIVIDENDS'].iloc[0] * (dominance_dict[netuid] / 100) * 2952
    except FileNotFoundError:
        print(f"File netuid{netuid}.csv not found.")
    return 0

def process_to_csv(input_file, output_csv):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Find the start of the data
    start_line = 0
    for i, line in enumerate(lines):
        if 'NETUID' in line:
            start_line = i
            break

    # Extract relevant lines
    relevant_lines = lines[start_line:-1]  # Skip the last line

    # Process each line into a list of values
    data = []
    for line in relevant_lines:
        # Use regular expression to split the line
        # The pattern will split on spaces but will treat sequences like '1.02 K' or '1000000.00 T' as single units
        values = re.split(r'(?<!\d)\s+(?!\d{1,2}\s)', line.strip())
        data.append(values)

    # Create a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Save to CSV
    df.to_csv(output_csv, index=False)

def get_dominance_dict():
    # Run the btcli s list command and capture the output
    output = subprocess.check_output(['btcli', 's', 'list'], text=True)

    # Save the output to a file
    with open('temp_output.txt', 'w') as file:
        file.write(output)

    # Specify the output CSV file path
    output_csv_path = 'output.csv'

    # Process the saved output to CSV with the updated code
    process_to_csv('temp_output.txt', output_csv_path)

    # Load the saved output from the file into a DataFrame
    df = pd.read_csv(output_csv_path, delimiter=',', skipinitialspace=True, usecols=['NETUID', 'N', 'MAX_N', 'EMISSION', 'TEMPO', 'BURN', 'POW', 'SUDO'])

    # Function to replace specific 'K' values and convert others
    def replace_k_values(value):
        if value == '1.02 K':
            return 1024
        elif value == '2.05 K':
            return 2048
        elif 'K' in str(value):
            return int(float(value.replace('K', '')) * 1000)
        return value

    # Apply the function to the 'N' column
    df['N'] = df['N'].apply(replace_k_values)

    df['N'] = df['N'].fillna(0).astype('int64')

    # Remove '%' sign from 'EMISSION' column and convert it to float
    df['EMISSION'] = df['EMISSION'].str.rstrip('%').astype(float)

    # Create a dictionary from 'NETUID' and 'EMISSION'
    dominance_dict = pd.Series(df.EMISSION.values, index=df.NETUID).to_dict()

    # Replace NaN values with 0.0
    dominance_dict = {k: 0.0 if pd.isna(v) else v for k, v in dominance_dict.items()}

    return dominance_dict

# Call the function to get dominance_dict
dominance_dict = get_dominance_dict()


def calculate_and_save_daily_tao_rewards(github_url, dominance_dict, output_csv_path):
    # Fetch GitHub data
    response = requests.get(github_url)
    github_data = response.json()

    # Initialize an empty list to store results
    results = []

    # Iterate over all HOTKEYS
    for hotkey in github_data.keys():
        # Extract the HOTKEY from the GitHub data
        hotkey_six_letters = hotkey[:6]
        
        # Initialize daily_tao_rewards for the current HOTKEY
        daily_tao_rewards = 0

        # Iterate over all netuids in dominance dictionary
        #delete key 0 from dict
        if 0 in dominance_dict:
            del dominance_dict[0]

        for netuid in dominance_dict.keys():
            daily_tao_rewards += get_dividends_for_hotkey(hotkey_six_letters, netuid, dominance_dict)

        # Append results to the list
        results.append({'HOTKEY': hotkey_six_letters, 'Total_Daily_TAO_Rewards': daily_tao_rewards})

    # Create a DataFrame from the results list
    results_df = pd.DataFrame(results)


    # Save the DataFrame to a CSV file
    results_df.to_csv(output_csv_path, index=False)
def calculate_and_save_apr():
    # Open the file and clear its contents
    df = pd.read_csv('static/TAO_Rewards.csv')

    with open('delegate_info.txt', 'w') as file:
        delegates = Delegate.objects.all()

        for delegate in delegates:
            hotkey_prefix = delegate.hot_key[:6]
            validator_stake = delegate.total_stake

            # Replace NaN with 0 for validator_stake
            validator_stake = validator_stake if pd.notna(validator_stake) else 0

            if validator_stake is not None and validator_stake > 0:  # Check for None and greater than zero
                matching_row = df[df['HOTKEY'].str.startswith(hotkey_prefix)]

                if not matching_row.empty:
                    if hotkey_prefix == '5DvTpi':
                        percentage_to_be_taken_out = 0
                    elif hotkey_prefix == '5EhvL1' or hotkey_prefix == '5FFApa':
                        percentage_to_be_taken_out = 9
                    elif hotkey_prefix == '5HK5tp':
                        percentage_to_be_taken_out = 1
                    else: 
                        percentage_to_be_taken_out = 18

                    reward = matching_row['Total_Daily_TAO_Rewards'].iloc[0]

                    apr = (365 * reward) / validator_stake
                    apr = apr - ((percentage_to_be_taken_out / 100) * apr)

                    # Save the data for all hotkeys
                    delegate.reward = str(reward)
                    apr = round(apr, 4) * 100
                    delegate.apr = apr
                    delegate.save()

                    # Write data to the file for all hotkeys
                    file.write(f'Hotkey: {delegate.hot_key}, Prefix: {hotkey_prefix}, Reward: {reward}, APR: {apr}, Percent Taken Out: {percentage_to_be_taken_out}\n')
                else:
                    print(f'No matching row for hotkey prefix: {hotkey_prefix}')
            else:
                print(f'Validator stake is None or 0 for hotkey prefix: {hotkey_prefix}')

def calculate_and_save_apr_every_two_hours():
    # Open the file and clear its contents
    df = pd.read_csv('static/TAO_Rewards.csv')

    for delegate in Delegate.objects.all():
        hotkey_prefix = delegate.hot_key[:6]
        validator_stake = delegate.total_stake

        # Replace NaN with 0 for validator_stake
        validator_stake = validator_stake if pd.notna(validator_stake) else 0

        if validator_stake is not None and validator_stake > 0:
            matching_row = df[df['HOTKEY'].str.startswith(hotkey_prefix)]

            if not matching_row.empty:
                if hotkey_prefix == '5DvTpi':
                    percentage_to_be_taken_out = 0
                elif hotkey_prefix == '5EhvL1' or hotkey_prefix == '5FFApa':
                    percentage_to_be_taken_out = 9
                elif hotkey_prefix == '5HK5tp':
                    percentage_to_be_taken_out = 1
                else:
                    percentage_to_be_taken_out = 18

                reward = matching_row['Total_Daily_TAO_Rewards'].iloc[0]

                apr = (365 * reward) / validator_stake
                apr = apr - ((percentage_to_be_taken_out / 100) * apr)

                # Save the data for all hotkeys in the AprSave model
                AprSave.objects.create(
                    validator=delegate.name,
                    apr=apr,
                    key=hotkey_prefix,
                    date=timezone.now()
                )

               
            else:
                print(f'No matching row for hotkey prefix: {hotkey_prefix}')
        else:
            print(f'Validator stake is None or 0 for hotkey prefix: {hotkey_prefix}')


@csrf_exempt
def delegate_undelegate_status(request):
    if request.method == 'OPTIONS':
        # Handle OPTIONS request (preflight)
        response = JsonResponse({'message': 'CORS preflight successful'})
        response['Access-Control-Allow-Origin'] = '*'  # Update with your frontend URL
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            wallet_address = data.get('wallet_address', '')
            amount = data.get('amount', '')
            action = data.get('action', '')
            validator = data.get('validator', '')

            # Additional validation or processing can be done here

            # Save the values to the database
            transaction = DelegateUndelegateStatus.objects.create(
                wallet_address=wallet_address,
                amount=amount,
                action=action,
                validator=validator,
                date=timezone.now()
            )

            transaction.save()
            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta

@shared_task
def calculate_and_save_average():
    # Calculate the datetime 7 days ago
    seven_days_ago = timezone.now() - timedelta(days = 7)

    # Filter data from the last 7 days
    data = AprSave.objects.filter(date__gte=seven_days_ago)
    
    # Calculate average for each 'hotkey'
    averages = data.values('key', 'validator').annotate(apr_average=Avg('apr'))

    # Save or update averages into MyDelegate table
    for average in averages:
        hotkey = average['key']
        validator = average['validator']
        apr_average = average['apr_average']
        average_apr = round(apr_average, 2) if apr_average is not None else None

        # Update existing record or create a new one
        WeeklyAprAverage.objects.update_or_create(
            validator=validator,
            key=hotkey,
            defaults={'average_apr': average_apr, 'date': timezone.now()}
        )

        # Update delegates
        delegates = Delegate.objects.filter(hot_key__startswith=hotkey[:6])
        for delegate in delegates:
            delegate.apr_average = average_apr  # Use the rounded value here as well
            delegate.save()



@shared_task
def scripts():
    process_metagraph_data()
    dominance_dict = get_dominance_dict()
    output_csv_path = 'static/TAO_Rewards.csv'
    calculate_and_save_daily_tao_rewards('https://raw.githubusercontent.com/opentensor/bittensor-delegates/master/public/delegates.json', dominance_dict, output_csv_path)
    calculate_and_save_apr_every_two_hours()





