import pandas as pd 
import json, requests, urllib.parse
from datetime import datetime, timezone

###########################################################################################################
### API Helpers/Normalizers ###############################################################################
###########################################################################################################

### Encode URL: '#' --> '%23'
def urlEncode(tag):
    return urllib.parse.quote(tag)

# Standard Clash of Clans API Call returning a df notmalized to a get_type ("items", "members", etc.)
def apiWithGetType(headers, api_url, get_type):
    request_response = requests.get(api_url, headers=headers)
    json_data = json.loads(request_response.text)
    # print(json_data)
    if not get_type in json_data or len(json_data[get_type]) ==0:
        return [] 
    return pd.json_normalize(json_data, get_type)

###########################################################################################################
### All API Interactions Below ############################################################################
###########################################################################################################

##################
### Dimensions ###
##################

### Get Player Labels (Reference Data) ###
def getPlayerLabels(headers, overwrite_pkl=0):
    # Player Labels
    api_url = 'https://api.clashofclans.com/v1/labels/players'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\player_labels.pkl')
    return df

### Get Clan Labels (Reference Data) ###
def getClanLabels(headers, overwrite_pkl=0):
    # Clan Labels
    api_url = 'https://api.clashofclans.com/v1/labels/clans'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\clan_labels.pkl')
    return df

### Get Leauges (Reference Data) ###
def getLeauges(headers, overwrite_pkl=0):
    # Leauges
    api_url = 'https://api.clashofclans.com/v1/leagues'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\leauges.pkl')
    return df

### Get War Leauges (Reference Data) ###
def getWarLeauges(headers, overwrite_pkl=0):
    api_url = 'https://api.clashofclans.com/v1/warleagues'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\war_leauges.pkl')
    return df

### Get Goldpass Current Season (Reference Data) ###
def getCurrentGoldpassSeason(headers, overwrite_pkl=0):
    api_url = 'https://api.clashofclans.com/v1/goldpass/seasons/current'
    get_type = 'items'
    request_response = requests.get(api_url, headers=headers)
    json_data = json.loads(request_response.text)
    df = pd.json_normalize(json_data) ## No need to normalize to a nest name
    if overwrite_pkl == 1:
        df.to_pickle('pickles\goldpass_season_current.pkl')
    return df

### Get All Locations Globally (Reference Data) ###
def getLocations(headers, overwrite_pkl=0):
    api_url = 'https://api.clashofclans.com/v1/locations'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\locations.pkl')
    return df


#############
### Facts ###
#############

# Get Single Clan
def getSingleClan(headers, clan_tag, overwrite_pkl=0):
    clan_tag = urlEncode(clan_tag)
    api_url = 'https://api.clashofclans.com/v1/clans/' + clan_tag 
    request_response = requests.get(api_url, headers=headers)
    json_data = json.loads(request_response.text)
    df = pd.json_normalize(json_data)
    df['data_collection_time_utc'], df['data_collection_time_local'], df['data_collection_time_local_tz'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\clans.pkl')
    return df

# Get Single Clan's Members
def getSingleClanMembers(headers, clan_tag, overwrite_pkl=0):
    # Clan Members
    clan_tag = urlEncode(clan_tag)
    api_url = 'https://api.clashofclans.com/v1/clans/' + clan_tag + '/members'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\clan_members.pkl')
    return df

# Get Single Clan's WarLog
def getSingleClanWarLog(headers, clan_tag, overwrite_pkl=0):
    # Clan Warlog
    clan_tag = urlEncode(clan_tag)
    api_url = 'https://api.clashofclans.com/v1/clans/' + clan_tag + '/warlog'
    get_type = 'items'
    df = apiWithGetType(headers, api_url, get_type)
    print(df)
    if overwrite_pkl == 1:
        df.to_pickle('pickles\warLog.pkl')
    return df

# Get Single Clan's Current War
# Working on improvements:
#   - Needs Storage Methodology (pkl)
#   - May Need Clan Tag Column  
def getSingleClanCurrentWar(headers, clan_tag): #overwrite_pkl = 0):
    clan_tag = urlEncode(clan_tag)
    api_url = 'https://api.clashofclans.com/v1/clans/' + clan_tag + '/currentwar'
    request_response = requests.get(api_url, headers=headers)
    json_data = json.loads(request_response.text)
    # statuses: 'warEnded', 'notInWar', 'preparation'
    #if overwrite_pkl == 1:
        #df.to_pickle('pickles\clan_war_detail.pkl')
    df = pd.json_normalize(json_data)
    return df

# Get Single Player's Info
def getSinglePlayer(headers, player_tag, overwrite_pkl=0):
    player_tag = urlEncode(player_tag)
    # player_tag_dec = urlEncode(player_tag) 

    # Player
    api_url = 'https://api.clashofclans.com/v1/players/' + player_tag#player_tag_dec
    request_response = requests.get(api_url, headers=headers)
    json_data = json.loads(request_response.text)
    p_df = pd.json_normalize(json_data)
    p_df['data_collection_time_utc'], p_df['data_collection_time_local'], p_df['data_collection_time_local_tz'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
    # Player Achievements
    get_type = 'achievements'
    pa_df = pd.json_normalize(json_data, get_type)
    pa_df['player_tag'], pa_df['data_collection_time_utc'], pa_df['data_collection_time_local'], pa_df['data_collection_time_local_tz'] = player_tag, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
    # Player Troops
    get_type = 'troops'
    pt_df = pd.json_normalize(json_data, get_type)
    pt_df['player_tag'], pt_df['data_collection_time_utc'], pt_df['data_collection_time_local'], pt_df['data_collection_time_local_tz'] = player_tag, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
    # Player Heros
    get_type = 'heroes'
    ph_df = pd.json_normalize(json_data, get_type)
    ph_df['player_tag'], ph_df['data_collection_time_utc'], ph_df['data_collection_time_local'], ph_df['data_collection_time_local_tz'] = player_tag, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
    # Player Spells
    get_type = 'spells'
    ps_df = pd.json_normalize(json_data, get_type)
    ps_df['player_tag'], ps_df['data_collection_time_utc'], ps_df['data_collection_time_local'], ps_df['data_collection_time_local_tz'] = player_tag, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
    if overwrite_pkl == 1:
        p_df.to_pickle('pickles\players.pkl')
        pa_df.to_pickle('pickles\players_achievements.pkl')
        pt_df.to_pickle('pickles\players_troops.pkl')
        ph_df.to_pickle('pickles\players_heroes.pkl')
        ps_df.to_pickle('pickles\players_spells.pkl')
    return p_df, pa_df, pt_df, ph_df, ps_df


### Loop through all locations across the globe, Get Clan Rankings for all Countries  ###
def getGlobalClanRankings(headers, overwrite_pkl=0):
    ### Loop through locations and get rankings
    loc_df = pd.read_pickle('pickles\locations.pkl')
    loc_df[loc_df['countryCode'].notna()]
    loc_df = loc_df['id'].apply(str)
    get_type = 'items'
    cr_df = pd.DataFrame([])
    for location in loc_df:
        # Clan Rankings
        api_url = 'https://api.clashofclans.com/v1/locations/' + location + '/rankings/clans'
        cr = apiWithGetType(headers, api_url, get_type)
        if not isinstance(cr, list):
            cr['data_collection_time_utc'], cr['data_collection_time_local'], cr['data_collection_time_local_tz'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
            cr_df = pd.concat([cr, cr_df])
    if overwrite_pkl == 1:
        cr_df.to_pickle('pickles\clan_rankings.pkl')
    return cr_df

### Loop through all locations across the globe, Get Player Rankings for all Countries  ###
def getGlobalPlayerRankings(headers, overwrite_pkl=0):
    ### Loop through locations and get rankings
    loc_df = pd.read_pickle('pickles\locations.pkl')
    loc_df[loc_df['countryCode'].notna()]
    loc_df = loc_df['id'].apply(str)
    get_type = 'items'
    pr_df = pd.DataFrame([])
    for location in loc_df:
        # Player Rankings
        api_url = 'https://api.clashofclans.com/v1/locations/' + location + '/rankings/players'
        pr = apiWithGetType(headers, api_url, get_type)
        if not isinstance(pr, list):
            pr['location.id'], pr['data_collection_time_utc'], pr['data_collection_time_local'], pr['data_collection_time_local_tz'] = location, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
            pr_df = pd.concat([pr, pr_df])
    if overwrite_pkl == 1:
        pr_df.to_pickle('pickles\player_rankings.pkl')
    return pr_df

### Loop through all locations across the globe, Get Clan Versus Rankings for all Countries  ###
def getGlobalClanVersusRankings(headers, overwrite_pkl=0):
    ### Loop through locations and get rankings
    loc_df = pd.read_pickle('pickles\locations.pkl')
    loc_df[loc_df['countryCode'].notna()]
    loc_df = loc_df['id'].apply(str)
    get_type = 'items'
    cv_df = pd.DataFrame([])
    for location in loc_df:
        # Clan Versus Rankings
        api_url = 'https://api.clashofclans.com/v1/locations/' + location + '/rankings/clans-versus'
        cv = apiWithGetType(headers, api_url, get_type)
        if not isinstance(cv, list):
            cv['data_collection_time_utc'], cv['data_collection_time_local'], cv['data_collection_time_local_tz'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
            cv_df = pd.concat([cv, cv_df])
    if overwrite_pkl == 1:
        cv_df.to_pickle('pickles\clanversus_rankings.pkl')
    return cv_df

### Loop through all locations across the globe, Get Player Versus Rankings for all Countries  ###
def getGlobalPlayerVersusRankings(headers, overwrite_pkl=0):
    ### Loop through locations and get rankings
    loc_df = pd.read_pickle('pickles\locations.pkl')
    loc_df[loc_df['countryCode'].notna()]
    loc_df = loc_df['id'].apply(str)
    get_type = 'items'
    pvr_df = pd.DataFrame([])
    for location in loc_df:
        # Players Versus Rankings
        api_url = 'https://api.clashofclans.com/v1/locations/' + location + '/rankings/players-versus'
        pvr = apiWithGetType(headers, api_url, get_type)
        if not isinstance(pvr, list):
            pvr['location.id'], pvr['data_collection_time_utc'], pvr['data_collection_time_local'], pvr['data_collection_time_local_tz'] = location, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().astimezone().tzinfo)
            pvr_df = pd.concat([pvr, pvr_df])
    if overwrite_pkl == 1:
        pvr_df.to_pickle('pickles\playerversus_rankings.pkl')
    return pvr_df

# Get All Global Rankings
#   - Gives Option to refresh the Locations pkl first incase new countries/locations get added over time
#   - Returns data Frames in this order:
#       - Clan Rankings, Player Rankings, Clan Versus Rankings, Player Versus Rankings
def getAllGlobalRankings(headers, overwrite_pkl=0, refreshLocations=0):
    if refreshLocations == 1:
        getLocations(headers, overwrite_pkl=1)
    return getGlobalClanRankings(headers, overwrite_pkl=overwrite_pkl), getGlobalPlayerRankings(headers, overwrite_pkl=overwrite_pkl), getGlobalClanVersusRankings(headers, overwrite_pkl=overwrite_pkl), getGlobalPlayerVersusRankings(headers, overwrite_pkl=overwrite_pkl)

#####################################################################################################################################################
#### *!*!*!*    DO NOT RUN THIS UNLESS YOU MEET THE REQUIREMENTS BELOW OR IT"LL BE A WASTE OF TIME    *!*!*!* #######################################
#### *!*!*!*    This requires >2gb of RAM, >2gb of Storage, and Runs for 18-24 hours                  *!*!*!* #######################################
#### *!*!*!*    This prints info in your console, showing progress and current tag for debugging      *!*!*!* #######################################
#####################################################################################################################################################
### WARNING: OVERWRITE DEFAULTED TO TRUE
###     This takes >18 hours to run, you'll be angry if it doesn't save your results
### Gather All distinct, non-null clans from clan list, your war log, and global clan versus, clan rankings, player versus, and player rankings
### Loop through All Clan dataframe, pull clan info and all member info    
### Save all clan info & member info to pkl files
### NEED TO OPTIMIZE FOR SPACE? But want to refreshGlobalRankings & refreshLocations?
###     Run each function in succession with overwrites on, but refreshes off (shown below)
###         getLocations(headers, overwrite_pkl=1)
###         getAllGlobalRankings(headers, overwrite_pkl=1, refreshLocations=0)
###         getAllGlobalClansAndClanMembers(headers, overwrite_pkl=1, refreshGlobalRankings=0)
def getAllGlobalClansAndClanMembers(headers, overwrite_pkl=1, refreshGlobalRankings=0):
    if refreshGlobalRankings ==1:
        cr, pr, cvr, pvr = getAllGlobalRankings(headers, overwrite_pkl=1, refreshLocations=1)
        cln = pd.concat([pd.read_pickle('pickles\clans.pkl')['tag'], pd.read_pickle('pickles\warLog.pkl')['opponent.tag'], pvr['clan.tag'], pr['clan.tag'], cvr['tag'], cr['tag']]).drop_duplicates().dropna()
    else:
        cln = pd.concat([pd.read_pickle('pickles\clans.pkl')['tag'], pd.read_pickle('pickles\warLog.pkl')['opponent.tag'], pd.read_pickle('pickles\playerversus_rankings.pkl')['clan.tag'], pd.read_pickle('pickles\player_rankings.pkl')['clan.tag'], pd.read_pickle('pickles\clanversus_rankings.pkl')['tag'], pd.read_pickle('pickles\clan_rankings.pkl')['tag']]).drop_duplicates().dropna()
    c_df, cm_df, cnt, tot = pd.DataFrame([]), pd.DataFrame([]), 0, len(cln)
    for clan_tag in cln:
        print("{0:.0%}".format(cnt/tot) + ' Complete | Call ' + str(cnt) + ' of ' + str(tot) + " | Clan Tag: " + clan_tag)
        cnt += 1
        # Clans
        c = getSingleClan(headers, clan_tag)
        if not isinstance(c, list):
            c_df = pd.concat([c, c_df])
        # Clan Members
        cm = getSingleClanMembers(headers, clan_tag)
        if not isinstance(cm, list):
            cm['clan_tag'] = clan_tag
            cm_df = pd.concat([cm, cm_df])
    if overwrite_pkl == 1:
        c_df.to_pickle('pickles\clans.pkl')
        cm_df.to_pickle('pickles\clan_members.pkl')
    return c_df, cm_df



####################################
### Need to Make a Player Looper ###
####################################
### Would Loop Through List of players & concat their player info, achievements, troops, heroes, and spells to a list
### Would have the option to overwrite the original player-related pickles
### Would be nice to have Upsert Function to update/insert player info to the curent pickle list

########################################
### Need to Add a WarHelper Function ###
########################################
### Would Look at current war
### If you are in 'Prepare', or "War" status, look at other player's

############################################
### Need to add Leauge War Functionality ###
############################################
### Before defining this functionality, need to get into a clan leauge war and see the API json responses. 
### See what data we get, how can we use this to derive valuable info