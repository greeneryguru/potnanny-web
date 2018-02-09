insert into settings ("name","value","notes") values ("polling interval minutes", 3, "Delay between sensor checks. Low polling value increases load on the CPU and database storage space.");
insert into settings ("name","value","notes") values ("store temperature fahrenheit", 1, "Store temperatures in the database as Fahrenheit(1) or Celsius(0)");
insert into settings ("name","value","notes") values ("hi-res data retention days", 7, "Measurments older than this setting are removed from the database. High-resolution data uses significantly more space in the database.");
insert into settings ("name","value","notes") values ("hourly-avg data retention days", 120, "Measurments older than this setting are removed from the database. Hourly-average data uses significantly less space in the database, and can be stored for long periods.");

# insert into sensors("name", "tags", "address") values ("temp sensor 1", "temperature dht22", 2);