use pytest;
select * from quotes_author order by name;



DELETE FROM quotes_author WHERE name IS NULL;

