#!/usr/bin/env python3

#------------------------ VERSION 2 -------------------------
#----------------- [Type of Output Changed] -----------------


#------------------------------------------------------------
#----------------SEARCHING REPEATING PATTERN-----------------
#VERSION        : by entering Timestamp 
#SUB- VERSION   : more than 1 line, in b/w points entered (2 points).
#------------------------------------------------------------


#Importing Libraries
import csv
import pandas as pd
from statistics import *
import numpy as np
from datetime import *
from os import sys
import json

output_data= {}


#File Input 
try:
    file_path=str(sys.argv[1])
    df=pd.read_csv(file_path)
    recorded_data=df.iloc[0:,1].tolist()
    df.iloc[0:,0]= pd.to_datetime(df.iloc[0:,0], dayfirst=True)
    timestamp= df.iloc[0:,0].dt.strftime("%d-%m-%Y %H:%M").tolist()
    #timestamp= df.iloc[0:,0].tolist()  


    #Timestamp Input
    try:  
        #JSON Input Process
        input_data= sys.argv[2]
        input_json= json.loads(input_data)            
        timestamp_start= str(input_json["start_timestamp"])
        timestamp_end= str(input_json["end_timestamp"])
        
        #Timestamp Dictionary
        timestamp_dict={}
        number=0
        for time in timestamp:
            timestamp_dict[time]=number
            number+=1    
            
        #Processing All Input Parameters
        graph_points=(timestamp_dict[timestamp_end]-timestamp_dict[timestamp_start])+1    
        if(graph_points > 1):
            graph_x=[]
            graph_y=[]
            for x in range(timestamp_dict[timestamp_start],timestamp_dict[timestamp_end]+1):
                graph_x.append(x)
                graph_y.append(recorded_data[x])
            graph_slope=[]
            for i in range(len(graph_x)-1):
                graph_slope.append(graph_y[i+1]-graph_y[i])
            
            # Calculating no. of entries in a Day
            x= datetime.strptime(timestamp[0],'%d-%m-%Y %H:%M')
            y= datetime.strptime(timestamp[1],'%d-%m-%Y %H:%M')
            day_entries= int((3600/(y-x).total_seconds())*24) #1 day selecting
            
            
            #Graph Type Enter   
            try:
                graph_type= int(input_json["graph_type"])            
                
                #------1. for Continuous Output
                #------2. for Discontinuous Output
                #------3. for Average of Timestamp's Output
                
                #Point Reference::
                if (graph_type == 1):
                    test_point=[]
                    test_point.append(graph_x)
                    for i in range(len(recorded_data)-(graph_points-1)):
                        sub_point=[]
                        for j in range(graph_points):
                            sub_point.append(i+j)    
                        test_point.append(sub_point)         
                        
                elif (graph_type == 2):
                    test_point=[]
                    test_point.append(graph_x)
                    for i in range(0,timestamp_dict[timestamp_start]):
                        sub_point=[]
                        for j in range(graph_points):
                            sub_point.append(i+j)  
                        if(sub_point[graph_points-1] < test_point[0][0]):    
                            test_point.append(sub_point)    
                        else:
                            continue
                        
                    for i in range(timestamp_dict[timestamp_end]+1,len(df)):
                        sub_point=[]
                        for j in range(graph_points):
                            sub_point.append(i+j)    
                        if(sub_point[graph_points-1] < (len(df)-1)):          
                            test_point.append(sub_point) 
                    
                elif (graph_type == 3):
                    test_point= []
                    test_point.append(graph_x)
                    
                    # backward propagation
                    ref= round(graph_points/day_entries)+1
                    start_time= timestamp_dict[timestamp_start] - ref*day_entries
                    end_time= timestamp_dict[timestamp_end] - ref*day_entries
                    if (start_time >= 0):
                        l1= []
                        for point in range(start_time, end_time+1):
                            l1.append(point)
                        test_point.append(l1)    
                    for i in range(len(df)):
                        sub_point= []
                        ref= round(graph_points/day_entries) 
                        if (ref == 0):
                            ref= 1
                            start_time-= ref*day_entries
                            end_time-= ref*day_entries
                            if (start_time >= 0):
                                for j in range(start_time, end_time+1):
                                    sub_point.append(j)
                                test_point.append(sub_point)
                            else:
                                break
                        else:
                            ref= round(graph_points/day_entries)
                            start_time-= ref*day_entries
                            end_time-= ref*day_entries
                            if (start_time >= 0):
                                for j in range(start_time, end_time+1):
                                    sub_point.append(j)
                                test_point.append(sub_point)            
                            else:
                                break
                    
                    # forward propagation            
                    ref= round(graph_points/day_entries)+1
                    start_time= timestamp_dict[timestamp_start] + ref*day_entries
                    end_time= timestamp_dict[timestamp_end] + ref*day_entries
                    if (end_time < len(df)):
                        l1= []
                        for point in range(start_time, end_time+1):
                            l1.append(point)
                        test_point.append(l1)    
                    for i in range(len(df)):
                        sub_point= []
                        ref= round(graph_points/day_entries) 
                        if (ref == 0):
                            ref= 1
                            start_time+= ref*day_entries
                            end_time+= ref*day_entries
                            if (end_time < len(df)):
                                for j in range(start_time, end_time+1):
                                    sub_point.append(j)
                                test_point.append(sub_point)
                            else:
                                break
                        else:
                            ref= round(graph_points/day_entries)
                            start_time+= ref*day_entries
                            end_time+= ref*day_entries
                            if (end_time < len(df)):
                                for j in range(start_time, end_time+1):
                                    sub_point.append(j)
                                test_point.append(sub_point)            
                            else:
                                break
                    
                else:
                    output_data["status"]= "error"
                    output_data["message"]= "please choose the graph type by entering- 1, 2 or 3"
                    output_data["data"]= ""
                    output_data["code"]= 401               
                    
                # Slope Reference::
                test_slope= []
                test_slope.append(graph_slope)
                for i in range(1,len(test_point)):
                    sub_slope=[]
                    for j in range(0,graph_points-1):
                        sub_slope.append((recorded_data[test_point[i][j+1]])-(recorded_data[test_point[i][j]]))
                    test_slope.append(sub_slope)        
                    
                    
                #Slope & Point Error | Slope & Point Weightage         
                try:
                   slope_error= float(input_json["slope_error"])
                   point_error= float(input_json["point_error"])
                   slope_weightage= float(input_json["slope_weightage"])
                   point_weightage= float(input_json["point_weightage"])
                   if ((slope_error < 1.0) and (point_error < 1.0) and ((slope_weightage + point_weightage)==1)):
                       accuracy_dict={}
                       accuracy_record=[]                        
                   else:
                       slope_error=0.10
                       point_error=0.05
                       slope_weightage=0.50
                       point_weightage=0.50     
                       accuracy_dict={}
                       accuracy_record=[]     
                except: #Slope & Point Error | Slope & Point Weightage Value: Error Handling
                    slope_error=0.10
                    point_error=0.05
                    slope_weightage=0.50
                    point_weightage=0.50
                    accuracy_dict={}
                    accuracy_record=[]   

                for row in range(1,len(test_slope)):
                    if(test_point[row][0]!=graph_x[0]):
                        sum=0
                        for column in range(len(test_slope[0])):
                            score=0
                            slope_min=test_slope[0][column]*(1-slope_error)
                            slope_max=test_slope[0][column]*(1+slope_error)
                            start_min=recorded_data[test_point[0][column]]*(1-point_error)
                            start_max=recorded_data[test_point[0][column]]*(1+point_error)
                            end_min=recorded_data[test_point[0][column+1]]*(1-point_error)
                            end_max=recorded_data[test_point[0][column+1]]*(1+point_error)
                            
                            #Slope_Error Block
                            if((test_slope[0][column] > 0 and test_slope[row][column] < 0) or (test_slope[0][column] < 0 and test_slope[row][column] > 0)):
                                score+=0
                            elif ((slope_min <= test_slope[row][column] <= slope_max) or (slope_min >= test_slope[row][column] >= slope_max)):
                                score+= slope_weightage
                            else:
                                score+=0
                            
                            #Point_Error Block
                            if((start_min <= recorded_data[test_point[row][column]] <= start_max) and (end_min <= recorded_data[test_point[row][column+1]] <= end_max)):
                                score+= point_weightage
                            elif((start_min <= recorded_data[test_point[row][column]] <= start_max) or (end_min <= recorded_data[test_point[row][column+1]] <= end_max)):
                                score+=0
                            else:
                                score+=0
                            sum+=score
                        accuracy=sum*100/len(test_slope[0])
                        accuracy_record.append(round(accuracy,2))
                        accuracy_dict[row]=round(accuracy,2)
                        
                # Output Type Enter
                try:
                    output_type=  int(input_json["output_type"])
                
                    #------1. for Accuracy Insights
                    #------2. for Top 5 Accuracy
                    #------3. for All Accuracies
                
                    if (output_type== 1):
                        insights_dict= {}
                        insights_dict["median_of_accuracy_is"]= round(np.percentile(accuracy_record,50),2)
                        insights_dict["upper_quartile_of_accuracy_is"]= round(np.percentile(accuracy_record,75),2)
                        insights_dict["mean_of_accuracy_is"]= round(mean(accuracy_record),2)
                        final_output= {}
                        final_output["accuracy_insights"]= insights_dict
                        output_data["status"]= "success"
                        output_data["message"]= ""
                        output_data["data"]= final_output
                        output_data["code"]= 200                        
                        
                            
                    elif ((output_type== 2) and (graph_type!= 3)): #Here Average won't be computed
                        accuracy_final=[item for item in accuracy_record if item > np.percentile(accuracy_record,75)] #taking top 25 percentile accuracies
                        accuracy_unique=[]
                        for val in accuracy_final:
                            if val not in accuracy_unique:
                                accuracy_unique.append(val)
                        accuracy_unique.sort(reverse=True)   
                        accuracy_index=[]
                        for value in accuracy_unique:
                            ll=[]
                            for (k,v) in accuracy_dict.items():
                                if(value==v):
                                    ll.append(k)
                            accuracy_index.append(ll)     
                            
                        j=0
                        rough_ll2=[]
                        for index in accuracy_index:
                            rough_ll=[]
                            index.sort()
                            for point in index:
                               rough_dict={}
                               rough_dict["Accuracy % is: "]=accuracy_unique[j]
                               rough_dict["Starting Timestamp is: "]= timestamp[test_point[point][0]]
                               rough_dict["Ending Timestamp is: "]= timestamp[test_point[point][len(test_point[point])-1]]
                               rough_ll.append(rough_dict)
                            rough_ll2.append(rough_ll) 
                            j+=1
                        data={}
                        i=0
                        for value in accuracy_unique:
                            data[value]=rough_ll2[i]       
                            i+=1
                        
                        top_dict= {}
                        top_5= [val for val in accuracy_unique[:5]]
                        i=1
                        for value in top_5:
                            top_dict[value]= []
                            j=1
                            for record in data[value]:
                                target_array= np.array(recorded_data[timestamp_dict[record['Starting Timestamp is: ']]:timestamp_dict[record['Ending Timestamp is: ']]+1])
                                name= str(i) +"."+ str(j)
                                j+=1   
                                sub_dict= {}
                                sub_dict["s_no"]= name
                                sub_dict["starting_timestamp"]= record['Starting Timestamp is: ']
                                sub_dict["ending_timestamp"]= record['Ending Timestamp is: ']
                                sub_dict["accuracy_%"]= record['Accuracy % is: ']
                                top_dict[value].append(sub_dict)
                            i+=1   
                        final_output= {}
                        final_output["top_5_accuracy"]= top_dict
                        output_data["status"]= "success"
                        output_data["message"]= ""                            
                        output_data["data"]= final_output
                        output_data["code"]= 200                        
                        
                        
                    elif ((output_type== 2) and (graph_type== 3)): #Here Average will be computed 
                        accuracy_final=[item for item in accuracy_record if item > np.percentile(accuracy_record,75)] #taking top 25 percentile accuracies
                        accuracy_unique=[]
                        for val in accuracy_final:
                            if val not in accuracy_unique:
                                accuracy_unique.append(val)
                        accuracy_unique.sort(reverse=True)   
                        accuracy_index=[]
                        for value in accuracy_unique:
                            ll=[]
                            for (k,v) in accuracy_dict.items():
                                if(value==v):
                                    ll.append(k)
                            accuracy_index.append(ll)     
                            
                        j=0
                        rough_ll2=[]
                        for index in accuracy_index:
                            rough_ll=[]
                            index.sort()
                            for point in index:
                               rough_dict={}
                               rough_dict["Accuracy % is: "]=accuracy_unique[j]
                               rough_dict["Starting Timestamp is: "]= timestamp[test_point[point][0]]
                               rough_dict["Ending Timestamp is: "]= timestamp[test_point[point][len(test_point[point])-1]]
                               rough_ll.append(rough_dict)
                            rough_ll2.append(rough_ll) 
                            j+=1
                        data={}
                        i=0
                        for value in accuracy_unique:
                            data[value]=rough_ll2[i]       
                            i+=1
                            
                        avg_dict= {}
                        for time in timestamp[timestamp_dict[timestamp_start]:timestamp_dict[timestamp_end]+1]:
                            string= time
                            avg_dict[string.split(" ")[1]]=[]
                        
                        top_dict= {}
                        top_5= [val for val in accuracy_unique[:5]]
                        i=1
                        for value in top_5:
                            top_dict[value]= []
                            j=1
                            for record in data[value]:
                                target_array= np.array(recorded_data[timestamp_dict[record['Starting Timestamp is: ']]:timestamp_dict[record['Ending Timestamp is: ']]+1])
                                name= str(i) +"."+ str(j)
                                j+=1   
                                sub_dict= {}
                                sub_dict["s_no"]= name
                                sub_dict["starting_timestamp"]= record['Starting Timestamp is: ']
                                sub_dict["ending_timestamp"]= record['Ending Timestamp is: ']
                                sub_dict["accuracy_%"]= record['Accuracy % is: ']
                                top_dict[value].append(sub_dict)
                                
                                for dict_rec in timestamp[timestamp_dict[record['Starting Timestamp is: ']] : timestamp_dict[record['Ending Timestamp is: ']]+1]:
                                    dict_key= dict_rec.split(" ")[1]
                                    for key in avg_dict:
                                        if (key == dict_key):
                                            avg_dict[key].append(recorded_data[timestamp_dict[dict_rec]])
                                
                            i+=1                            
                                               
                        final_avg= []   
                        for key in avg_dict:
                            final_avg.append(mean(avg_dict[key]))                        
                        
                        final_output= {}
                        final_output["top_5_accuracy"]= top_dict
                        final_output["average_value"]= final_avg
                        #final_output.append(top_dict)
                        #final_output.append(final_avg)
                        output_data["status"]= "success"
                        output_data["message"]= ""                            
                        output_data["data"]= final_output
                        output_data["code"]= 200                                      
                        
                        
                    elif (output_type== 3):   
                        accuracy_final=[item for item in accuracy_record if item > np.percentile(accuracy_record,75)] #taking top 25 percentile accuracies
                        accuracy_unique=[]
                        for val in accuracy_final:
                            if val not in accuracy_unique:
                                accuracy_unique.append(val)
                        accuracy_unique.sort(reverse=True)   
                        accuracy_index=[]
                        for value in accuracy_unique:
                            ll=[]
                            for (k,v) in accuracy_dict.items():
                                if(value==v):
                                    ll.append(k)
                            accuracy_index.append(ll)     
                            
                        j=0
                        rough_ll2=[]
                        for index in accuracy_index:
                            rough_ll=[]
                            index.sort()
                            for point in index:
                               rough_dict={}
                               rough_dict["accuracy_%_is"]=accuracy_unique[j]
                               rough_dict["starting_timestamp_is"]= timestamp[test_point[point][0]]
                               rough_dict["ending_timestamp_is"]= timestamp[test_point[point][len(test_point[point])-1]]
                               rough_ll.append(rough_dict)
                            rough_ll2.append(rough_ll) 
                            j+=1
                        accuracies_dict={}
                        i=0
                        for value in accuracy_unique:
                            accuracies_dict[value]=rough_ll2[i]       
                            i+=1
                        final_output= {}  
                        final_output["all_accuracies"]= accuracies_dict                          
                        output_data["status"]= "success"
                        output_data["message"]= ""                            
                        output_data["data"]= final_output
                        output_data["code"]= 200                                  
                                             
                    
                    
                    else:   
                        output_data["status"]= "error"
                        output_data["message"]= "please choose the output type by entering- 1, 2 or 3"
                        output_data["data"]= ""
                        output_data["code"]= 401        
                        
                        
                except: #Output Type: Error Handling
                    output_data["status"]= "error"
                    output_data["message"]= "please choose the output type by entering- 1, 2 or 3"
                    output_data["data"]= ""
                    output_data["code"]= 401                                
                        
                        
            except: #Graph Type: Error Handling
                output_data["status"]= "error"
                output_data["message"]= "please choose the graph type by entering- 1, 2 or 3"
                output_data["data"]= ""
                output_data["code"]= 401
                
                
        else: #Timestamp Value: Error Handling         
            output_data["status"]= "error"
            output_data["message"]= "make sure that the end timestamp is greater than the start timestamp "
            output_data["data"]= ""
            output_data["code"]= 401
                    
        
    except: #Timestamp Input: Error Handling
        output_data["status"]= "error"
        output_data["message"]= "please enter the timestamp in the format: 01-01-2018 01:05 or any/ both of the start & end timestamp does not exist in the dataset "
        output_data["data"]= ""
        output_data["code"]= 401
                
        
except: #File Input: Error Handling
    output_data["status"]= "error"
    output_data["message"]= "please provide the csv file path or check the file name entered"
    output_data["data"]= ""
    output_data["code"]= 401
    
output_json = json.dumps(output_data, ensure_ascii = 'False')
print(output_json)

#NOTE:: in JSON, the keys are always in double quotation.



 #-----------------------------
 #|| written by AAYUSH GADIA ||
 #-----------------------------