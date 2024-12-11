#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
"""

import cvxpy as cp
from ..Base_Assets import Asset_STEVFNs
import numpy as np


class Diesel_Storage_Asset(Asset_STEVFNs):
    """Class of Diesel storage asset"""
    asset_name = "Diesel_Storage"
    source_node_type = "Diesel"
    target_node_type = "Diesel"
    
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["sizing_constant"]
        usage_constant_1 = params["usage_constant_1"]
        return sizing_constant * cp.max(flows) + usage_constant_1 * cp.sum(flows)
        # return sizing_constant * cp.max(flows)
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["conversion_factor"]
        return conversion_factor * flows
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True),
                          "usage_constant_1": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"conversion_factor": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        self.target_node_times[-1] = self.source_node_times[0]
        self.target_node_times[:-1] = self.source_node_times[1:]
        return
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["sizing_constant"].value = self.cost_fun_params["sizing_constant"].value * NPV_factor
        return
    
    def _update_usage_constant(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["usage_constant_1"].value = (self.cost_fun_params["usage_constant_1"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Update cost parameters based on NPV#
        self._update_sizing_constant()
        self._update_usage_constant()
        return
    
    def outflow(self, loc):
        return self.flows.value
    
    def inflow(self, loc):
        temp_flows = self.conversion_fun(
            self.flows,
            self.conversion_fun_params).value
        component_flows = np.zeros_like(temp_flows)
        component_flows[1:] = temp_flows[:-1]
        component_flows[0] = temp_flows[-1]
        return component_flows
    
    def get_times(self):
        return np.arange(self.asset_structure["Start_Time"], self.asset_structure["End_Time"], self.period)
