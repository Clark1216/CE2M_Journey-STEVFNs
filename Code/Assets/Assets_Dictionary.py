#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:16:24 2021

@author: aniqahsan
"""

from .EL_Demand import EL_Demand_Asset
from .HTH_Demand import HTH_Demand_Asset
from .CG import CG_Asset
from .EL_to_HTH import EL_to_HTH_Asset
from .RE import RE_Asset
from .BESS import BESS_Asset
from .EL_to_NH3 import EL_to_NH3_Asset
from .NH3_to_EL import NH3_to_EL_Asset
from .NH3_Storage import NH3_Storage_Asset
from .NH3_to_HTH import NH3_to_HTH_Asset
from .EL_Transport import EL_Transport_Asset
from .NH3_Transport import NH3_Transport_Asset
from .RE_PV import RE_PV_Asset
from .RE_WIND import RE_WIND_Asset
from .RE_max import RE_max_Asset
from .EL_Demand_UM import EL_Demand_UM_Asset
from .EL_Demand_Constant import EL_Demand_Constant_Asset
from .RE_PV_Constant import RE_PV_Constant_Asset
from .RE_WIND_Constant import RE_WIND_Constant_Asset
from .CO2_Budget import CO2_Budget_Asset
from .PP_CO2 import PP_CO2_Asset
from .RE_PV_Rooftop_Lim import RE_PV_Rooftop_Lim_Asset
from .RE_PV_Openfield_Lim import RE_PV_Openfield_Lim_Asset
from .RE_WIND_Onshore_Lim import RE_WIND_Onshore_Lim_Asset
from .RE_WIND_Offshore_Lim import RE_WIND_Offshore_Lim_Asset
from .PP_NGS_CCGT_CO2 import PP_NGS_CCGT_CO2_Asset
from .PP_NGS_SCGT_CO2 import PP_NGS_SCGT_CO2_Asset
from .PP_COAL_CO2 import PP_COAL_CO2_Asset
from .FF_to_HTH import FF_to_HTH_Asset
from .H2_Storage import H2_Storage_Asset
from .H2_to_EL import H2_to_EL_Asset
from .NG_Storage import NG_Storage_Asset
from .EL_to_H2 import EL_to_H2_Asset
from .NG_Transport import NG_Transport_Asset
from .NG_to_EL import NG_to_EL_Asset
from .SW_to_EL import SW_to_EL_Asset 
from .EL_to_LTH import EL_to_LTH_Asset
from .EL_to_Cooling import EL_to_Cooling_Asset
from .Biofuel_to_EL import Biofuel_to_EL_Asset
from .LTH_Demand import LTH_Demand_Asset
from .Cooling_Demand import Cooling_Demand_Asset 
from .PT_Demand import PT_Demand_Asset
from .GT_Demand import GT_Demand_Asset
from .Gasoline_to_PT import Gasoline_to_PT_Asset 
from .Gasoline_to_GT import Gasoline_to_GT_Asset 
from .Diesel_to_PT import Diesel_to_PT_Asset 
from .Diesel_to_GT import Diesel_to_GT_Asset 
from .RE_PV_Floating import RE_PV_Floating_Asset
from .Nuclear import Nuclear_Asset 
from .RE_Compiled import RE_Compiled_Asset
from .EL_to_PT import EL_to_PT_Asset
from .EL_to_GT import EL_to_GT_Asset
from .Diesel_Storage import Diesel_Storage_Asset
from .Gasoline_Storage import Gasoline_Storage_Asset
from .Diesel_Transport import Diesel_Transport_Asset
from .Gasoline_Transport import Gasoline_Transport_Asset
from .Gasoline_Production import Gasoline_Production_Asset
from .Diesel_Production import Diesel_Production_Asset




ASSET_DICT = {EL_Demand_Asset.asset_name: EL_Demand_Asset,
              HTH_Demand_Asset.asset_name: HTH_Demand_Asset,
              CG_Asset.asset_name: CG_Asset,
              EL_to_HTH_Asset.asset_name: EL_to_HTH_Asset,
              RE_Asset.asset_name: RE_Asset,
              BESS_Asset.asset_name: BESS_Asset,
              EL_to_NH3_Asset.asset_name: EL_to_NH3_Asset,
              NH3_to_EL_Asset.asset_name: NH3_to_EL_Asset,
              NH3_Storage_Asset.asset_name: NH3_Storage_Asset,
              NH3_to_HTH_Asset.asset_name: NH3_to_HTH_Asset,
              EL_Transport_Asset.asset_name: EL_Transport_Asset,
              NH3_Transport_Asset.asset_name: NH3_Transport_Asset,
              RE_PV_Asset.asset_name: RE_PV_Asset,
              RE_WIND_Asset.asset_name: RE_WIND_Asset,
              RE_max_Asset.asset_name: RE_max_Asset,
              EL_Demand_UM_Asset.asset_name: EL_Demand_UM_Asset,
              EL_Demand_Constant_Asset.asset_name: EL_Demand_Constant_Asset,
              RE_PV_Constant_Asset.asset_name: RE_PV_Constant_Asset,
              RE_WIND_Constant_Asset.asset_name: RE_WIND_Constant_Asset,
              CO2_Budget_Asset.asset_name: CO2_Budget_Asset,
              PP_CO2_Asset.asset_name: PP_CO2_Asset,
              RE_PV_Openfield_Lim_Asset.asset_name: RE_PV_Openfield_Lim_Asset,
              RE_PV_Rooftop_Lim_Asset.asset_name: RE_PV_Rooftop_Lim_Asset,
              RE_WIND_Onshore_Lim_Asset.asset_name: RE_WIND_Onshore_Lim_Asset,
              RE_WIND_Offshore_Lim_Asset.asset_name: RE_WIND_Offshore_Lim_Asset,
              PP_NGS_CCGT_CO2_Asset.asset_name: PP_NGS_CCGT_CO2_Asset,
              PP_NGS_SCGT_CO2_Asset.asset_name: PP_NGS_SCGT_CO2_Asset,
              PP_COAL_CO2_Asset.asset_name: PP_COAL_CO2_Asset,
              FF_to_HTH_Asset.asset_name: FF_to_HTH_Asset,
              H2_Storage_Asset.asset_name: H2_Storage_Asset,
              H2_to_EL_Asset.asset_name: H2_to_EL_Asset,
              NG_Storage_Asset.asset_name: NG_Storage_Asset,
              EL_to_H2_Asset.asset_name: EL_to_H2_Asset,
              NG_Transport_Asset.asset_name: NG_Transport_Asset,
              NG_to_EL_Asset.asset_name: NG_to_EL_Asset,
              SW_to_EL_Asset.asset_name: SW_to_EL_Asset, 
              EL_to_LTH_Asset.asset_name: EL_to_LTH_Asset,
              EL_to_Cooling_Asset.asset_name: EL_to_Cooling_Asset,
              Biofuel_to_EL_Asset.asset_name: Biofuel_to_EL_Asset,
              LTH_Demand_Asset.asset_name: LTH_Demand_Asset, 
              Cooling_Demand_Asset.asset_name: Cooling_Demand_Asset,
              PT_Demand_Asset.asset_name: PT_Demand_Asset, 
              GT_Demand_Asset.asset_name: GT_Demand_Asset,
              Gasoline_to_PT_Asset.asset_name: Gasoline_to_PT_Asset,
              Gasoline_to_GT_Asset.asset_name: Gasoline_to_GT_Asset,
              Diesel_to_PT_Asset.asset_name: Diesel_to_PT_Asset,
              Diesel_to_GT_Asset.asset_name: Diesel_to_GT_Asset,
              RE_PV_Floating_Asset.asset_name: RE_PV_Floating_Asset,
              Nuclear_Asset.asset_name: Nuclear_Asset,
              RE_Compiled_Asset.asset_name: RE_Compiled_Asset,
              Diesel_Storage_Asset.asset_name: Diesel_Storage_Asset,
              Gasoline_Storage_Asset.asset_name: Gasoline_Storage_Asset,
              Diesel_Transport_Asset.asset_name: Diesel_Transport_Asset,
              Gasoline_Transport_Asset.asset_name: Gasoline_Transport_Asset,
              EL_to_PT_Asset.asset_name:EL_to_PT_Asset,
              EL_to_GT_Asset.asset_name:EL_to_GT_Asset,
              Gasoline_Production_Asset.asset_name: Gasoline_Production_Asset,
              Diesel_Production_Asset.asset_name: Diesel_Production_Asset
              }
