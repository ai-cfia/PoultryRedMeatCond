## Purpose
This repository allows us to share data `ADH-717 - Poultry and Red Meat Condemnations in Federally Registered Establishments - Criteria` with the visualization team. 

When the [new monthly report](https://aimis-simia.agr.gc.ca/rp/index-eng.cfm?action=pR&pdctc=&r=278) is released, the `CSV_downloader.py`script is executed, and it downloads the new report and merges it into `ADH-717 Poultry and Red Meat data.csv`.

## Updates
* `ADH-717 Poultry and Red Meat data.csv` now contains all historical data (since 1999, instead of only a 3-year window).
* Runs from Docker container, automated thanks to GitHub Actions (CRON job), instead of using Azure DataBricks.
* Answers the security question to gain access to the new report.

## Running the script locally
### Building the container
`docker build -t csvscraper .`

### Running the container
`docker run -v ./data:/usr/src/app/data -p 8081:8081 csvscraper`
