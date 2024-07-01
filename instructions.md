# GOAL
- Deploy a Lambda that runs automatically on day x that does following:
    - query Customer DB with dedictaed Role
    - find out if some tenants need to update their data
    - invoke SES Lambda sending required payload

# Steps
1. pack updater_logic into lambda_handler and run locally with test data
2. add lambda to template
2. add querying logic and dedicated role   
    FOR DEV   
    **arn:aws:iam::471685057907:role/vw-lambda-reporting-CostReportingFunctionRole-AXA0WJOBOLIW**
4. deploy to customers DEV account using specific samconfig variables
5. invoke SES lambda sending payload
    code to filter which lambda to run => see trigger/app.py
    
6. test it and loop until return artifact working as desired 
