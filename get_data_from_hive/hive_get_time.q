#get the number of check-in data every minute in NYC, Chicago, Los Angeles, China and USA
#we specify each region with four dots which contains longitude and latitude

#How to run:
#chmod +x hive_get_time
#./hive_get_time
  
#Global
hive -e "select hour(time), minute(time), count(*) as cnt from check_in group by hour(time), minute(time);" > interval_min.tsv

#NYC
hive -e "select hour(time), minute(time), count(*) as cnt from (select * from check_in where longitude >= -74.259090 and longitude <= -73.700272 and latitude >= 40.477399 and latitude <= 40.917577) ll group by hour(time), minute(time);" > interval_nyc.tsv

#Chicago 
hive -e "select hour(time), minute(time), count(*) as cnt from (select * from check_in where longitude >= -87.847512 and longitude <= -87.524102 and latitude >= 41.646724 and latitude <= 42.020197) ll group by hour(time), minute(time);" > interval_chi.tsv

#Los Angeles
hive -e "select hour(time), minute(time), count(*) as cnt from (select * from check_in where longitude >= -118.660298 and longitude <= -118.161794 and latitude >= 33.700624 and latitude <= 34.334637) ll group by hour(time), minute(time);" > interval_la.tsv

#China
hive -e "select hour(time), minute(time), count(*) as cnt from (select * from check_in where longitude >= 73.55 and longitude <= 135.083333 and latitude >= 3.85 and latitude <= 53.55) ll group by hour(time), minute(time);" > interval_chn.tsv

#USA
hive -e "select hour(time), minute(time), count(*) as cnt from (select * from check_in where longitude >= -124.626080 and longitude <= -62.361014 and latitude >= 18.005611 and latitude <= 48.987386) ll group by hour(time), minute(time);" > interval_nyc.tsv


