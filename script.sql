CREATE TABLE IF NOT EXISTS bus_stop_links (
  id VARCHAR(255) UNIQUE NOT NULL,
  from_stop VARCHAR(255),
  to_stop VARCHAR(255),
  FOREIGN KEY (from_stop) REFERENCES bus_stops(stop_point_ref),
  FOREIGN KEY (to_stop) REFERENCES bus_stops(stop_point_ref)
);
CREATE TABLE IF NOT EXISTS bus_stops (
  stop_point_ref VARCHAR(255) UNIQUE NOT NULL,
  CommonName VARCHAR(255),
  Latitude FLOAT,
  Longitude FLOAT
);
CREATE TABLE IF NOT EXISTS buses (
  id SERIAL PRIMARY KEY,
  VehicleUniqueId VARCHAR(255),
  BlockRef VARCHAR(255),
  DestinationAimedArrivalTime VARCHAR(255),
  DestinationName VARCHAR(255),
  DestinationRef VARCHAR(255),
  DirectionRef VARCHAR(255),
  LineRef VARCHAR(255),
  OperatorRef VARCHAR(255),
  OriginAimedDepatureTime VARCHAR(255),
  OriginName VARCHAR(255),
  OriginRef VARCHAR(255),
  PublishedLineName VARCHAR(255),
  Bearing VARCHAR(255),
  Latitude FLOAT,
  Longitude FLOAT,
  RecordedAtTime VARCHAR(255),
  ValidUntilTime VARCHAR(255),
  InsertedAtTime VARCHAR(255),
  UpdatedAtTime VARCHAR(255)
);