#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:38:43 2021

@author: aniqahsan 
"""
#includes updating system and location params for scenario from one file


import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import time
import os
import cvxpy as cp

from Code.Network.Network import Network_STEVFNs
from Code.Results import GMPA_Results
from Code.Plotting import SG_STEVFNS_Plotting

case_study_name = "SG-MY_Collab"
# case_study_name = "SG_Case_Study"

# case_study_name = "Testingsss"
# case_study_name = "Tester"
# case_study_name = "SG_Trial_OG_Only"
# case_study_name = "Testing"
# case_study_name = "Test_for_PTGT" 

#### Define Input Files ####
# case_study_name = "EM_Case_Study"
# case_study_name = "SG_Case_Study"


###### Autarky Case Studies #########
# case_study_name = "Autarky_SG"
# case_study_name = "Autarky_ID"
# case_study_name = "Autarky_MY"
# case_study_name = "Autarky_VN"
# case_study_name = "Autarky_PH"
# case_study_name = "Autarky_TH"
# case_study_name = "Autarky_KH"
# case_study_name = "Autarky_LA"
# case_study_name = "Autarky_BN"
# case_study_name = "SG_BN_Collab"

# case_study_name = "Autarky_AU"
# case_study_name = "Autarky_IN"
# case_study_name = "Autarky_SA"
# case_study_name = "Autarky_AE"

###### Two Country Case Studies #########
# case_study_name = "SG-ID_Autarky"
# case_study_name = "SG-ID_Collab"

# case_study_name = "SG-BN_Collab"
# case_study_name = "SG-BN-MY_Collab"


# case_study_name = "SG-MY_Autarky"
# case_study_name = "SG-MY_Collab"

# case_study_name = "SG-PH_Autarky"
# case_study_name = "SG-PH_Collab"

# case_study_name = "ID-MY_Autarky"
# case_study_name = "ID-MY_Collab"

# case_study_name = "MY-PH_Autarky"
# case_study_name = "MY-PH_Collab"

# case_study_name = "ID-PH_Autarky"
# case_study_name = "ID-PH_Collab"

# case_study_name = "VN-TH_Autarky"
# case_study_name = "VN-TH_Collab"

# case_study_name = "VN-LA_Autarky"
# case_study_name = "VN-LA_Collab"

# case_study_name = "VN-KH_Autarky"
# case_study_name = "VN-KH_Collab"

# case_study_name = "TH-LA_Autarky"
# case_study_name = "TH-LA_Collab"

# case_study_name = "TH-KH_Autarky"
# case_study_name = "TH-KH_Collab"

# case_study_name = "LA-KH_Autarky"
# case_study_name = "LA-KH_Collab"

###### Three Country Case Studies #########
# case_study_name = "SG-ID-MY_Autarky"
# case_study_name = "SG-ID-MY_Collab"

# case_study_name = "SG-ID-PH_Autarky"
# case_study_name = "SG-ID-PH_Collab"
# 
# case_study_name = "SG-MY-PH_Autarky"
# case_study_name = "SG-MY-PH_Collab"

# case_study_name = "ID-MY-PH_Autarky"
# case_study_name = "ID-MY-PH_Collab"

# case_study_name = "VN-TH-LA_Autarky"
# case_study_name = "VN-TH-LA_Collab"

# case_study_name = "VN-TH-KH_Autarky"
# case_study_name = "VN-TH-KH_Collab"

# case_study_name = "TH-LA-KH_Autarky"
# case_study_name = "TH-LA-KH_Collab"

# case_study_name = "VN-LA-KH_Autarky"
# case_study_name = "VN-LA-KH_Collab"

###### Four Country Case Studies #########

# case_study_name = "SG-ID-MY-PH_Autarky"
# case_study_name = "SG-ID-MY-PH_Collab"

# case_study_name = "VN-TH-LA-KH_Autarky"
# case_study_name = "VN-TH-LA-KH_Collab"

###### BAU_No_Action #######
# case_study_name = "BAU_No_Action"

base_folder = os.path.dirname(__file__)
data_folder = os.path.join(base_folder, "Data")
case_study_folder = os.path.join(data_folder, "Case_Study", case_study_name)
location_parameters_filename = os.path.join(case_study_folder, "Location_Parameters.csv")
system_parameters_filename = os.path.join(case_study_folder, "System_Parameters.csv")
network_structure_filename = os.path.join(case_study_folder, "Network_Structure.csv")
results_filename = os.path.join(case_study_folder, "total_data.csv")
unrounded_results_filename = os.path.join(case_study_folder, "total_data_unrounded.csv")


network_structure_df = pd.read_csv(network_structure_filename, dtype = {"Location_1":str, "Location_2":str})
location_parameters_df = pd.read_csv(location_parameters_filename, dtype = {"Location":str})
system_parameters_df = pd.read_csv(system_parameters_filename)
# location_parameters_df.loc[:, "Location"] = location_parameters_df["Location"].astype("string")

start_time = time.time()


my_network = Network_STEVFNs()
my_network.build(network_structure_df)


end_time = time.time()
print("Time taken to build network = ", end_time - start_time, "s")
total_df = pd.DataFrame()
total_df_1 = pd.DataFrame()

for counter1 in range(0, len(network_structure_df.columns) - 6):
    asset_parameters_df = network_structure_df.iloc[:, [0, 1, 2, 3, counter1 + 6]] #8 reaches to first scenario
    my_network.scenario_name = asset_parameters_df.columns.values[4]
    asset_parameters_df.columns.values[4] = "Asset_Type"
    asset_parameters_df.loc[:, "Asset_Type"] = asset_parameters_df["Asset_Type"].astype("string") 
    system_params_df = system_parameters_df.iloc[:, [0, (counter1 * 2) + 1, 2 + (counter1 * 2)]]
    system_params_df.columns.values[1] = "value"
    system_params_df.columns.values[2] = "unit"
    loc_counter = 3 * counter1

### Update Network Parameters ###
    start_time = time.time()
    my_network.update(location_parameters_df, asset_parameters_df, system_params_df)    
    end_time = time.time()
    print("Time taken to update network = ", end_time - start_time, "s")
    start_time = time.time()
    
    # my_network.solve_problem()
    my_network.problem.solve(solver = cp.CLARABEL, warm_start=True, ignore_dpp=True, verbose=False)
    # my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=10000, feastol=1e-5, reltol=1e-5, abstol=1e-5, ignore_dpp=True, verbose=False)
    # my_network.problem.solve(solver = cp.SCS, warm_start=True, max_iters=10000, ignore_dpp=True, verbose=False)
    end_time = time.time()

    
    ### Plot Results ############
    print("Scenario: ", my_network.scenario_name)
    print("Time taken to solve problem = ", end_time - start_time, "s")
    print(my_network.problem.solution.status)
    if my_network.problem.value == float("inf"):
        continue
    print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD")
    print("Total emissions = ", my_network.assets[0].asset_size(), "MtCO2e")
    # SG_STEVFNS_Plotting.plot_asset_costs(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_NH3_inflows(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_NH3_outflows(my_network, asset_parameters_df)
    SG_STEVFNS_Plotting.plot_all(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_emissions_by_asset(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_NH3_inflows(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_NH3_outflows(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_loc_NH3_output_flows(my_network, 0, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_loc_NH3_input_flows(my_network, 0, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_sizes_costs(my_network, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_output_flows(my_network, 0, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_output_flows(my_network, 1, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_output_flows(my_network, 2, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_output_flows(my_network, 3, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_input_flows(my_network, 0, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_input_flows(my_network, 1, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_input_flows(my_network, 2, asset_parameters_df)
    # SG_STEVFNS_Plotting.plot_Location_EL_input_flows(my_network, 3, asset_parameters_df)
        
    # Export cost results to pandas dataframe
#     t_df = GMPA_Results.export_total_data(my_network, location_parameters_df, asset_parameters_df)
#     t1_df = GMPA_Results.export_total_data_not_rounded(my_network, location_parameters_df, asset_parameters_df)
#     # t_df = GMPA_Results.export_total_data(my_network, location_params_df, asset_parameters_df)
#     # t1_df = GMPA_Results.export_total_data_not_rounded(my_network, location_params_df, asset_parameters_df)
#     if counter1 == 0:
#         total_df = t_df
#         total_df_1 = t1_df
#     else:
#         total_df = pd.concat([total_df, t_df], ignore_index=True)
#         total_df_1 = pd.concat([total_df_1, t1_df], ignore_index=True)



# #### Save Result
# total_df.to_csv(results_filename, index=False, header=True)
# total_df_1.to_csv(unrounded_results_filename, index=False, header=True)
