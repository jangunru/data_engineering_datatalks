select 
	count(*) 
from yellow_taxi_trips
where cast(tpep_pickup_datetime as date) = '2021-01-15'

SELECT 
	date_trunc('day', tpep_pickup_datetime) as day,
	tip_amount 
FROM yellow_taxi_trips
order by 2 desc


select 
	"Zone",
	times
from zones as z
join (
	select 
		yellow_taxi_trips."PULocationID" as id,
		count(*) as times
	from yellow_taxi_trips 
	where cast(tpep_pickup_datetime as date) = '2021-01-14'
	group by 1
) as t
on t.id= z."LocationID"
order by times desc



select 	
	concat(t."PULocationID",'/',
	t."DOLocationID") as pairloc,
	(sum(t.total_amount)/count(*)) as avgAmount,
	t."PULocationID",
	t."DOLocationID",
	concat(zpu."Zone", '/',zdo."Zone" ) as zonesNames
from yellow_taxi_trips as t
join zones zpu
	on t."PULocationID" = zpu."LocationID"
join zones zdo
	on t."DOLocationID" = zdo."LocationID"
group by 1, 3, 4, 5
order by avgAmount desc