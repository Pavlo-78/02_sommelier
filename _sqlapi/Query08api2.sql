/* 
 top 2 offers for each wines of kind 'Cabernet Sauvignon', 
 which the most likely resemble it by taste and price	*/
----------------------------------------------------------------------------------
--EXPLAIN QUERY PLAN
with a as (
--basic search
select 
	t.wine_id1, -- pfix "s" means "searched" wine_id, wine, price, etc.	
	t.wine1,
	t.price_L1,
--	t.rating1,
	kw2.group_name as groupp,
	kw2.count as count_users,
	kw2.keyword_id ,
	kw2.wine_id as wine_id2,
	w.name||' / winery'|| w.winery_id||' / '||w.ratings_average as wine2,	
	w.ratings_average as rating2,
	(-- price to field directly
		select round(avg(vnt.price_euros * vnt.bottle_volume_ml/1000))
		from vintages vnt where vnt.wine_id = kw2.wine_id
		group by vnt.wine_id ) as price_L2
from 	keywords_wine kw2
left join wines w ON w.id = kw2.wine_id 
--**join all keywords for 'Cabernet Sauvignon'
inner join (select  kw.wine_id as wine_id1,
					wn.name ||' / winery'|| wn.winery_id||' / '||wn.ratings_average as wine1,
					wn.ratings_average as rating1,
					kw.keyword_id,
					kw.group_name,
					kw.keyword_type,
					(-- price - directly to field	
						select round(avg(vnt.price_euros * vnt.bottle_volume_ml/1000))
						from vintages vnt where vnt.wine_id = kw.wine_id
						group by vnt.wine_id ) as price_L1
			from 	keywords_wine kw
			inner join wines wn ON wn.id = kw.wine_id
			where upper(wn.name) like upper(@VINE) --and wn.id =16578
			and kw.keyword_type ='primary'
			and wn.fizziness is null
			) t 
	on  kw2.keyword_id 		= t.keyword_id
	and kw2.group_name 		= t.group_name 
	and kw2.keyword_type 	= t.keyword_type
where kw2.keyword_type 		= 'primary'
and kw2.count>100 --optimization from 6.27sec to 0.57sec
and price_L2 between t.price_L1*0.90 and t.price_L1*1.10
and t.wine_id1 <> kw2.wine_id --and kw2.keyword_id=292
and w.fizziness is null
order by t.wine_id1, kw2.count desc	) --select * from a;
--
-- hide kywords
,b as (
select  wine_id1, wine1||' ('|| price_L1||' EUR/1L)' as wine1, price_L1,
		wine_id2, wine2||' ('|| price_L2||' EUR/1L)' as wine2, price_L2,
		max(count_users) as count_users,
		ROW_NUMBER() OVER(PARTITION BY wine_id1 ORDER BY rating2 desc, sum(count_users) desc) as RN
from a
group by wine_id1, wine1, price_L1,	wine_id2, wine2, price_L2
order by wine_id1, sum(count_users) desc )
--select * from b;
-- result
select b.* from b where b.RN <= 5 order by price_L1 desc, count_users desc, wine_id1;
