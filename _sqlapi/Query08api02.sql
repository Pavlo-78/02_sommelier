with
	 w as (	-- wines + price1L + short name of rating
			select 
			aw.*,
			aw.ratings_average as rating,
			aw.winery_id,
				(select 
					round(avg(vnt.price_euros * vnt.bottle_volume_ml/1000))
				from vintages vnt 
				where vnt.wine_id = aw.id
				group by vnt.wine_id) as price1L
			from wines aw)
	,m as (	-- comparison by matches number 
			select  
				a.wine_id as id, 
				b.wine_id as id2,
				sum(a.count * case when a.keyword_type ='primary' then 1 else 0.5 end) as taste_index,
				sum(a.count) as taste_confirmations			
			from keywords_wine a
			inner join keywords_wine b 
				on  1=1--a.wine_id <> b.wine_id
				and a.group_name = b.group_name
				and a.keyword_id = b.keyword_id
				and a.keyword_type = b.keyword_type
			where a.wine_id = @VINE 
--			where a.wine_id = 9710 --10175--in( 16578	, 10175)
			group by a.wine_id, b.wine_id)
	,n as ( --defining differences
			select 
				w1.name,		w2.name 		as name2,  
				w1.price1L, 	w2.price1L 		as price1L2,				
				w1.rating,		w2.rating 		as rating2, 	
				w1.winery_id,	w2.winery_id	as winery_id2,
				w2.price1L/w1.price1L 			as price1L_rdiff,
				abs(w1.rating - w2.rating) 		as rating_diff,
				m.*
			from m
			left join w w1 on w1.id = m.id
			left join w w2 on w2.id = m.id2
			order by m.taste_index desc)
	,t as ( --selecting the most similar wines by all indicators
			select  n.* 
					,(	select GROUP_concat(y.year,', ') 
							from (	select vvn.* 
									from vintages vvn
									where vvn.wine_id = n.id2
									order by vvn.year asc) y
							group by y.wine_id) as vintage		
			from n
			where price1L_rdiff between 0.8 and 1.2
			order by n.taste_index desc, n.rating_diff
			limit 16
			)
--result + layout
select 
	case when id=id2 then '*ORIGINAL*' else 'substitute' end type2,
	t.*
from t;
