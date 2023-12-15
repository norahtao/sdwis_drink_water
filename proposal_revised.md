## Project Name

Safe Drinking Water Information System (SDWIS) API Wrapper

## Project Type

Option A: Functional / API Project

## Brief Description of Project Purpose

### Background
Prompted by the Biden-Harris Administration's efforts to eradicate lead in drinking water and reinforce the Lead and Copper Rule, the need for prompt and precise information about water quality has never been more imperative. The SDWIS serves as a crucial repository of data, including details on drinking water contamination, adherence to regulatory standards, and infringements by public water systems. This information is instrumental in protecting public health and shaping environmental policies.

### Objective
The core objective of this project is to develop Python wrappers for the Envirofacts Data Services API provided by the U.S. Environmental Protection Agency (EPA), with a focus on the Safe Drinking Water Information System (SDWIS). By providing an API client encapsulated in a Python package, users will be able to more simply and efficiently access important data about U.S. drinking water quality in the SDWIS database. For example, users can compare the results of lead or copper test samples from different areas.

## Links to API

### API Homepage: 
[Envirofacts Data Service API](https://www.epa.gov/enviro/envirofacts-data-service-api)

### Url Pattern
![Optional Image Description](https://s2.loli.net/2023/12/12/rkLpzJPd1HMZ4Ea.png)

The API itself as a whole is very large, providing access to a large amount of publicly available data, but for this project I'm only focusing on what's relevant to drinking water resources.

### Safe Drinking Water Information System (SDWIS) Database
![SDWIS Model](https://s2.loli.net/2023/12/12/9UFjtTrwl8v2amb.png)
### Example Query URL about SDWIS: 
1. Query how many of the 90th percentile lead or copper samples have a PB90 indicator greater than 0.015 in the results (mg/L)
`https://data.epa.gov/efservice/LCR_SAMPLE_RESULT/CONTAMINANT_CODE/=/PB90/SAMPLE_MEASURE/>/0.015/rows/COUNT/JSON`

- Response Body
    ```json
    [
      {
          "TOTALQUERYRESULTS": 8299
      }
    ]
    ```

2. Query 10 results in the test sample have a PB90 indicator greater than 0.015 (mg/L)
`https://data.epa.gov/efservice/LCR_SAMPLE_RESULT/CONTAMINANT_CODE/=/PB90/SAMPLE_MEASURE/>/0.015/rows/0:10/JSON`

- Response Body
  ```json
  [
      {
          "pwsid": "010502003",
          "sample_id": "01050200317607",
          "primacy_agency_code": "01",
          "epa_region": "01",
          "sar_id": 18509157,
          "contaminant_code": "PB90",
          "result_sign_code": "=",
          "sample_measure": 0.029,
          "unit_of_measure": "mg/L"
      },
      ...
  ]
  ```

## Overview of Technical Steps

### API Interaction and Data Retrieval:

Understand and utilize the Envirofacts RESTful data service API for querying the SDWIS and other relevant databases. Implement methods to construct URLs for different types of queries, considering parameters like table names, column names, operators, and rows. I will be using the **`"requests"`** package for web requests.

For some requests that may query large amounts of data. I will use **`"ThreadPoolExecutor"`** to manage the thread pool and process multiple API requests concurrently in a multi-threaded manner to reduce the user's waiting time. In addition, **`"tqdm"`** will be used to provide a progress bar for the requests, providing visual feedback on the progress of the API requests.


### Handling Output Formats:
The Envirofacts API provides functionality for various output formats (XML, JSON, CSV, Excel). In my project, I will mainly use JSON format to get the reponse from the API. I need to process, parse the JSON response using the **`"json"`** package.


To unify the formatted output, I will use the **`"tabulate"`** library to enhance the user experience by displaying the query results in a more organized and readable format.

### Program Logging:

I will be using **`"logging"`** to configure the logging module. Logging possible errors and exceptions in a structured way allows for more efficient error tracking and resolution. When a user encounters a problem, they can view the logs to see what actions were performed and what errors occurred, thus helping to troubleshoot faster.

### Testing

I will use **`"unittest"`** to create test cases for a number of functions to ensure that the program performs as expected


## Potential Challenges

According to the API settings, the queried data does **not provide a direct address**, only the water system identification code **PWSID**.

#### Definition of PWSID:
```
PWSID uniquely identifies the water system within a specific state. The format is `SSXXXXXXXXXXXX` where: 

- `SS` = the Federal Information Processing Standard (FIPS) Pub 5-2 State abbreviation in which the water system is located, or the region number of the EPA region responsible for an Indian reservation.
- `XXXXXXXXXXXX` = the water system identification code assigned by the EPA region or the State.
```

As a result, users need to obtain the water system ID through other means to perform related queries. This raises the threshold for users to a certain extent.

From the perspective of **project integrity**, this issue is not seen to have a significant impact. The limitation is inherent to the requirements of the API itself and the data it provides.