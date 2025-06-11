

import playsound


import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd



plt.rcParams['axes.grid'] = True


def viz_per_time_period(df, time_period, period_list):
#weekdays_list=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    period_groupby=df.groupby(time_period)[['collision_id','number_of_persons_injured','number_of_persons_killed']].\
                        agg({'collision_id':'count',
                             'number_of_persons_injured':'sum',
                             'number_of_persons_killed':'sum'
                             
                                                                        }).reindex(period_list)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4))
    ax1.plot(period_groupby.index, period_groupby.iloc[:,0],c='blue')
    ax1.set_title(f'Collisions per {time_period}')
    
    ax2.plot(period_groupby.index, period_groupby.iloc[:,1],color='#F29775')
    ax2.set_title(f'Injured per {time_period}')
    
    ax3.plot(period_groupby.index, period_groupby.iloc[:,2],color='#F26C8A')
    ax3.set_title(f'Deaths per {time_period}')
    
    #Let's do it per collision:
    period_by_collision=(period_groupby*(100/df.shape[0])).iloc[:,1:]

    fig, ax4 = plt.subplots(figsize=(14, 4))
    # Plot the first chart
    ax4.plot(period_by_collision.index, period_by_collision.iloc[:,0], color='#F29775',label='Injured per collision',linewidth=3)
    ax4.set_xlabel(time_period)
    ax4.set_ylabel('Injured per Collision')
    ax4.tick_params('y')
    # Create a second axes that shares the same x-axis
    ax5 = ax4.twinx()
    
    # Plot the second chart
    ax5.plot(period_by_collision.index, period_by_collision.iloc[:,1],color='#F26C8A',label='Deaths per collision',linewidth=3)
    ax5.set_ylabel('Deaths per Collision' )
    ax5.tick_params('y')
    
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    
    # Combine the handles and labels
    handles = handles1 + handles2
    labels = labels1 + labels2
    
    # Create a single legend for both axes
    plt.legend(handles, labels)
    
    
    # Show the plot
    plt.title('Combined Plot')
    
    plt.show()


def grouping_by_time_period(df, time_period, period_list):
#weekdays_list=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    period_groupby=df.groupby(time_period)[['collision_id','number_of_persons_injured','number_of_persons_killed']].\
                        agg({'collision_id':'count',
                             'number_of_persons_injured':'sum',
                             'number_of_persons_killed':'sum'
                             
                                                                        }).reindex(period_list)
    period_groupby.columns=['num_collisions','num_victims','num_killed']
    return period_groupby


def play_done_message():
    playsound.playsound("./data/JobDone.m4a")


def adding_shp_boro(df,path='./data/shapefileGeoPandasBorough/NYC_Borough_Boundary.shp'):
    """Add info about boroughs to dataframe from a shapefile

    Input: dataframe to add the BoroName
    Returns: geodataframe with new fileds
    """
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude,df.latitude,crs='EPSG:4326'))
    shapefile_=gpd.read_file(path).to_crs(gdf.crs)
    gdf=gpd.sjoin(gdf,shapefile_[['geometry','BoroName']],how='left',predicate='within',rsuffix='boro')
    gdf.loc[gdf['BoroName'].isnull(),['BoroName']]='Highways and Bridges'
    gdf=gdf.drop_duplicates('collision_id')
    df_incremented = pd.DataFrame(gdf.drop(columns='geometry'))
    return df_incremented

def adding_shp_hood(df,path='./data/shapefileGeoPandasNeighborhood/NYC_Neighborhood_Tabulation_Areas_2020.shp'):
    """Add info about heighborhoods to dataframe from a shapefile

    Input: dataframe to add the NTAName
    Returns: geodataframe with new fileds
    """
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude,df.latitude,crs='EPSG:4326'))
    shapefile_=gpd.read_file(path).to_crs(gdf.crs)
    gdf=gpd.sjoin(gdf,shapefile_[['geometry','NTAName']],how='left',predicate='within',rsuffix='hood')
    gdf = gdf.rename(columns={'NTAName': 'hood'})
    gdf.loc[(gdf['hood'].isnull())&(gdf.index_boro.notnull()),['hood']]='added: West Village'
    gdf=gdf.drop_duplicates('collision_id')
    df_incremented = pd.DataFrame(gdf.drop(columns='geometry'))
    return df_incremented   

def adding_shp_zip(df,path='./data/ZipCodeAreas/geo_export_143e2047-e7c2-49a7-a5d2-c7fa441c7ef5.shp'):
    """Add info about zip_code to dataframe from a shapefile

    Input: dataframe to add the modzcta
    Returns: geodataframe with new fields
    """
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude,df.latitude,crs='EPSG:4326'))
    shapefile_=gpd.read_file(path).to_crs(gdf.crs)
    gdf=gpd.sjoin(gdf,shapefile_[['geometry','modzcta']],how='left',predicate='within',rsuffix='zip')
    gdf = gdf.rename(columns={'modzcta': 'zip_code_shp'})
    gdf.loc[(gdf.index_zip.isnull()) &(gdf.index_hood.notnull()),['zip_code_shp']]='weirdo'
    gdf=gdf.drop_duplicates('collision_id')
    df_incremented = pd.DataFrame(gdf.drop(columns='geometry'))
    return df_incremented

def adding_shp_st(df,path='./data/shapefiles/DCM_StreetCenterLine.shp'):
    """Add info about streets to dataframe from a shapefile

    Input: dataframe to add the street_NM and Route_Type whiole keeping only the first one
    Returns: geodataframe with new fields
    """
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude,df.latitude,crs='32618'))
    shapefile_=gpd.read_file(path).to_crs(gdf.crs)
    gdf=gpd.sjoin_nearest(gdf,shapefile_[['geometry','Street_NM','Route_Type']],how='left',distance_col='distances',rsuffix='street')
    gdf = gdf.rename(columns={'Street_NM': 'street'})
    gdf=gdf.drop_duplicates('collision_id')
    df_incremented = pd.DataFrame(gdf.drop(columns='geometry'))
    return df_incremented

    