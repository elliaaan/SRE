# SLI / SLO for PacToDo Backend (Flask)

## Overview

This document defines the Service Level Indicators (SLIs), Service Level Objectives (SLOs), and supporting reliability metrics for the **PacToDo backend**, developed with Flask.  
All metrics are collected via `prometheus_flask_exporter`, visualized in **Grafana**, and stored in **Prometheus**.


## SLIs (Service Level Indicators)

 Name                | Metric                                           -     Description                                                                
 Task success rate   | `rate(flask_http_request_total{status=~"2.."})`    -   Share of successful requests (HTTP 2xx responses)            
 Availability        | `rate(flask_http_request_total{status=~"2.."}) / rate(flask_http_request_total)` -  Measures API uptime                        
 Error rate          | `rate(flask_http_request_total{status=~"4..|5.."})` - Share of client/server errors (HTTP 4xx and 5xx responses)              
 Latency (buckets)   | `flask_http_request_duration_seconds_bucket`     -  Time buckets for request processing duration (e.g., 0.025s, 0.05s, 0.5s)   
 Task endpoints rate | `rate(create_task_total[5m])`, `rate(delete_task_total[5m])` -     Number of create/delete task operations over time              


## SLOs (Service Level Objectives)

 Objective Type | Target                                                                 

 Latency      | 95% of all requests should complete in under **500ms**                
 Availability | 99.9% availability of `/api/tasks` endpoint (downtime ≤ 43min/month)  
 Error Rate   | Error responses (5xx) must not exceed **1%** of total daily requests   


## SLA (Service Level Agreement)

While not formalized for users, the backend targets:

- **< 500ms** response time in 95% of cases
- **> 99.9%** uptime monthly
- Incident response time: within **60 minutes**

---

## Tools Used

- `prometheus_flask_exporter` — to expose metrics in `/metrics`
- **Prometheus** — to scrape and store metrics
- **Grafana** — to build dashboards for:
  - Task success rate
  - Availability (%)
  - Error rate (%)
  - Latency SLO for different thresholds (25ms / 50ms / 500ms)
- **Docker** — service management and failure simulation

---

## Dashboard Panels

- **Task Success SLO** — real-time success rate of task API
- **Error Rate SLO** — % of failed responses (4xx, 5xx)
- **Latency SLO** — stacked panel for 25ms, 50ms, 500ms buckets
- **Availability SLO** — based on HTTP 200/total ratio

---

## Test Scenario

- Simulated **container down** scenario to verify alerting & availability drop  
  Grafana and Prometheus correctly visualized the incident timeline.  
  Postmortem to be added separately.



##  Future Improvements

- Add **Prometheus alert rules** (e.g., latency > 300ms)
- Export **Grafana dashboards** (JSON or snapshot link)
- Add **alerts for 5xx spikes** and recovery visualization
- Integrate with incident logging tool or webhook

 
Last updated: May 31, 2025
