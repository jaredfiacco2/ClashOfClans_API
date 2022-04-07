
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from datetime import datetime, timezone
import apiHelpers

# Get Single Clan
def getSingleClan(event, context):
    #Credentials for BigQuery Access
    credentials_path = 'gcp-service-account-auth-key.json'
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    project_id = "PROJECT_ID"
    # API Token & Player/Clan Tags
    API_KEY = 'API_KEY'
    clan_tag = 'CLAN_TAG'
    # API Headers: Generally
    headers = {
        'authorization' : 'Bearer '+API_KEY,
        'Accept'        : 'application/json'
    }
    #Get Context to get event_id - will be used as load ID in BigQuery
    c = str(context)
    event_id = c[c.find('event_id: ')+len('event_id: '):c.rfind(', timestamp:')]
    cln_mem = apiHelpers.getSingleClanMembers(headers, clan_tag=clan_tag)
    p, pa, pt, ph, ps = pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])
    for player_tag in cln_mem['tag']:
        print(player_tag)
        p_df, pa_df, pt_df, ph_df, ps_df = apiHelpers.getSinglePlayer(headers, player_tag=player_tag)
        p_df['player_tag'], pa_df['player_tag'], pt_df['player_tag'], ph_df['player_tag'], ps_df['player_tag'] = player_tag, player_tag, player_tag, player_tag, player_tag
        p, pa, pt, ph, ps = pd.concat([p, p_df]), pd.concat([pa, pa_df]), pd.concat([pt, pt_df]), pd.concat([ph, ph_df]), pd.concat([ps, ps_df])
    #players
    p['data_collection_time_utc'], p['data_collection_time_local'], p['data_collection_time_local_tz'], p['event_id'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo), event_id 
    p.columns = [c.replace(".", "_") for c in list(p.columns)]
    p = p.drop(columns = ['achievements', 'labels', 'troops', 'heroes', 'spells'])
    pandas_gbq.to_gbq(p, 'my_current_clan_stats.players', project_id=project_id, credentials=credentials, if_exists='append')
    #player achievements
    pa = pa.reset_index().pivot_table(index='player_tag', columns='name', values='value')
    pa['event_id'] = event_id
    pa.columns = [c.replace(".", "_").replace("&", "and").replace("!", "").replace(" ", "_").replace("-", "_") for c in list(pa.columns)]
    pa = pa.reset_index(level=0)
    pandas_gbq.to_gbq(pa, 'my_current_clan_stats.player-achievements', project_id=project_id, credentials=credentials, if_exists='append')
    #player troops
    pt = pt.reset_index().pivot_table(index='player_tag', columns='name', values='level')
    pt['event_id'] = event_id
    pt.columns = [c.replace(".", "").replace(" ", "_") for c in list(pt.columns)]
    pt = pt.reset_index(level=0)
    pandas_gbq.to_gbq(pt, 'my_current_clan_stats.player-troops', project_id=project_id, credentials=credentials, if_exists='append')
    #player heroes
    ph = ph.reset_index().pivot_table(index='player_tag', columns='name', values='level')
    ph['event_id'] = event_id
    ph.columns = [c.replace(" ", "_") for c in list(ph.columns)]
    ph = ph.reset_index(level=0)
    pandas_gbq.to_gbq(ph, 'my_current_clan_stats.player-heroes', project_id=project_id, credentials=credentials, if_exists='append')
    #player spells
    ps = ps.reset_index().pivot_table(index='player_tag', columns='name', values='level')
    ps['event_id'] = event_id
    ps.columns = [c.replace(" ", "_") for c in list(ps.columns)]
    ps = ps.reset_index(level=0)
    pandas_gbq.to_gbq(ps, 'my_current_clan_stats.player-spells', project_id=project_id, credentials=credentials, if_exists='append')
