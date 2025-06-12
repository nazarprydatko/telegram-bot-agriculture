#!/bin/bash
DATE=$(date +%Y-%m-%d)
pg_dump -U agro_user -d agro_db > backup_$DATE.sql
echo "Backup created: backup_$DATE.sql"
