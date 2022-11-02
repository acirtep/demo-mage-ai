# demo-mage-ai
Demo of mage.ai and error on write vs error on read

Base repo for investigating data processing design
Article 1: https://ownyourdata.ai/wp/traditional-vs-modern-analytics-data-processing-part-1/ 


# dev
1. `docker-compose up --build`
2. Execute alembic migration `docker exec -it demo_mage_app alembic upgrade head`
3. Start mage `docker exec -it demo_mage_app mage start demo_error_read_write`

# clean
1. `docker-compose down`
