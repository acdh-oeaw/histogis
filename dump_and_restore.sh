#!/bin/bash

pg_dump -d histogis -h localhost -p 5433 -U  histogis -c -f histogis_dump.sql
psql -U postgres -d histogis < histogis_dump.sql