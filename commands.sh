#!/bin/bash
table_name="$1"
function spark-job(){
    local table_name="$1"  # Assign the provided table name to a local variable
    local table_id="${table_name::-1}_id"  # Extract "order" from the table name and append "_id"
    local target_path="s3a://warehouse/database=default/table_name=${table_name}"
    
    # Echoing the command and variable values
    echo "Executing spark-submit command:"
    echo "table_name: $table_name"
    echo "table_id: $table_id"
    echo "target_path: $target_path"

    spark-submit \
    --class org.apache.hudi.utilities.streamer.HoodieStreamer \
    --packages 'org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.0,org.apache.hadoop:hadoop-aws:3.3.2' \
    --properties-file spark-config.properties \
    --master 'local[*]' \
    --executor-memory 1g \
    --jars jar-files/hudi-extensions-0.1.0-SNAPSHOT-bundled.jar,jar-files/hudi-java-client-0.14.0.jar \
     jar-files/hudi-utilities-slim-bundle_2.12-0.14.0.jar \
    --table-type COPY_ON_WRITE \
    --target-base-path "s3a://warehouse/database=default/table_name=${table_name}"  \
    --target-table ${table_name} \
    --op UPSERT \
    --enable-sync \
    --enable-hive-sync \
    --sync-tool-classes 'io.onetable.hudi.sync.OneTableSyncTool' \
    --source-limit 4000000 \
    --source-class org.apache.hudi.utilities.sources.debezium.PostgresDebeziumSource \
    --payload-class org.apache.hudi.common.model.debezium.PostgresDebeziumAvroPayload \
    --min-sync-interval-seconds 10 \
    --continuous \
    --source-ordering-field _event_origin_ts_ms \
    --hoodie-conf bootstrap.servers=localhost:7092 \
    --hoodie-conf schema.registry.url=http://localhost:8081 \
    --hoodie-conf hoodie.deltastreamer.schemaprovider.registry.url=http://localhost:8081/subjects/hive.public.${table_name}-value/versions/latest \
    --hoodie-conf hoodie.deltastreamer.source.kafka.value.deserializer.class=io.confluent.kafka.serializers.KafkaAvroDeserializer \
    --hoodie-conf hoodie.deltastreamer.source.kafka.topic=hive.public.${table_name} \
    --hoodie-conf auto.offset.reset=earliest \
    --hoodie-conf hoodie.datasource.write.recordkey.field=${table_id} \
    --hoodie-conf hoodie.datasource.write.partitionpath.field= \
    --hoodie-conf hoodie.datasource.write.precombine.field=_event_origin_ts_ms \
    --hoodie-conf 'hoodie.onetable.formats.to.sync=DELTA,ICEBERG' \
    --hoodie-conf 'hoodie.onetable.target.metadata.retention.hr=168' \
    --hoodie-conf 'hoodie.metadata.index.async=true' \
    --hoodie-conf 'hoodie.metadata.enable=true' \
    --hoodie-conf 'hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.MultiPartKeysValueExtractor' \
    --hoodie-conf 'hoodie.datasource.hive_sync.metastore.uris=thrift://localhost:9083' \
    --hoodie-conf 'hoodie.datasource.hive_sync.mode=hms' \
    --hoodie-conf 'hoodie.datasource.hive_sync.enable=true' \
    --hoodie-conf 'hoodie.datasource.hive_sync.database=default' \
    --hoodie-conf hoodie.datasource.hive_sync.table=${table_name} \
    --hoodie-conf 'hoodie.datasource.write.hive_style_partitioning=true'

}

# Call the function with the provided argument
# spark-job "$1"