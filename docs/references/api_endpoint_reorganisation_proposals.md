1. **patient_data**
  - *retrieve_data*
    - GET: get API documentation and usage information, that is to say, the generic documentation of the API.
    - POST: query patient vital signs data for all vital sign tables using JSON request body. This conflicts with the semantical purpose of this API endpoint, should be placed into the second API endpoint.
  I think even this route should be renamed to something more generic like *metadata*, and place two routes, one to retrieve vital signs metadata, and another one for operational metadata

2. **vital_signs**
  - GET: retrieve all vital signs data for a patient within a date range using an optimised UNION ALL query for better performance
  - POST: it's here where the POST method in the first API endpoint should be placed.

3. **operational_data**
  - Keep as is