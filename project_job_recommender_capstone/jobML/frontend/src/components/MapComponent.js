import React, { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import styles from './MapComponent.module.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiamdhaHVuaWEiLCJhIjoiY2x1NjBvejdrMXBycDJrbzZkdGdqbDU2NSJ9.Ya1zWmvoro9FtkfJOUM_Cw';

const MapComponent = () => {
  const mapContainerRef = useRef(null);

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-79.3832, 43.75], // Centered on Toronto
      zoom: 10,
    });

    map.on('load', () => {
      // Add source for cluster data using hardcoded GeoJSON
      map.addSource('jobs', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: [
            { type: 'Feature', properties: { fakePointCount: 98 }, geometry: { type: 'Point', coordinates: [-79.3832, 43.68] } }, // Toronto
            { type: 'Feature', properties: { fakePointCount: 73 }, geometry: { type: 'Point', coordinates: [-79.639319, 43.61] } }, // Mississauga
            { type: 'Feature', properties: { fakePointCount: 67 }, geometry: { type: 'Point', coordinates: [-79.525, 43.815] } }, // Vaughan
            { type: 'Feature', properties: { fakePointCount: 82 }, geometry: { type: 'Point', coordinates: [-79.325, 43.876] } }, // Markham
            { type: "Feature", properties: { fakePointCount: 24 }, geometry: { type: "Point", coordinates: [-123.1216, 49.2827] } }, // Vancouver
            { type: "Feature", properties: { fakePointCount: 35 }, geometry: { type: "Point", coordinates: [-114.0719, 51.0447] } }, // Calgary
            { type: "Feature", properties: { fakePointCount: 37 }, geometry: { type: "Point", coordinates: [-113.4909, 53.5444] } }, // Edmonton
            { type: "Feature", properties: { fakePointCount: 27 }, geometry: { type: "Point", coordinates: [-97.1384, 49.8951] } }, // Winnipeg
            { type: "Feature", properties: { fakePointCount: 32 }, geometry: { type: "Point", coordinates: [-75.6972, 45.4215] } }, // Ottawa
            { type: "Feature", properties: { fakePointCount: 22 }, geometry: { type: "Point", coordinates: [-73.5673, 45.5017] } }, // Montreal
            { type: "Feature", properties: { fakePointCount: 14 }, geometry: { type: "Point", coordinates: [-66.6458, 45.9636] } }, // Fredericton
            { type: "Feature", properties: { fakePointCount: 26 }, geometry: { type: "Point", coordinates: [-63.5752, 44.6488] } }, // Halifax
            { type: "Feature", properties: { fakePointCount: 19 }, geometry: { type: "Point", coordinates: [-106.6345, 52.1318] } }, // Saskatoon
            { type: "Feature", properties: { fakePointCount: 21 }, geometry: { type: "Point", coordinates: [-104.6178, 50.4452] } }, // Regina
            { type: "Feature", properties: { fakePointCount: 13 }, geometry: { type: "Point", coordinates: [-130.3208, 54.3164] } }, // Prince Rupert
            { type: "Feature", properties: { fakePointCount: 7 }, geometry: { type: "Point", coordinates: [-60.1955, 46.1386] } }, // Sydney
            { type: "Feature", properties: { fakePointCount: 9 }, geometry: { type: "Point", coordinates: [-63.1311, 46.2337] } }, // Charlottetown
            { type: "Feature", properties: { fakePointCount: 37 }, geometry: { type: "Point", coordinates: [-123.3656, 48.4284] } }, // Victoria
            { type: "Feature", properties: { fakePointCount: 98 }, geometry: { type: "Point", coordinates: [-86.300568, 32.377716] } }, // Montgomery, AL
            { type: "Feature", properties: { fakePointCount: 67 }, geometry: { type: "Point", coordinates: [-112.074036, 33.448376] } }, // Phoenix, AZ
            { type: "Feature", properties: { fakePointCount: 82 }, geometry: { type: "Point", coordinates: [-92.288986, 34.746613] } }, // Little Rock, AR
            { type: "Feature", properties: { fakePointCount: 84 }, geometry: { type: "Point", coordinates: [-121.493629, 38.576668] } }, // Sacramento, CA
            { type: "Feature", properties: { fakePointCount: 52 }, geometry: { type: "Point", coordinates: [-104.984856, 39.739227] } }, // Denver, CO
            { type: "Feature", properties: { fakePointCount: 35 }, geometry: { type: "Point", coordinates: [-72.683052, 41.763493] } }, // Hartford, CT
            { type: "Feature", properties: { fakePointCount: 37 }, geometry: { type: "Point", coordinates: [-75.519722, 39.157307] } }, // Dover, DE
            { type: "Feature", properties: { fakePointCount: 27 }, geometry: { type: "Point", coordinates: [-84.2807, 30.438118] } }, // Tallahassee, FL
            { type: "Feature", properties: { fakePointCount: 32 }, geometry: { type: "Point", coordinates: [-84.388229, 33.749027] } }, // Atlanta, GA
            {type: "Feature", properties: {fakePointCount: 20}, geometry: {type: "Point", coordinates: [-157.8583, 21.3069]}}, // Honolulu, Hawaii
            {type: "Feature", properties: {fakePointCount: 19}, geometry: {type: "Point", coordinates: [-116.2023, 43.615]}}, // Boise, Idaho
            {type: "Feature", properties: {fakePointCount: 15}, geometry: {type: "Point", coordinates: [-89.6501, 39.7817]}}, // Springfield, Illinois
            {type: "Feature", properties: {fakePointCount: 18}, geometry: {type: "Point", coordinates: [-86.1581, 39.7684]}}, // Indianapolis, Indiana
            {type: "Feature", properties: {fakePointCount: 22}, geometry: {type: "Point", coordinates: [-93.625, 41.5868]}}, // Des Moines, Iowa
            {type: "Feature", properties: {fakePointCount: 10}, geometry: {type: "Point", coordinates: [-95.6776, 39.0493]}}, // Topeka, Kansas
            {type: "Feature", properties: {fakePointCount: 30}, geometry: {type: "Point", coordinates: [-84.8733, 38.2009]}}, // Frankfort, Kentucky
            {type: "Feature", properties: {fakePointCount: 22}, geometry: {type: "Point", coordinates: [-91.1871, 30.4515]}}, // Baton Rouge, Louisiana
            {type: "Feature", properties: {fakePointCount: 23}, geometry: {type: "Point", coordinates: [-69.7795, 44.3106]}}, // Augusta, Maine
            {type: "Feature", properties: {fakePointCount: 12}, geometry: {type: "Point", coordinates: [-76.4922, 38.9784]}}, // Annapolis, Maryland
            {type: "Feature", properties: {fakePointCount: 29}, geometry: {type: "Point", coordinates: [-71.0589, 42.3601]}}, // Boston, Massachusetts
            {type: "Feature", properties: {fakePointCount: 14}, geometry: {type: "Point", coordinates: [-84.5555, 42.7325]}}, // Lansing, Michigan
            {type: "Feature", properties: {fakePointCount: 28}, geometry: {type: "Point", coordinates: [-93.09, 44.9537]}}, // Saint Paul, Minnesota
            {type: "Feature", properties: {fakePointCount: 25}, geometry: {type: "Point", coordinates: [-90.1848, 32.2998]}}, // Jackson, Mississippi
            {type: "Feature", properties: {fakePointCount: 30}, geometry: {type: "Point", coordinates: [-92.1735, 38.5767]}}, // Jefferson City, Missouri
            {type: "Feature", properties: {fakePointCount: 25}, geometry: {type: "Point", coordinates: [-112.0245, 46.5884]}}, // Helena, Montana
            {type: "Feature", properties: {fakePointCount: 15}, geometry: {type: "Point", coordinates: [-96.7026, 40.8136]}}, // Lincoln, Nebraska
            {type: "Feature", properties: {fakePointCount: 14}, geometry: {type: "Point", coordinates: [-119.7674, 39.1638]}}, // Carson City, Nevada
            {type: "Feature", properties: {fakePointCount: 16}, geometry: {type: "Point", coordinates: [-71.5376, 43.2081]}}, // Concord, New Hampshire
            {type: "Feature", properties: {fakePointCount: 13}, geometry: {type: "Point", coordinates: [-74.7429, 40.2171]}}, // Trenton, New Jersey
            {type: "Feature", properties: {fakePointCount: 23}, geometry: {type: "Point", coordinates: [-105.9378, 35.687]}}, // Santa Fe, New Mexico
            {type: "Feature", properties: {fakePointCount: 29}, geometry: {type: "Point", coordinates: [-73.7562, 42.6526]}}, // Albany, New York
            {type: "Feature", properties: {fakePointCount: 11}, geometry: {type: "Point", coordinates: [-78.6382, 35.7796]}}, // Raleigh, North Carolina
            {type: "Feature", properties: {fakePointCount: 13}, geometry: {type: "Point", coordinates: [-100.7837, 46.8083]}}, // Bismarck, North Dakota
            {type: "Feature", properties: {fakePointCount: 10}, geometry: {type: "Point", coordinates: [-82.9988, 39.9612]}}, // Columbus, Ohio
            {type: "Feature", properties: {fakePointCount: 19}, geometry: {type: "Point", coordinates: [-97.5164, 35.4676]}}, // Oklahoma City, Oklahoma
            {type: "Feature", properties: {fakePointCount: 20}, geometry: {type: "Point", coordinates: [-123.0351, 44.9429]}}, // Salem, Oregon
            {type: "Feature", properties: {fakePointCount: 21}, geometry: {type: "Point", coordinates: [-76.8867, 40.2732]}}, // Harrisburg, Pennsylvania
            {type: "Feature", properties: {fakePointCount: 11}, geometry: {type: "Point", coordinates: [-71.4128, 41.824]}}, // Providence, Rhode Island
            {type: "Feature", properties: {fakePointCount: 30}, geometry: {type: "Point", coordinates: [-81.0348, 34.0007]}}, // Columbia, South Carolina
            {type: "Feature", properties: {fakePointCount: 17}, geometry: {type: "Point", coordinates: [-100.351, 44.3683]}}, // Pierre, South Dakota
            {type: "Feature", properties: {fakePointCount: 13}, geometry: {type: "Point", coordinates: [-86.7816, 36.1627]}}, // Nashville, Tennessee
            {type: "Feature", properties: {fakePointCount: 13}, geometry: {type: "Point", coordinates: [-97.7431, 30.2672]}}, // Austin, Texas
            {type: "Feature", properties: {fakePointCount: 24}, geometry: {type: "Point", coordinates: [-111.891, 40.7608]}}, // Salt Lake City, Utah
            {type: "Feature", properties: {fakePointCount: 21}, geometry: {type: "Point", coordinates: [-72.5754, 44.2601]}}, // Montpelier, Vermont
            {type: "Feature", properties: {fakePointCount: 28}, geometry: {type: "Point", coordinates: [-77.436, 37.5407]}}, // Richmond, Virginia
            {type: "Feature", properties: {fakePointCount: 28}, geometry: {type: "Point", coordinates: [-122.9007, 47.0379]}}, // Olympia, Washington
            {type: "Feature", properties: {fakePointCount: 29}, geometry: {type: "Point", coordinates: [-81.6326, 38.3498]}}, // Charleston, West Virginia
            {type: "Feature", properties: {fakePointCount: 23}, geometry: {type: "Point", coordinates: [-89.4012, 43.0731]}}, // Madison, Wisconsin
            {type: "Feature", properties: {fakePointCount: 15}, geometry: {type: "Point", coordinates: [-104.8202, 41.14]}} // Cheyenne, Wyoming
          ],
        },
        cluster: true,
        clusterMaxZoom: 2, // Max zoom to cluster points on
        clusterRadius: 50, // Radius of each cluster when clustering points
      });

      // Add a layer for the clusters
      map.addLayer({
        id: 'clusters',
        type: 'circle',
        source: 'jobs',
        filter: ['has', 'fakePointCount'], // Use the fakePointCount property
        paint: {
          'circle-color': [
            'step',
            ['get', 'fakePointCount'],
            '#51bbd6',
            20,
            '#f1f075',
            50,
            '#f28cb1',
          ],
          'circle-radius': [
            'step',
            ['get', 'fakePointCount'],
            20,
            10,
            30,
            100,
            40,
          ],
        },
      });

      // Add a layer for the cluster labels
      map.addLayer({
        id: 'cluster-count',
        type: 'symbol',
        source: 'jobs',
        filter: ['has', 'fakePointCount'],
        layout: {
          'text-field': '{fakePointCount}',
          'text-size': 12,
        },
      });
    });

    return () => {
      map.remove();
    };
  }, []);

  return <div className={styles.mapContainer} ref={mapContainerRef} />;
};

export default MapComponent;
