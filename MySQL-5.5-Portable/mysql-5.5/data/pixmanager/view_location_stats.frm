TYPE=VIEW
query=select `l`.`location_name` AS `location_name`,count(distinct `p`.`photoID`) AS `photo_count` from (`pixmanager`.`locations` `l` join `pixmanager`.`photos` `p` on((`l`.`locationID` = `p`.`locationID`))) group by `l`.`location_name`
md5=7e794df7611e36d8c249bc17540e7aad
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=2024-12-25 17:14:48
create-version=1
source=SELECT\n  l.location_name,\n  COUNT(DISTINCT p.photoID) AS photo_count\nFROM locations l\n  JOIN photos p\n    ON l.locationID = p.locationID\nGROUP BY l.location_name
client_cs_name=utf8
connection_cl_name=utf8_general_ci
view_body_utf8=select `l`.`location_name` AS `location_name`,count(distinct `p`.`photoID`) AS `photo_count` from (`pixmanager`.`locations` `l` join `pixmanager`.`photos` `p` on((`l`.`locationID` = `p`.`locationID`))) group by `l`.`location_name`
