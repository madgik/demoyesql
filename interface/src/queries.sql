select * from nsf limit 10;
select * from publication limit 2;
select count(*) from nsf;
select count(*) from publication;
select regexprmatch('\d{3}','an example of 3 digit number: 343') as match;

sample '100' select * from nsf;
select sum(regexprmatch('\d{7}',grantid)) as matches, count(*) as total from nsf;

select c1, textwindow2s(keywords(lower(c2)), 10,1,3,"\d{7}") from publication limit 100;

select * from (select c1, textwindow2s(keywords(lower(c2)), 10,1,3,"\d{7}") from publication), nsf where middle = grantid and regexprmatch('nsf|national science foundation', prev||next);
