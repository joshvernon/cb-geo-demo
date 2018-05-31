# N1QL Queries
* Select features modified in last 5 minutes
    ```
    select geometry, properties, type from viastops where date_diff_millis(now_millis(), properties.`modified_date`, 'minute') <= 5;
    ```