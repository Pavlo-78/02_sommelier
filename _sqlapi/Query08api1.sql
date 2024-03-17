select	
		wn.name || ' /// winery=' || wn.winery_id || ', ' || 'ratings_average=' || wn.ratings_average as wine,			
			(-- price - directly to field	
			select	round(avg(vnt.price_euros * vnt.bottle_volume_ml / 1000))
			from vintages vnt
			where vnt.wine_id = wn.id
			group by vnt.wine_id
		) as price_L1
from  wines wn 
where
	upper(wn.name) like upper(@VINE);
--	upper(wn.name) like upper('Cabernet Sauvignon')
--limit 1000;	
