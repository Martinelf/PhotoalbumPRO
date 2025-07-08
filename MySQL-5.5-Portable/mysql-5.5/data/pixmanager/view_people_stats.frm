TYPE=VIEW
query=select `p`.`name` AS `person_name`,count(distinct `pp`.`photoID`) AS `photo_count` from (`pixmanager`.`people` `p` join `pixmanager`.`photo_people` `pp` on((`p`.`personID` = `pp`.`personID`))) group by `p`.`name`
md5=27369f3f0681cfeebb686a89a7d082b8
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=2024-12-25 17:10:48
create-version=1
source=SELECT\n  p.name AS person_name,\n  COUNT(DISTINCT pp.photoID) AS photo_count\nFROM people p\n  JOIN photo_people pp\n    ON p.personID = pp.personID\nGROUP BY p.name
client_cs_name=utf8
connection_cl_name=utf8_general_ci
view_body_utf8=select `p`.`name` AS `person_name`,count(distinct `pp`.`photoID`) AS `photo_count` from (`pixmanager`.`people` `p` join `pixmanager`.`photo_people` `pp` on((`p`.`personID` = `pp`.`personID`))) group by `p`.`name`
