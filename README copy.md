# SES Automatic Email Service for CAST

## Architecture
### Lambda CRC triggers the SES function and awaits for the response
- CRC billing list is used as monitoring data 
  - CRC passes sendingList to SES 
  - SES iterates list, sends emails and returns monitoring data
  - monitoring email is sent to clearing office
  
## Event Example
### Passed to the triggering function
{
    "month": "2023/10/",
    "adresses": [
        {
            "email": "project1@gmail.at", 
            "cost_limit": 5000,
            "project_name": "Water_Bottle_Production",
            "forecast": 67133
        },       

        {
            "email": "project999@gmail.at,
            "cost_limit": 10000,
            "project_name": "Cola_Bottle_Production",
            "forecast": 9377
        },
    ]
}



