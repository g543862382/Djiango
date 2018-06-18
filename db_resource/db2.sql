select count(*),productid
from axf_goods
group by productid
HAVING count(*) >1;

select productid,productname,productlongname,
  price,marketprice
from axf_goods
where categoryid=0
and childcid=0
ORDER BY price DESC ;

update axf_goods
set productname = productlongname
where productname = '';
