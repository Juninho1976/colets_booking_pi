# colets_booking_pi
Using playwright to help me book classes on Colets website... !


Requirements:
- playwright
- colets booking account
- a vm or always on computer (recommmend a pi or there are free vms on oci)

Note: you need to create a .env file which has your colets credentials 

use cron or any scheduler to run this at 6am.

code is very limited... website is super
flakey especially the wait list
flow but it will let you book one class (have to get the name spot on for the env file !) .


todo
- add some resilience
- move the instance number to .env to allow when miltiple classes exist for a day for the same name it picks the correct instance
- better state handling
- check to see if a class was
- booked!
- 
