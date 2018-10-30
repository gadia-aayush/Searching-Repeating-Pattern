## README- Searching-Repeating-Pattern


### **BRIEF DESCRIPTION:**

  -	Basically we have datasets containing Timestamp & corresponding Energy Values. On generating the Visual Plot of the dataset with Timestamp on the X Axis & Energy Values on the Y Axis we get a Pattern. Our goal was to select any 2 particular Timestamp viz in the dataset, between these Timestamp's we have a Pattern enclosed and the Script will basically search for all the Timestamp Range which encloses similar pattern (any Timestamp Range will consist of 2 values: starting timestamp & ending timestamp).

  -	The Script also computes the Accuracy percentage of each Possible Timestamp Range, with each Timestamp Range enclosing a pattern similar to the selected one. Lets say for a particular Timestamp Range, the accuracy percentage for the pattern enclosed is 65%, then this actually means that the pattern is 65% similar to the pattern generated by selected Timestamp Range which was entered by user.

  -	**The Script tells about the following:**    
		      1.  **Accuracy Insights** ::  it represents the Mean , Upper Quartile & Median of Accuracy Values.  
		      2.  **Top 5 Accuracies**  ::  it represents the Top 5 Accuracy Percentages among all the Accuracy values along with their respective Timestamp Range.    
		      3.  **Average Value**     ::  it represents basically the Average. Top 5 Accuracies has several timestamp's ranges and within each range their are timestamp's at which value is recorded; so basically we are computing the average of the recorded values at each timestamp of different timestamp's ranges which are coming in the Top 5 Accuracies.     
		      4.  **All Accuracies**    ::  it represents All the Unique Accuracy Values sorted in Descending Order with each Unique Accuracy representing all the Timestamp Range where the same percentage of Accuracy exists.  
          
 
***NOTE :: It may happen that one particular accuracy percentage exists in more than 1 particular Timestamp Range.***  

***NOTE:: All the above Outputs are passed by the Script in JSON.***  


-------------------------------------------------------------------------------------------------------------------

### **PREREQUISITES:**


  - written for LINUX Server.
  - written in  Python 3.6 .
  - supporting packages required- pandas, numpy, statistics, json & sys. 


-------------------------------------------------------------------------------------------------------------------


### **CLIENT-END FULFILMENTS:**

> The below format must be followed for the successful running of the script:  

  1. `File Path ::  
     - it must be a CSV File Path.    
     - `it must be passed in the second argument of sys.argv.`    
					  
