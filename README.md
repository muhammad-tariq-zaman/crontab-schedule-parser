# crontab-schedule-parser

Parse crontab lines and describe each schedule in plain English, so a
schedule can be checked at a glance before it is installed. Invalid
field values are reported instead of silently accepted.

## How to run

```bash
python3 main.py crontab.txt
```

## Example output

```text
*/15 * * * * job -> every 15 minutes; every hour; every day of month; every month; every day of week :: job
```

Standard library only. No network access. It only reads and describes;
it never installs a crontab.
