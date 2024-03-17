select 
	substr( t.RN||'.        ', 1,6) ||
	substr(t.name||'................................................', 1, 50) ||
	substr(' winery=' || t.winery_id || '       ',1, 15	) ||
	' rating(avg)=' || t.ratings_average ||
	'  price_1L(euro)=' || cast(t.price_L1 AS INTEGER) ||
	substr(' - oldest 3 years= '|| vintag ||'                      ',1,35) as wine, 	
	t.price_L1, t.id, t.vintag
	from (
	select	
	ROW_NUMBER() OVER() AS RN,	
	wn.*,		
	(select	round(avg(vnt.price_euros * vnt.bottle_volume_ml / 1000))
		from vintages vnt
		where vnt.wine_id = wn.id
		group by vnt.wine_id) as price_L1
	,(	select GROUP_concat(y.year,',') 
		from (	select vvn.* 
				from vintages vvn
				where vvn.wine_id = wn.id
				order by vvn.year asc limit 3) y
		group by y.wine_id) as vintag
	from  wines wn ) t
where upper(t.name) like upper(@VINE) ;--limit 3;
--where t.name like '%'

