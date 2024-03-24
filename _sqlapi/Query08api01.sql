select 
	t.rn, t.id, t.name, t.winery_id, t.ratings_average as rating, cast(t.price1L as integer) as price1L,  t.vintage
	from (	select	
			ROW_NUMBER() OVER() AS rn,	
			wn.*,		
				(select	round(avg(vnt.price_euros * vnt.bottle_volume_ml / 1000))
				 from vintages vnt
				 where vnt.wine_id = wn.id
				 group by vnt.wine_id) as 
			price1L
			,	(select GROUP_concat(y.year,',') 
				from (	select vvn.* 
						from vintages vvn
						where vvn.wine_id = wn.id
						order by vvn.year asc --limit 3
						) y
				group by y.wine_id) as 
			vintage
			from  wines wn ) t
limit 100;


