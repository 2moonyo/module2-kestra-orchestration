import pandas as pd
import requests
from sqlalchemy import create_engine, inspect
import pyarrow.parquet as pq
from tqdm.auto import tqdm
import click
import os


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-database', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--green-table', default='green_taxi', help='Green taxi table name')
@click.option('--zone-table', default='taxi_zone', help='Taxi zone table name')
@click.option('--chunksize', default=500, type=int, help='Batch size for processing parquet')
def run(pg_user, pg_pass, pg_host, pg_port, pg_database, year, month, green_table, zone_table, chunksize):
    
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_database}')
    
    
    click.echo("Ingesting taxi zone lookup data...")
    prefix_zone = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc'
    url_zone = f'{prefix_zone}/taxi_zone_lookup.csv'
    
    taxi_zones = pd.read_csv(url_zone)
    

    taxi_zones.head(n=0).to_sql(name=zone_table, con=engine, if_exists='replace', index=False)
    click.echo(f"Created table '{zone_table}' with headers")
    

    taxi_zones.to_sql(name=zone_table, con=engine, if_exists='append', index=False)
    click.echo(f"Inserted {len(taxi_zones)} rows into '{zone_table}'")
    
    
    click.echo("\nIngesting green taxi trip data...")
    prefix_green = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url_green = f'{prefix_green}/green_tripdata_{year}-{month:02d}.parquet'
    local_file = 'green_tripdata.parquet'
    
    click.echo(f"Downloading from {url_green}...")
    with requests.get(url_green, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(local_file, 'wb') as f, tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc='Downloading'
        ) as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    
    
    parquet_file = pq.ParquetFile(local_file)
    total_rows = parquet_file.metadata.num_rows
    
    count = 0
    first = True
    batch_num = 0
    
    
    with tqdm(total=total_rows, desc='Ingesting rows', unit='rows') as pbar:
        for batch in parquet_file.iter_batches(batch_size=chunksize):
            df_chunk = batch.to_pandas()
            batch_num += 1
            batch_size = len(df_chunk)
            
            if first:
                
                df_chunk.head(n=0).to_sql(
                    name=green_table,
                    con=engine,
                    if_exists="replace",
                    index=False
                )
                
                inspector = inspect(engine)
                columns = inspector.get_columns(green_table)
                click.echo(f"\nTable '{green_table}' created with columns:")
                for col in columns:
                    click.echo(f"  {col['name']}: {col['type']}")
                click.echo("")
                
                first = False
            
            
            df_chunk.to_sql(
                name=green_table,
                con=engine,
                if_exists="append",
                index=False
            )
            
            count += batch_size
            pbar.update(batch_size)
            pbar.set_postfix({
                'batch': batch_num,
                'batch_size': batch_size,
                'total': count
            })
    
    click.echo(f"\nTotal batches processed: {batch_num}")
    click.echo(f"Total rows inserted into '{green_table}': {count}")
    
    
    if os.path.exists(local_file):
        os.remove(local_file)
        click.echo(f"Cleaned up temporary file: {local_file}")
    
    click.echo("\n✅ Data ingestion completed successfully!")


if __name__ == '__main__':
    run()