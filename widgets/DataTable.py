from PyQt5 import QtWidgets, QtCore, QtGui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import sys

class DataFrameTableModel(QtCore.QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df
        self.colormaps = self._generate_colormaps()

    def _generate_colormaps(self,random = False):
        """
        Generate random continuous color maps for each numeric column based on their min and max values.
        """
        continuous_colormaps = [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Blues', 'Greens', 'Reds', 'Purples', 'Oranges'
        ]
        
        colormaps = {}
        for column in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[column]):
                col_min = np.nanmin(self.df[column])
                col_max = np.nanmax(self.df[column])
                if random:
                    cmap_name = np.random.choice(continuous_colormaps)
                else:
                    cmap_name = 'viridis'
                cmap = plt.get_cmap(cmap_name)
                colormaps[column] = cmap
                colormaps[column].norm = Normalize(vmin=col_min, vmax=col_max) 
            else:
                colormaps[column] = None  
        return colormaps

    def rowCount(self, parent=None):
        return len(self.df)

    def columnCount(self, parent=None):
        return len(self.df.columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        row = index.row()
        col = index.column()

        value = self.df.iloc[row, col]

        if role == QtCore.Qt.DisplayRole:
            if pd.isna(value):
                return "NaN"
            return str(value)

        if role == QtCore.Qt.BackgroundRole:
            if pd.isna(value):
                return QtGui.QColor(0, 0, 0, 200) 
            else:
                column_name = self.df.columns[col]
                cmap = self.colormaps.get(column_name)

                if cmap is not None:
                    norm_value = cmap.norm(value)
                    rgba = cmap(norm_value)  
                    r, g, b, a = [int(x * 255) for x in rgba]
                    return QtGui.QColor(r, g, b, int(a * 0.2))  # Reduce alpha for visualization

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

        return QtCore.QVariant()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.df.columns[section]
            elif orientation == QtCore.Qt.Vertical:
                return str(section)
        return QtCore.QVariant()

