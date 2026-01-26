# Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

SELECT COUNT(*)
FROM public.green_taxi
WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
AND trip_distance <= '1';

7,853
8,007 [x]
8,254
8,421
# Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

2025-11-14 [x]
2025-11-20
2025-11-23
2025-11-25

SELECT MAX(trip_distance)
FROM public.green_taxi
WHERE lpep_pickup_datetime::date='2025-11-14'
AND trip_distance <=100
AND trip_distance > 10;

# Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

East Harlem North [x]
East Harlem South
Morningside Heights
Forest Hills

SELECT 
    tz."Zone", 
    SUM(gt.total_amount) AS sum_total_fare
FROM public.green_taxi AS gt
JOIN public.taxi_zone AS tz
  ON gt."PULocationID" = tz."LocationID"
WHERE gt.lpep_pickup_datetime::date = '2025-11-18'
GROUP BY 
    tz."Zone"
ORDER BY 
    sum_total_fare DESC
LIMIT 1;

# Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.

JFK Airport
Yorkville West [x]
East Harlem North
LaGuardia Airport
Terraform
In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. Copy the files from the course repo here to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.

# Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

Downloading the provider plugins and setting up backend,
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform`
Answers:

terraform import, terraform apply -y, terraform destroy
teraform init, terraform plan -auto-apply, terraform rm
terraform init, terraform run -auto-approve, terraform destroy
terraform init, terraform apply -auto-approve, terraform destroy
terraform import, terraform apply -y, terraform rm
