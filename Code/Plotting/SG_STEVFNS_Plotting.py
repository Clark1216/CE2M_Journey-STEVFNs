# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:39:14 2024

@author: Rammah & aniqahsan
"""

import numpy as np
from ..Plotting import bar_chart_artist, stackplot_artist, twin_line_artist, linegraph_artist

def plot_asset_sizes(my_network, asset_parameters_df, bar_width = 1.0, bar_spacing = 3.0):
    # Plots the size of assets in the system #
    
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df = my_network.system_structure_df.copy()
    asset_sizes_array = np.zeros(og_df.shape[0])
    for counter1 in range(len(asset_sizes_array)):
        asset_sizes_array[counter1] = my_network.assets[counter1].asset_size()
    og_df["Asset_Size"] = asset_sizes_array
    og_df = og_df.drop(og_df[og_df['Asset_Class'] == 'CO2_Budget'].index)
    max_asset_size = np.max(asset_sizes_array)
    # Set minimum asset size to plot
    min_asset_size = max_asset_size * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Size"] >= min_asset_size
    og_df = og_df[con1]
    og_df["Asset_Class"] = og_df["Asset_Class"] + " " + asset_parameters_df["Asset_Type"]
    
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_size = my_network.assets[asset_number].asset_size()
            # check if asset is too small
            if asset_size < min_asset_size:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_size]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_size = my_network.assets[asset_number].asset_size()
                # check if asset is too small
                if asset_size < min_asset_size:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_size]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Size (GWh)"
    my_artist.title = "Size of Assets in the System by Location and Location Pair \n Scenario: " + my_network.scenario_name
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return


def plot_asset_costs(my_network, asset_parameters_df, bar_width = 1.0, bar_spacing = 3.0):
    # Plots the cost of assets in the system #
    
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df = my_network.system_structure_df.copy()
    asset_costs_array = np.zeros(og_df.shape[0])
    for counter1 in range(len(asset_costs_array)):
        asset_costs_array[counter1] = my_network.assets[counter1].cost.value
    og_df["Asset_Cost"] = asset_costs_array
    max_asset_cost = np.max(asset_costs_array)
    og_df["Asset_Class"] = og_df["Asset_Class"] + " " + asset_parameters_df["Asset_Type"]
    # Set minimum asset size to plot
    min_asset_cost = max_asset_cost * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Cost"] >= min_asset_cost
    og_df = og_df[con1]
    
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_cost = my_network.assets[asset_number].cost.value
            # check if asset is too small
            if asset_cost < min_asset_cost:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_cost]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_cost = my_network.assets[asset_number].cost.value
                # check if asset is too small
                if asset_cost < min_asset_cost:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_cost]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Cost (Billion USD)"
    my_artist.title = "Cost of Assets in the System by Location and Location Pair \n Scenario: " + my_network.scenario_name
    my_artist.text_data = {"x": 0.12, "y": 0.5, "s": "Total Cost = " + f"{my_network.cost.value: .5}" + " Bil USD"}
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return

def plot_emissions_by_asset(my_network, asset_parameters_df, bar_width = 1.0, bar_spacing = 3.0): 
    # Plots the emissions of assets in the system #
    data = my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    emission_Assets = {"PP_CO2", "FF_to_HTH", "PP_NGS_CCGT_CO2", "PP_NGS_SCGT_CO2"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con = data["Asset_Class"].isin(emission_Assets)
    og_df = data[con]
    if og_df.empty:
        return
    assets_emissions_array = np.zeros(og_df.shape[0])
    counter_em_array = 0
    for index, row in og_df.iterrows():
        asset_number = row["Asset_Number"]
        assets_emissions_array[counter_em_array] = sum(my_network.assets[asset_number].emissions())
        counter_em_array += 1
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df["Asset_Emissions"] = assets_emissions_array
    max_asset_emissions = np.max(assets_emissions_array)
    # Set minimum asset size to plot
    min_asset_emissions = max_asset_emissions * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Emissions"] >= min_asset_emissions
    og_df = og_df[con1]
    og_df["Asset_Class"] = og_df["Asset_Class"] + " " + asset_parameters_df["Asset_Type"]
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_emissions = sum(my_network.assets[asset_number].emissions())
            # check if asset is too small
            if asset_emissions < min_asset_emissions:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_emissions]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_emissions = sum(my_network.assets[asset_number].emissions())
                # check if asset is too small
                if asset_emissions < min_asset_emissions:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_emissions]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Emissions (MtCO2)"
    my_artist.title = "Asset Emissions in the System by Location and Location Pair \n Scenario: " + my_network.scenario_name
    # my_artist.text_data = {"x": 0.12, "y": 0.5, "s": "Total Cost = " + f"{my_network.cost.value: .5}" + " MtCO2"}
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return

def plot_Location_emissions(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    emission_Assets = {"PP_CO2", "FF_to_HTH", "PP_NGS_CCGT_CO2", "PP_NGS_SCGT_CO2"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(emission_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    #set location 1 as desired location then restrict by that location and asset class
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        #Str count is to work around same asset type and name but different locations
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].emissions() #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Emissions (MtCO2)" #what is the unit
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Carbon emissions at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_EL_input_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    EL_Assets = {"EL_Transport", "BESS", "NH3_to_EL", "RE_PV", "RE_WIND", "RE_max", "RE_PV_Constant", 
                 "RE_PV_Openfield_Lim", "RE_PV_Rooftop_Lim", "RE_WIND_Constant", "RE_WIND_Offshore_Lim", 
                 "RE_WIND_Onshore_Lim", "PP_CO2", "PP_COAL_CO2", "PP_NGS_CCGT_CO2", "PP_NGS_SCGT_CO2", 
                 "RE_Compiled", "Biofuel_to_EL", "H2_to_EL", "NG_to_EL", "Nuclear", "SW_to_EL"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(EL_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    #set location 1 as desired location then restrict by that location and asset class
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        #Str count is to work around same asset type and name but different locations
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].inflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy into EL node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_EL_output_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    EL_Assets = {"EL_Transport", "BESS", "EL_to_NH3", "EL_to_HTH", "EL_to_Cooling", "EL_to_GT", "EL_to_H2", "EL_to_LTH", "EL_to_PT"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(EL_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].outflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy out of EL node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_Gasoline_input_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    EL_Assets = {"Gasoline_Production", "Gasoline_Transport", "Gasoline_Storage"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(EL_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    #set location 1 as desired location then restrict by that location and asset class
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        #Str count is to work around same asset type and name but different locations
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].inflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Gasoline Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Gasoline into Gasoline node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_Gasoline_output_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    EL_Assets = {"Gasoline_to_PT", "Gasoline_to_GT", "Gasoline_Transport", "Gasoline_Storage"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(EL_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].outflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Gasoline Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Gasoline out of Gasoline node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_Diesel_input_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    EL_Assets = {"Diesel_Production", "Diesel_Transport", "Diesel_Storage"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(EL_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    #set location 1 as desired location then restrict by that location and asset class
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        #Str count is to work around same asset type and name but different locations
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].inflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Diesel Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Diesel into Diesel node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_Diesel_output_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    EL_Assets = {"Diesel_to_PT", "Diesel_to_GT", "Diesel_Transport", "Diesel_Storage"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(EL_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].outflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Diesel Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Diesel out of Diesel node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_NG_input_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    NG_Assets = {"NG_Production", "NG_Storage", "NG_Transport"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(NG_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    #set location 1 as desired location then restrict by that location and asset class
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        #Str count is to work around same asset type and name but different locations
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].inflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "NG Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Natural Gas into NG node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_Location_NG_output_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    NG_Assets = {"NG_Storage", "NG_to_EL", "NG_Transport"}
    #array stores assets which need mapping, must include asset here when built and create inflow(Loc) accordingly
    con2 = tdf1["Asset_Class"].isin(NG_Assets)
    tdf2 = tdf1[con2]
    component_name = ""
    if tdf2.empty:
        return
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].outflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary[component_name]/24
    my_artist.ylabel = "Natural Gas Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Natural Gas out of NG node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
    my_artist.plot()
    return

def plot_loc_NH3_output_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    NH3_Assets =  {"NH3_to_EL", "NH3_to_HTH"} #assets associated with stackplot graph, have method NOutflow(loc)
    NH3_Twin_Assets = {"NH3_Transport", "NH3_Storage"} #assets associated with twin graph, have method Outflow(loc)
    con2 = tdf1["Asset_Class"].isin(NH3_Assets)
    con3 = tdf1["Asset_Class"].isin(NH3_Twin_Assets) 
    tdf2 = tdf1[con2]
    tdf3 = tdf1[con3]
    if tdf2.empty and tdf3.empty:
        return     
    component_name = ""
    #set location 1 as desired location then restrict by that location and asset class
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].outflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    for index, row in tdf3.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in twin_flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        twin_flows_dictionary[component_name] = my_network.assets[asset_number].outflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()    
    if tdf3.empty:
        my_artist = stackplot_artist()
        my_artist.flows_dictionary = flows_dictionary
        my_artist.times = times_dictionary[list(flows_dictionary.keys())[0]]/24
        my_artist.ylabel = "Ammonia Flow (Gg)"
        my_artist.xlabel = "Time (Days)"
        my_artist.title = "Flow of Ammonia out of NH3 node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
        my_artist.plot()
    elif tdf2.empty:
        my_twin_artist = linegraph_artist()
        my_twin_artist.times = times_dictionary[list(twin_flows_dictionary.keys())[0]]/24
        my_twin_artist.flows_dictionary = twin_flows_dictionary
        my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
        my_twin_artist.xlabel = "Time (Days)"
        my_twin_artist.title = "Flow of Ammonia out of NH3 node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
        my_twin_artist.plot()
    else:
        my_artist = stackplot_artist()
        my_artist.flows_dictionary = flows_dictionary
        my_artist.times = times_dictionary[list(flows_dictionary.keys())[0]]/24
        my_artist.ylabel = "Ammonia Flow (Gg)"
        my_artist.xlabel = "Time (Days)"
        my_artist.title = "Flow of Ammonia out of NH3 node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
        # my_artist.plot()
        my_twin_artist = twin_line_artist()
        my_twin_artist.flows_dictionary = twin_flows_dictionary
        my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
        my_twin_artist.attach_artist(my_artist)
        my_twin_artist.plot()
    return

def plot_loc_NH3_input_flows(my_network, Loc, asset_parameters_df):
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    data =  my_network.system_structure_df.join(asset_parameters_df["Asset_Type"])
    con1 = (data["Location_1"] == Loc) | (data["Location_2"] == Loc)
    tdf1 = data[con1]
    NH3_Assets =  {"EL_to_NH3"}
    NH3_Twin_Assets = {"NH3_Transport", "NH3_Storage"}
    con2 = tdf1["Asset_Class"].isin(NH3_Assets)
    con3 = tdf1["Asset_Class"].isin(NH3_Twin_Assets) 
    tdf2 = tdf1[con2]
    tdf3 = tdf1[con3]
    if tdf2.empty and tdf3.empty:
        return 
    component_name = ""
    for index, row in tdf2.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        flows_dictionary[component_name] = my_network.assets[asset_number].inflow(Loc) #component flow added
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    for index, row in tdf3.iterrows():
        count = 2
        component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) 
        while component_name in twin_flows_dictionary:
            component_name = row["Asset_Class"] + " " + str(row["Asset_Type"]) + " " + str(count)
            count = count + 1
        asset_number = row["Asset_Number"]
        twin_flows_dictionary[component_name] = my_network.assets[asset_number].inflow(Loc) #component flow added 
        times_dictionary[component_name] = my_network.assets[asset_number].get_times()
    if tdf3.empty:
        my_artist = stackplot_artist()
        my_artist.flows_dictionary = flows_dictionary
        my_artist.times = times_dictionary[list(flows_dictionary.keys())[0]]/24
        my_artist.ylabel = "Ammonia Flow (Gg)"
        my_artist.xlabel = "Time (Days)"
        my_artist.title = "Flow of Ammonia into NH3 node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
        my_artist.plot()
    elif tdf2.empty:
        my_twin_artist = linegraph_artist()
        my_twin_artist.times = times_dictionary[list(twin_flows_dictionary.keys())[0]]/24
        my_twin_artist.flows_dictionary = twin_flows_dictionary
        my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
        my_twin_artist.xlabel = "Time (Days)"
        my_twin_artist.title = "Flow of Ammonia into NH3 node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
        my_twin_artist.plot()
    else:
        my_artist = stackplot_artist()
        my_artist.flows_dictionary = flows_dictionary
        my_artist.times = times_dictionary[list(flows_dictionary.keys())[0]]/24
        my_artist.ylabel = "Ammonia Flow (Gg)"
        my_artist.xlabel = "Time (Days)"
        my_artist.title = "Flow of Ammonia into NH3 node at " + str(Loc) + " \n Scenario: " + my_network.scenario_name
        # my_artist.plot()
        my_twin_artist = twin_line_artist()
        my_twin_artist.flows_dictionary = twin_flows_dictionary
        my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
        my_twin_artist.attach_artist(my_artist)
        my_twin_artist.plot()
    return

def plot_all(my_network, asset_parameters_df):
    plot_asset_sizes(my_network, asset_parameters_df)
    plot_asset_costs(my_network, asset_parameters_df)
    plot_emissions_by_asset(my_network, asset_parameters_df)
    loc_df = asset_parameters_df[["Location_1", "Location_2"]]
    locations = loc_df.stack().unique()
    for location in locations:
        plot_Location_EL_input_flows(my_network, location, asset_parameters_df)
        plot_Location_EL_output_flows(my_network, location, asset_parameters_df)
        plot_loc_NH3_input_flows(my_network, location, asset_parameters_df)
        plot_loc_NH3_output_flows(my_network, location, asset_parameters_df)
        plot_Location_Gasoline_input_flows(my_network, location, asset_parameters_df)
        plot_Location_Gasoline_output_flows(my_network, location, asset_parameters_df)
        plot_Location_Diesel_input_flows(my_network, location, asset_parameters_df)
        plot_Location_Diesel_output_flows(my_network, location, asset_parameters_df)
        plot_Location_NG_input_flows(my_network, location, asset_parameters_df)
        plot_Location_NG_output_flows(my_network, location, asset_parameters_df)
        plot_Location_emissions(my_network, location, asset_parameters_df)
    return 

def plot_sizes_costs(my_network, asset_parameters_df):
    plot_asset_sizes(my_network, asset_parameters_df)
    plot_asset_costs(my_network, asset_parameters_df)
    return
    
def plot_all_by_loc(my_network, asset_parameters_df):
    plot_all(my_network, asset_parameters_df)
    return

def plot_all_by_type(my_network, asset_parameters_df):
    plot_asset_sizes(my_network, asset_parameters_df)
    plot_asset_costs(my_network, asset_parameters_df)
    plot_emissions_by_asset(my_network, asset_parameters_df)
    loc_df = asset_parameters_df[["Location_1", "Location_2"]]
    locations = loc_df.stack().unique()
    for location in locations:
        plot_Location_EL_input_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_EL_output_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_loc_NH3_input_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_loc_NH3_output_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_Diesel_input_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_Diesel_output_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_Gasoline_input_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_Gasoline_output_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_NG_input_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_NG_output_flows(my_network, location, asset_parameters_df)
    for location in locations:
        plot_Location_emissions(my_network, location, asset_parameters_df)
    return 

def plot_emissions(my_network, asset_parameters_df):
    plot_emissions_by_asset(my_network, asset_parameters_df)
    loc_df = asset_parameters_df[["Location_1", "Location_2"]]
    locations = loc_df.stack().unique()
    for location in locations:
        plot_Location_emissions(my_network, location, asset_parameters_df)
    return
    
def plot_NH3_inflows(my_network, asset_parameters_df):
    loc_df = asset_parameters_df[["Location_1", "Location_2"]]
    locations = loc_df.stack().unique()
    for location in locations:
        plot_loc_NH3_input_flows(my_network, location, asset_parameters_df)
    return

def plot_NH3_outflows(my_network, asset_parameters_df):
    loc_df = asset_parameters_df[["Location_1", "Location_2"]]
    locations = loc_df.stack().unique()
    for location in locations:
        plot_loc_NH3_output_flows(my_network, location, asset_parameters_df)
    return

    
     
 