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
    "month": "2023/10/Cost reports",
    "adresses": [
        {
            "email": "cast.ses.1@efs.at", 
            "cost_limit": 5000,
            "project_name": "1400-Kassel-LZ1",
            "forecast": 67133
        },
        {
            "email": "cast.ses.1@efs.at",
            "cost_limit": 10000,
            "project_name": "1200-Hannover-Comp",
            "forecast": 9377
        },
        {
            "email": "cast.ses.1@efs.at",
            "cost_limit": 5000,
            "project_name": "1300-Braunschweig",
            "forecast": 64491
        },
        {
            "email": "cast.ses.1@efs.at",
            "cost_limit": 5000,
            "project_name": "FantasyProject",
            "forecast": 64491
        },
        {
            "email": 0,
            "cost_limit": 5000,
            "project_name": "1300-Braunschweig",
            "forecast": 64491
        }
    ]
}
