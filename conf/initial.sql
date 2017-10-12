insert into users ("username","password") values ("admin","pbkdf2:sha256:50000$eGXLn1tI$3dce263bf46ac8315028ca42e6115883282d4ee6af8309d182f7cc3690aa6e62");

insert into settings ("name","value") values ("data retention days",60);
insert into settings ("name","value") values ("polling interval minutes",3);
insert into settings ("name","value") values ("base code",12066304);
insert into settings ("name","value") values ("store temperature fahrenheit",1);

insert into measurement_types ("name","code") values ("temperature", "t");
insert into measurement_types ("name","code") values ("humidity", "h");
insert into measurement_types ("name","code") values ("soil moisture", "sm");


insert into sensors ("name","notes","profile") values ("main temp/humidity", "AcuRite 592TXR wireless","t,h");
insert into sensors ("name","notes","profile") values ("soil sensor 1", "", "sm");
insert into sensors ("name","notes","profile") values ("soil sensor 2", "", "sm");
insert into sensors ("name","notes","profile") values ("soil sensor 3", "", "sm");
insert into sensors ("name","notes","profile") values ("soil sensor 4", "", "sm");



