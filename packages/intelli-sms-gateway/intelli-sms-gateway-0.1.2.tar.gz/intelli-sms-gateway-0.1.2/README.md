# Overview

1. Authenticate

2. Assign CSV file path to variable CSV for a bulk sms

3. Call either method for sending bulk or single SMSs


# 1. Authentication




**Instantiate Client class byt passing the parameters email and password in that order**
`from intelli_sms_gateway.client import Client`
`# Import the client class from the client module`
` `
` `
`client = Client('foo@foo.com', 'password')`

*Should the client be authenticated, this instantiation will return a property of value True. The reverse is true.*



# 2. Getting Details On a Bulk SMS from a CSV



*Define a variable, assign to it the path of the csv file you want to use*
**Make sure the first column in the CSV is named 'numbers' or the program will return errors. Phone numbers must be in the format 263777534224**


# 3. Sending the messages



## Bulk SMSes




*Call the single SMS method of the client instance and pass the required parameters namely: message, csv, title*
**The CSV that is being passed is the variable that contains the path to the CSV. Should the path be incorrect, errors will be raised**

`client.send_bulk_sms('Please attend the meeting at 1pm', csv_variable, 'Meeting announcament')`



## Single SMSes






*Call the single SMS method of the client instance and pass the required parameters namely: message, receiver, title*
**Phone numbers must be in the format 263777534224**

`client.send_single_sms('Please attend the meeting at 1pm', '263777534224', 'Meeting announcament')`


#  *If your credentials are correct, your messages will not be sent*
