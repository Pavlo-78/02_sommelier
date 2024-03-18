with
	 w as (	-- wines + price1L + short name of rating
			select 
			aw.*,
			aw.ratings_average as R,
			aw.winery_id as wr_id,
				(select 
					round(avg(vnt.price_euros * vnt.bottle_volume_ml/1000))
				from vintages vnt 
				where vnt.wine_id = aw.id
				group by vnt.wine_id) as price1L
			from wines aw)
	,m as (	-- comparison by matches number 
			select  
				a.wine_id, 
				b.wine_id as wine_id2,
				sum(a.count * case when a.keyword_type ='primary' then 1 else 0.5 end) as flavor_matches
				--sum(a.count) as cccnt			
			from keywords_wine a
			inner join keywords_wine b 
				on  a.wine_id <> b.wine_id
				and a.group_name = b.group_name
				and a.keyword_id = b.keyword_id
				and a.keyword_type = b.keyword_type
			where a.wine_id =10175--in( 16578	, 10175)
			group by a.wine_id, b.wine_id)
	,n as ( --defining differences
			select 
				w1.name, 	w2.name 	as name2,  
				w1.price1L, w2.price1L 	as price1L2, 	w2.price1L/w1.price1L 	as price1L_rdiff,
				w1.R, 		w2.R 		as R2, 			abs(w1.R - w2.R) 		as R_diff,
				w1.wr_id,	w2.wr_id	as wr_id2,
				m.*
			from m
			left join w w1 on w1.id = m.wine_id
			left join w w2 on w2.id = m.wine_id2
			order by m.flavor_matches desc)
	,t as ( --selecting the most similar wines by all indicators
			select  n.* 
					,(	select GROUP_concat(y.year,',') 
							from (	select vvn.* 
								from vintages vvn
								where vvn.wine_id = n.wine_id
								order by vvn.year asc limit 3) y
							group by y.wine_id) as vintag		
			from n
			where price1L_rdiff between 0.8 and 1.2
			order by n.flavor_matches desc, n.R_diff
			limit 20
			)
select 
substr(t.name||'...............................................', 1, 50) ||' '||
substr(t.wr_id 						|| '        ',1, 9 ) ||
substr(t.R 							|| '        ',1, 9 ) ||	
substr(cast(t.price1L as INTEGER) 	|| '        ',1, 8 ) ||
substr(t.vintag 					|| '        ',1, 14) as wine,
substr(t.name2||'...............................................', 1, 50) ||' '||
substr(t.wr_id2						|| '        ',1, 9 ) ||
substr(t.R2 							|| '        ',1, 9 ) ||	
substr(cast(t.price1L2 as INTEGER) 	|| '        ',1, 8 ) ||
substr(t.vintag 					|| '        ',1, 14) as wine2,
t.*
from t
;

	
	