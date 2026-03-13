# Grafana Dashboard Provisioning

A provisionable Grafana dashboard for infrastructure monitoring. Shows CPU usage and memory usage from Prometheus `node_exporter` metrics.

## Panels

| Panel | Metric |
|-------|--------|
| CPU Usage | `node_cpu_seconds_total` (idle mode, inverted) |
| Memory Usage | `node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes` |

## Provisioning

Place in your Grafana provisioning directory:

```bash
cp dashboard.json /etc/grafana/provisioning/dashboards/
```

Add a provisioning config at `/etc/grafana/provisioning/dashboards/infra.yaml`:

```yaml
apiVersion: 1
providers:
  - name: infrastructure
    folder: Infrastructure
    type: file
    options:
      path: /etc/grafana/provisioning/dashboards
```

Then restart Grafana:

```bash
systemctl restart grafana-server
```

## Requirements

- Grafana 9.0+
- Prometheus datasource
- `node_exporter` running on monitored hosts
