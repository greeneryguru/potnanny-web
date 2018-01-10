insert into users ("username", "password") values ("admin", "pbkdf2:sha256:50000$eGXLn1tI$3dce263bf46ac8315028ca42e6115883282d4ee6af8309d182f7cc3690aa6e62");

insert into measurement_types("name") values ("temperature");
insert into measurement_types("name") values ("humidity");
insert into measurement_types("name") values ("soil-moisture");

insert into settings ("name","value","notes") values ("polling interval minutes", 3, "Delay between sensor checks. Low polling value increases load on the CPU and database storage space.");
insert into settings ("name","value","notes") values ("store temperature fahrenheit", 1, "Store temperatures in the database as Fahrenheit(1) or Celsius(0)");
insert into settings ("name","value","notes") values ("hi-res data retention days", 7, "Measurments older than this setting are removed from the database. High-resolution data uses significantly more space in the database.");
insert into settings ("name","value","notes") values ("hourly-avg data retention days", 120, "Measurments older than this setting are removed from the database. Hourly-average data uses significantly less space in the database, and can be stored for long periods.");
insert into settings ("name","value","notes") values ("rf tx pin", 11, "Pin number the RF transmitter is connected to.");
insert into settings ("name","value","notes") values ("rf tx base code", 12066304, "Wireless transmit codes are calculated from the base code and channel number. Intey=1206630, Etekcity=446200");
insert into settings ("name","value","notes") values ("rf outlet brand", 1, "1=Intey, 2=Etekcity");

insert into sensors("name", "tags", "address") values ("temp sensor 1", "temperature dht22", 2);