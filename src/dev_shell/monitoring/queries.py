class Queries:
    @staticmethod
    def get_queries(job_name):
        return {
            "cpu": f'rate(process_cpu_seconds_total{{job="{job_name}"}}[5m])',
            "memory": f'process_resident_memory_bytes{{job="{job_name}"}}',
            "requests_per_sec": f'rate(http_requests_total{{job="{job_name}"}}[5m])',
            "error_rate": f'rate(http_requests_total{{job="{job_name}", status=~"5.."}}[5m])',
            "latency_p95": f'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{{job="{job_name}"}}[5m])) by (le))'
        }
