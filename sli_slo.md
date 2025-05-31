#  SLI / SLO for PacToDo Backend (Flask)

## Information 

Application: PacToDo (backend — Flask)  
Metrics are collected via `prometheus_flask_exporter`  
Data source: Prometheus + Grafana Dashboard


##  SLI (Service Level Indicators)

| Name                   | Metrics                                      | Description                                                              |
|------------------------|----------------------------------------------|--------------------------------------------------------------------------|
| Request count          | `flask_http_request_total`                   | Total number of requests, by methods and statuses                        |
| Request latency        | `flask_http_request_duration_seconds_bucket` | Distribution of response time across buckets                             |
| Task created count     | `create_task_total`                          | Number of tasks created                                                  |
| Task deleted count     | `delete_task_total`                          | Number of tasks deleted                                                  |



##  SLO (Service Level Objectives)

| Name          | Target                                                                                               |
|---------------|------------------------------------------------------------------------------------------------------|
| Latency       | 95% of all requests should be processed in < 500ms                                                   |
| Availability  | Endpoint `/api/tasks` is available 99.9% of the time (no more than 43 minutes of downtime per month) |
| Error Rate    | The number of 5** errors should not exceed 1% of the total number of requests per day                |



## SLA (optional)

We strive to provide:
- Response time < 500ms in 95% of cases
- Uptime 99.9%
- Incident support within 1 hour

*(This section demonstrates what user expectations might look like in a real SLA agreement)*


## Tools used

- `prometheus_flask_exporter`
- `Prometheus` (Metrics)
- `Grafana` (visualization)
