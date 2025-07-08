TYPE=VIEW
query=select `t`.`tag_name` AS `tag_name`,count(distinct `pt`.`photoID`) AS `photo_count` from (`pixmanager`.`tags` `t` join `pixmanager`.`photo_tags` `pt` on((`t`.`tagID` = `pt`.`tagID`))) group by `t`.`tag_name`
md5=40df3e289873e5a82eabfa4bba665f2b
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=2024-12-25 17:11:26
create-version=1
source=SELECT\n  t.tag_name,\n  COUNT(DISTINCT pt.photoID) AS photo_count\nFROM tags t\n  JOIN photo_tags pt\n    ON t.tagID = pt.tagID\nGROUP BY t.tag_name
client_cs_name=utf8
connection_cl_name=utf8_general_ci
view_body_utf8=select `t`.`tag_name` AS `tag_name`,count(distinct `pt`.`photoID`) AS `photo_count` from (`pixmanager`.`tags` `t` join `pixmanager`.`photo_tags` `pt` on((`t`.`tagID` = `pt`.`tagID`))) group by `t`.`tag_name`
