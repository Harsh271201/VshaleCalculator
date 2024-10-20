import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyQt5 import QtCore
import typing
class VshaleCalculator(QtCore.QObject):
    vshale_gr_array = QtCore.pyqtSignal(object)
    vshale_phi_array = QtCore.pyqtSignal(object)
    def __init__(self,data : pd.DataFrame,selected_column_DEPTH : str = None):
        super().__init__()
        if not selected_column_DEPTH:
            self.selected_column_DEPTH = list(data.columns)[0] 
        else:
            self.selected_column_DEPTH = selected_column_DEPTH
        self.data = data
        self.depth_boundaries_gr=np.array([np.min(data[selected_column_DEPTH].values),np.max(data[selected_column_DEPTH].values)],dtype='f8')
        self.sand_shale_lines=[[5,95]]
        self.age_correction=['Linear']
        self.depth_boundaries_phi=np.array([np.min(data[selected_column_DEPTH].values),np.max(data[selected_column_DEPTH].values)],dtype='f8')
        
    def vshale_gr(self,colunm_gr : str):     
        """ Calculating the Vsh using the Gamma ray 
        Args:
            colunm_gr(str): Column name for the Gamma ray colunm
        """

        if self.age_correction==None:
            self.age_correction = ['Linear' for _ in range(len(self.sand_shale_lines))]
        self.colunm_gr=colunm_gr
        self.gammaray=self.data[colunm_gr]
        Vshale=np.full(len(self.gammaray), np.nan)
        if len(self.depth_boundaries_gr)-1==len(self.sand_shale_lines):
        
            for i in range(len(self.depth_boundaries_gr)-1):
                condition=(self.depth_boundaries_gr[i]<=self.data[self.selected_column_DEPTH]) & (self.depth_boundaries_gr[i+1]>=self.data[self.selected_column_DEPTH])
                pmax = np.percentile(self.gammaray[condition],self.sand_shale_lines[i][1])
                pmin = np.percentile(self.gammaray[condition],self.sand_shale_lines[i][0])
                igr = (self.gammaray[condition] - pmin) / (pmax - pmin)
                igr = (self.gammaray[condition] - pmin) / (pmax - pmin)
                if self.age_correction[i]=='Linear':
                    vsh=igr
                if self.age_correction[i]=='Larinor_older':
                    vsh=0.33 * (2 ** (2 * igr) - 1)
                if self.age_correction[i]=='Larinor_tertiary':
                    vsh=0.083 * (2 ** (3.7 * igr) - 1)
                if self.age_correction[i]=='Clavier':
                    vsh=1.7 - (3.38 - (igr + 0.7) ** 2) ** 0.5
                if self.age_correction[i]=='Stieber':
                    vsh = igr/(3-2*igr)
                Vshale[condition]=vsh

            self.data['Vsh_GR'] = Vshale
        self.vshale_gr_array.emit(Vshale)
        return Vshale
    
    def zone_position_gr(self,depth : float) -> int:                
        """ Gives the position of the depth point,in which zone it is.(for the Vshale using the Gamma ray)
    
        Args:
            depth (float): depth point 

        Returns:
            int: zone position 
        """        
        index=[]
        if depth not in self.depth_boundaries_gr:
            for dep in self.depth_boundaries_gr:
                if dep <= depth:
                    continue
                else:
                    index.append(np.where(self.depth_boundaries_gr==dep)[0][0])
                    break
        zone_position_gr=index[0]
        return zone_position_gr
    
        
    def shale_sand_edit(self,depth , sand_shale_perc : typing.List[float]):        
        """ Editing the sand line and shale line.(for the Vshale using the Gamma ray)
        Args:
            depth (str): depth point from the zone for which sand and shale line has to be changed.
            sand_shale_perc (list[float,float]): list with the two element which is basically percentile values for the sand and shale lines.
        """
        
        zone_position_gr=self.zone_position_gr(depth)
        self.sand_shale_lines[zone_position_gr-1]=sand_shale_perc

    def age_corretion_edit(self,depth : float , correction : str):
      
        """ Editiing the age correction for zone in which current depth point is lying.(for the Vshale using the Gamma ray)
        Args:
            depth (float): depth point 
            correction (str): correction to be applied on the that zone  ('Linear','Larinor_older','Larinor_tertiary','Clavier','Stieber')
        """        
        zone_position_gr=self.zone_position_gr(depth)
        self.age_correction[zone_position_gr-1]=correction
        
    def adding_zone_gr(self,depth):       
        """Adding the zone.(for the Vshale using the Gamma ray)
        Args:
            data (DepthPointArgs): Data class containing the input arguments for the adding the zones.
        
        Field description of the data.
            - depth (float): Depth point which will be the boundary of the new zone.
        """        

        if depth not in self.depth_boundaries_gr:
            from copy import copy
            self.depth_boundaries_gr=np.sort(np.append(self.depth_boundaries_gr,depth))
            index=np.where(self.depth_boundaries_gr==depth)[0][0]
            self.age_correction.insert(index,copy(self.age_correction[index-1]))
            self.sand_shale_lines.insert(index,copy(self.sand_shale_lines[index-1]))

    def deleting_zone_gr(self,depth):
        """ Deleting the zone 
        Args:
            data (DepthPointArgs): Data class containing the input arguments for the adding the zones.
        
        Field description of the data.
            - depth (float): depth point from the zone to be deleted.
        """ 
      
        if self.zone_position_gr(depth) != len(self.depth_boundaries_gr)-1:
            zone_position_gr=self.zone_position_gr(depth)
            zone_end=self.depth_boundaries_gr[zone_position_gr]
            self.depth_boundaries_gr = np.delete(self.depth_boundaries_gr, np.where(self.depth_boundaries_gr == zone_end))
            self.age_correction.pop(zone_position_gr-1)
            self.sand_shale_lines.pop(zone_position_gr-1)
    
    def vsh_phi(self,selected_column_phi1 : str ,phi1sh : typing.Union[int,float] ,selected_column_phi2 : str ,phi2sh :typing.Union[int,float], phi_type = ['V/V','V/V']):      
        """ Calculating the shale volume using the porosities
        Args:
            selected_column_phi1 (str): colunm for the density porosity 
            phi1sh (float): Density porosity of the shale 
            selected_column_phi2 (str): column for the Neutron porosity
            phi2sh (float): Neutron porosity
            phi_type (list[str], optional): type of the porosity you are entering (V/V or V/V%).Defaults to ['V/V','V/V'].
        """                    
        self.phi1sh=phi1sh
        self.phi2sh=phi2sh
        self.column_phi1=selected_column_phi1
        self.column_phi2=selected_column_phi2
        phi1=self.data[selected_column_phi1].values
        phi2=self.data[selected_column_phi2].values
        if len(phi_type)==2:
            if phi_type[0]=='V/V':
                self.phi1=phi1
            elif phi_type[0]=='V/V%':
                self.phi1=phi1/100
                #self.data[selected_column_ph1].values=phi1
            if phi_type[1]=='V/V':
                self.phi2=phi2
            elif phi_type[1]=='V/V%':
                self.phi2=phi2/100
                #self.data[selected_column_ph1].values=phi1
            Vshale =(self.phi1-self.phi2)/(self.phi1sh-self.phi2sh)
            
            self.vshale_phi_array.emit(Vshale)

            self.data['Vsh_phi'] = Vshale
    






