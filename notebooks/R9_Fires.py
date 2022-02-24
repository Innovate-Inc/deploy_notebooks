# %%
pip install openpyxl

# %%
pip install slack_sdk

# %%
from notebooks.func import *

# %%
import sys
from datetime import datetime as dt
from arcgis.features import Feature
from arcgis.gis import GIS
import json
from tenacity import retry, stop_after_attempt, after_log
import logging
from slack_sdk.webhook import WebhookClient

# %%
import arcgis
arcgis.__version__

# %%
FIRE_REPORT_SETTINGS = {
    'PERIMETER_SERVICE': 'https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/USA_Wildfires_v1/FeatureServer/1',
    'PERIMETER_ID_FIELD': 'GeometryID',
    'PERIMETER_IRWIN_FIELD': 'IRWINID',
    'IRWIN_SERVICE': 'https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/USA_Wildfires_v1/FeatureServer/0',
    'IRWIN_ID_FIELD': 'IrwinID',
    # 'BOUNDARIES_SERVICE': 'https://gispub.epa.gov/arcgis/rest/services/Region9/Boundaries_R9Administrative/MapServer/29',
    'BOUNDARIES_SERVICE': 'https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_States_Generalized/FeatureServer/0',
    'COUNTY_SERVICE': 'https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Counties_Generalized/FeatureServer/0',
    # 'BUFFERED_PERIMETER_SERVICE': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/R9_Fire_Perimeter_Buffers/FeatureServer/0',
    # 'COP_LAYERS': 'USA_Wildfires_v1_3262;USA_Wildfires_v1_5448;PotentialPollutantAndSpillSources_6033;PotentialPollutantAndSpillSources_6033_14;PotentialPollutantAndSpillSources_6033_44;PotentialPollutantAndSpillSources_6033_62;PotentialPollutantAndSpillSources_6033_59;PotentialPollutantAndSpillSources_6033_58;PotentialPollutantAndSpillSources_6033_57;PotentialPollutantAndSpillSources_6033_19;PotentialPollutantAndSpillSources_6033_152;ER1702727_SafeDrinkingWater_9569;ER1702727_SafeDrinkingWater_9569_0;NationalPriorityListBoundaryTypes_R9_2020_R9_6264;ActiveSitesResponseepagov_2512;ActiveSitesResponseepagov_2512_0',
    # 'NOTIFIABLE_FEATURES': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/R9NotifiableFeatures/FeatureServer/0',
    'NOTIFIABLE_FEATURES': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/R9Notifiable/FeatureServer/0',
    # 'NOTEBOOK_ID': 'b9f4201a65ae44c2a3878cb563513234',
    'FIRE_CONFIG_ID': '7c7e8175-1aab-4092-9091-99af45148ab7',
    'TASK_TABLE_ID': '21b721732c3d4cf2bb1a0fe5fc4863eb',
    'CUSTOM_POI': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/R9NotificationCustomPoints/FeatureServer/0',
    'TRIBAL_LANDS': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/Tribal_Lands_R9_2020_BIA_BLM_EPA_Public_Layer_View/FeatureServer/0',
    'REPORT_TEMPLATE_ID': '6522d1d6db994710918200948cddca0a',
    'FACILITY_LAYERS': [
        # RMP
        {'name': 'Active RMP Facilities',
         'url': 'https://utility.arcgis.com/usrsvcs/servers/a9dda0a4ba0a433992ce3bdffd89d35a/rest/services/SharedServices/RMPFacilities/MapServer/0',
         'update_date': '03/01/2021',
         'sheet_index': 1},
        # CA TierII
        {'name': 'CA Tier II',
         'url': 'https://utility.arcgis.com/usrsvcs/servers/f7e36ad5c73f4a19a24877d920a27c0a/rest/services/EPA_EPCRA/TierIIFacilities/MapServer/0',
         'update_date': '2017',
         'sheet_index': 3},
        #             # SDWIS
        #             {'name': 'Safe_Drinking_Water_(SDWIS)_Region_9_V1',
        #             'url': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/SDWIS_Base/FeatureServer/0',
        #             'update_date': '2018'},
        # NPDES Wastewater
        {'name': 'NPDES Wastewater',
         'url': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/FRS_INTERESTS_NPDES/FeatureServer/0',
         'update_date': '2012',
         'sheet_index': 5},
        # NPL Points
        # if this name changes, adjust npl point poly edge case below!
        {'name': 'NationalPriorityListPoint_R9_2019_R9',
         'url': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/R9_National_Priority_List_Points/FeatureServer/0',
         'update_date': '2019',
         'sheet_index': 7},
        # NPL Polygons
        {'name': 'NationalPriorityListBoundaryTypes_R9_2020_R9',
         'url': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/R9_NPL_Site_Boundaries/FeatureServer/0',
         'update_date': '2019',
         'sheet_index': 9},
        # FRP
        {'name': 'FRP Facilities',
         'url': 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/Facility_Response_Plan_Sites_Region_9_V1_D/FeatureServer/0',
         'update_date': '2019',
         'sheet_index': 11},
    ]
}


# def main(days=1):
@retry(stop=stop_after_attempt(2), after=after_log(get_logger(), logging.DEBUG))
def main():
    try:
        # config/setup
        gis = GIS('home')
        FIRE_REPORT_SETTINGS['TOKEN'] = token = gis._con.token
        url = "https://hooks.slack.com/services/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"
        webhook = WebhookClient(url)
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        ####################################################################################################################
        notifiable_fires_query = f"NotificationConfigurationID = '{FIRE_REPORT_SETTINGS['FIRE_CONFIG_ID']}'"
        fire_features = load_features_json(url=FIRE_REPORT_SETTINGS['NOTIFIABLE_FEATURES'],
                                           where=notifiable_fires_query,
                                           auth_token=token)
        for f in fire_features:
            f['attributes']['Data'] = json.loads(f['attributes']['Data'])
        # get R9 CONUS boundary
        conus_where = "STATE_ABBR='CA' OR STATE_ABBR='AZ' OR STATE_ABBR='NV'"
        r9_features = load_features_json(FIRE_REPORT_SETTINGS['BOUNDARIES_SERVICE'], where=conus_where)
        irwin_where = "IncidentTypeCategory = 'WF'"
        irwin_incidents = [item for feat in r9_features for item in
                           get_irwin_info(FIRE_REPORT_SETTINGS['IRWIN_SERVICE'], where_statement=irwin_where, geometry_filter=feat['geometry'])]
        perimeter_incidents = [item for feat in r9_features for item in
                               get_perimeters(FIRE_REPORT_SETTINGS['PERIMETER_SERVICE'], geometry=feat['geometry'], calc_centroids=True)]
        # update existing
        update_unarchived_fires(irwin_incidents, perimeter_incidents, FIRE_REPORT_SETTINGS, force_update=True)
        update_custom_poi(token=token, config_settings=FIRE_REPORT_SETTINGS)

        # get fires we know about and notified already
        known_irwin_ids = [x['attributes'].get('Data').get('IRWINID') for x in fire_features if
                           x['attributes'].get('Data', None).get('IRWINID', None) is not None]
        known_perimeter_ids = [x['attributes'].get('Data').get('perimeter_id') for x in fire_features if
                               x['attributes'].get('Data').get('perimeter_id', None) is not None]
        ################################################################################################################
        new_incidents = []
        # prevent duplicate irwin points and just get most recently modified
        for x in irwin_incidents:
            if x['attributes']['IrwinID'] not in known_irwin_ids and \
                not any(y for y in new_incidents if y['IRWINID'] == x['attributes']['IrwinID']):
                new_incidents.append({'IncidentName': x['attributes']['IncidentName'].upper(),
                                      'IRWINID': x['attributes']['IrwinID'],
                                      'reported_date': str(dt.fromtimestamp(
                                          x['attributes']['FireDiscoveryDateTime'] / 1000)),
                                      'percent_contained': x['attributes']['PercentContained'],
                                      'acres': x['attributes']['DailyAcres']
                                      })

        # get perimeters for irwin incidents and update new incident record with perimeter ID
        perimeters = []
        incidents_with_irwinid = [i['IRWINID'] for i in new_incidents if i.get('IRWINID', False)]
        if len(incidents_with_irwinid) > 0:
            matching_perims = [p for p in perimeter_incidents if p['attributes']['IRWINID'] in incidents_with_irwinid]
            for p in matching_perims:
                index = \
                    [i for i, x in enumerate(new_incidents) if
                     f"{x.get('IRWINID').upper()}" == p.get('attributes').get('IRWINID').upper()][
                        0]
                new_incidents[index]['perimeter_id'] = p['attributes']['GeometryID']
                # capture acres if irwin DailyAcres is null
                if new_incidents[index]['acres'] is None:
                    new_incidents[index]['acres'] = p['attributes']['GISAcres']

        perims_missing_irwin = [p for p in perimeter_incidents if p['attributes'].get('IRWINID') is None]
        perimeters += perims_missing_irwin

        # merge new_indcidents and perimeters
        new_incidents += [{'IncidentName': p['attributes']['IncidentName'].upper(),
                           'perimeter_id': p['attributes']['GeometryID'],
                           'reported_date': str(dt.fromtimestamp(p['attributes']['CreateDate'] / 1000)),
                           # '_geometry': json.dumps(p['geometry']),
                           'geometry': p.get('geometry'),
                           'acres': p['attributes']['GISAcres']} for p in perimeters
                          if p['attributes']['GeometryID'] not in known_perimeter_ids]
        ######################################################################################################################
        # log newly found fires
        for incident in new_incidents:
            if incident.get('acres', None) is None or incident.get('acres', 0) < 10:
                continue
            incident_irwin = incident.get('IRWINID', None)
            incident_perim = incident.get('perimeter_id', None)
            # fire report and intersects:
            incident_results, incident_report = generate_fire_report(incident_irwin, incident_perim,
                                                                     FIRE_REPORT_SETTINGS['FACILITY_LAYERS'])
            # create new feature
            feat = Feature(attributes={})
            feat.geometry = incident_results.get('feature_geometry')
            del incident_results['feature_geometry']
            feat.attributes['Name'] = incident.get('IncidentName').upper()
            feat.attributes['Retrieved'] = incident_results['RETRIEVED']
            incident['current_results'] = incident_results
            incident['counties'] = get_counties(feat.geometry)
            incident['tribes'] = get_tribes(feat.geometry)
            feat.attributes['Data'] = json.dumps(incident)
            feat.attributes['Display'] = display_fire(feat)
            feat.attributes['NotificationConfigurationID'] = FIRE_REPORT_SETTINGS['FIRE_CONFIG_ID']
            created_ft = update_feature(feat, target_url=FIRE_REPORT_SETTINGS['NOTIFIABLE_FEATURES'],
                                        attachment=incident_report)
            print(f'Created {feat.attributes["Name"]} feature')
            print(created_ft)
        print('main done')
        # response = webhook.send(text="R9 Fire Notifications Notebook Run: SUCCESS")
        return
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_msg = ", ".join([str(exc_type), str(fname), str(exc_tb.tb_lineno)])
        print(error_msg)
        response = webhook.send(text="R9 Fire Notifications Notebook Run: FAILED")
        response = webhook.send(text=error_msg)
        raise Exception(e)


# %%
main()

# generate_fire_report(None, "{A6EC388F-A752-4A23-9721-62E8DF4F3BEE}") # coldwater perimeter
# generate_fire_report(None, "{BD4DF34B-1CD1-4816-AF97-19998B5848CB}") # mccash perimeter
# update_custom_poi(token)
# update_unarchived_fires()
