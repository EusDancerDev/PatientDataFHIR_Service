Perfect! Now it's clear about how are the SELECT queries built up.
Now, we're going to scale the whole app up.

1. Add a table in the database 'KM0' that contains fictitious administrative data of the staff:
  1.1 Name the table like `staff` or something else, similar, as you wish
  1.2 The columns are:
    - `index`: primary key, autoindex, increment +1
    - `username`: not a nickname, but a real-world compatible name
    - `usersurname`: surname of the subject
    - `password`: password following the basic security standards:
        * Minimum length of 8 characters
        * One uppercase letter at least
        * One lowercase letter at least
        * One special, non-word character
    - `role`: role of the professional that will make use of the web service:
      `admin`: meaning an administrative, taking care of staff hiring, measurement equipment availability, etc.
      `medical`: healthcare professional.
  Regarding the password, a common issue sounds to me: some special characters are sort of escaped instead of treating them as literals; if my memory serves, this issue is fixed using the `text` subclass of the package SQLAlchemy.

2. Add an authentication web service (Swagger UI):
  2.1 It will ask for:
    - User name: linked to `username` attribute
    - User surname: linked to `usersurname` attribute
    - Password: linked to `password` attribute
  2.2 Methods
    - GET: mimic the `GET` method for the `retrieve_data` route, creating the necessary models
    - POST: once again, mimic the `POST` method for the `retrieve_data` route, creating the necessary models with the following draft example:
      ```json
      staff_query_model = api.model('StaffQuery', {
        'username': fields.String(required=True, description='Name of the person using the database', example='Jon'),
        'usersurname': fields.String(required=True, description='First surname of the person using the database', example='Huertas'),
        'password': fields.String(required=True)
      })
      ```
      I put a likely non-existent `fields.dropdown` attribute up there, I was just trying to put an understandable example.

  2.3 Data validation (both methods, 'GET' and 'POST')
    2.3.1 First block
      - Validate the user name and surname and passwords at once, performing the following query
      ```SQL
      SELECT username, usersurname, password FROM staff
      ```
      If the above query returns zero length data, warn telling that either the user's full name and/or password is incorrect; we won't give any hint as to which data from the introed is correct.
    2.3.2 Second block
      - Validate the role parameter, checking whether the default option is selected. If so, warn accordingly.

  2.4 Finally, my question: is this web service addable on the top of the service that just searches for coincident data, or would this new service wrap the searcher?

3. Definition of operational data (i.e. non-vital signs)
  - Create a file similar to @vital_signs_tables.py (sth like `operational_tables.py`), but considering all tables in @patient_models.py except those in @vital_signs_tables.py. 

4. Data retrieval: integration and scaleup of our current web service
  - If the authentication is a success, depending on the role selected, redirect to this second web service
    * If `role==medical`: simply redirect to our current web service, that where we select the ID of the patient and the range of timestamps.
    * If `role==admin`: retrieve data from all tables with operational data as is, converting it to HL7 v2 (file @hl7_formatter.py) and then to FHIR version 5 (file @fhir_formatter.py). For all operational tables considered in `operational_tables.py`