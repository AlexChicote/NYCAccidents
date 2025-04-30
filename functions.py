import matplotlib.pyplot as plt
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
    