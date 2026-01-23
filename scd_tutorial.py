# scd
# a table stores discriptive columns about a customer, but customers data change over time
# 
# scd1 - use these when you dont care of old values 
# steps 
# 1.identify overwrite columns - you decidde which columns should always be updated('email,phone')
# 2.detect existing customers - a customer is existing if their custoemerid is already in master.
# 3.update only the existing customers - if exists update, no new row is created.
# 4.insert new customers - if customerid in update but not in master. 

# scd2 - maintain full history
# keep old row, create new row for the new value
# example('address')

# steps
# 1.pick history tracked columns 
# 2.always compare against the current row  - if the customer has multiple records, his most recent one needs to be update.
# 3.detect address change
# 4.keep old row , set currentflag = 0
# 5.insert the new version row- same customerid, new address , version = old_version + 1 , currentflag = 1
# 6.insert brand new customer - if doesnt exist insert new - version = 1 , currentflag = 1


# set index 
