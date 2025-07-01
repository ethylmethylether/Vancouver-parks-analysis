# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 19:18:56 2025

@author: Uzair
"""

# Libraries
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import contextily as ctx
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# Font Style
plt.rcParams['font.family'] = 'Times New Roman'

# Reading files
parks = gpd.read_file('parks.geojson')
neighborhood = gpd.read_file('local-area-boundary.geojson')
parks_boundary = gpd.read_file('parks-polygon-representation.geojson')

# Convert to Web Mercator (EPSG:3857)
parks_merc = parks.to_crs(epsg=3857)
neighborhood_merc = neighborhood.to_crs(epsg=3857)
parks_boundary_merc = parks_boundary.to_crs(epsg=3857)

# Top 10 largest parks
top10parks = parks_merc.sort_values(by='hectare', ascending=False).head(10)
top10parks_merc = top10parks.to_crs(epsg=3857)

# Buffer based on park area
top10buffered = top10parks.copy()
top10buffered['buffer_radius'] = np.sqrt((top10buffered['hectare'] * 10000) / np.pi)
top10buffered['geometry'] = top10buffered.geometry.buffer(top10buffered['buffer_radius'])

# Parks per neighborhood
parks_in_neighborhood = gpd.sjoin(parks, neighborhood, how='left', predicate='within')
park_counts = parks_in_neighborhood['name_right'].value_counts().sort_values(ascending=False)

# ------------------- MAP -------------------
fig, ax = plt.subplots(figsize=(12, 12))

# All parks
parks_merc.plot(ax=ax, color='seagreen', markersize=15, alpha=0.8, label='All Parks')

# Park boundaries
parks_boundary_merc.plot(ax=ax, facecolor='none', edgecolor='darkgreen', alpha=0.8)

# Top 10 parks
top10parks.plot(ax=ax, color='darkolivegreen', markersize=70, label='Top 10 Parks')

# Buffers
top10buffered.plot(ax=ax, color='green', alpha=0.3)

# Neighborhood boundaries
neighborhood_merc.plot(ax=ax, facecolor='none', edgecolor='black', alpha=0.5, linewidth=1)

# Legend
red_circle = Line2D([0], [0], marker='o', color='w', label='All Parks', markerfacecolor='seagreen', markersize=10)
green_circle = Line2D([0], [0], marker='o', color='w', label='Top 10 Parks by Size', markerfacecolor='darkolivegreen', markersize=10)
buffer_patch = mpatches.Patch(color='green', alpha=0.3, label='Circular Buffer Area')
neighborhood_patch = mpatches.Patch(color='black', label='Neighborhood Boundary')
park_patch = mpatches.Patch(color='darkgreen', label='Park Boundary')

plt.legend(handles=[red_circle, green_circle, buffer_patch, neighborhood_patch, park_patch])

# Basemap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13)

plt.title('Top 10 Parks by Size, Buffers, Neighborhoods, and Park Boundaries')
plt.axis('off')
plt.savefig('vancouver_parks_map.png', dpi=300, bbox_inches='tight')
plt.show()

# ------------------- BAR CHART 1 -------------------
top10buffered_sorted = top10buffered.sort_values(by='buffer_radius', ascending=False)
plt.figure(figsize=(12, 6))
plt.bar(top10buffered_sorted['name'], top10buffered_sorted['buffer_radius'], color='green', edgecolor='black')
plt.xticks(rotation=45, ha='right', color='black')
plt.xlabel('Park Name', color='black')
plt.ylabel('Buffer Radius (meters)', color='black')
plt.title('Top 10 Parks by Buffer Radius', color='black')
plt.tight_layout()
plt.savefig('top10_parks_buffer_radius.png', dpi=300, bbox_inches='tight')
plt.show()

# ------------------- BAR CHART 2 -------------------
top10neighborhood = park_counts.head(10)
plt.figure(figsize=(12, 6))
plt.bar(top10neighborhood.index, top10neighborhood.values, color='grey', edgecolor='black')
plt.xticks(rotation=45, ha='right', color='black')
plt.xlabel('Neighborhood', color='black')
plt.ylabel('Number of Parks', color='black')
plt.title('Top 10 Neighborhoods by Number of Parks', color='black')
plt.tight_layout()
plt.savefig('top10_neighborhood_parks.png', dpi=300, bbox_inches='tight')
plt.show()


