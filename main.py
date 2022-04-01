import pandas as pd 
import json, requests, urllib.parse
from datetime import datetime, timezone
import apiHelpers

# API Token & Player/Clan Tags
API_KEY = 'API_KEY'
player_tag = '#PLAYER_TAG'
clan_tag = '#CLAN_TAG'


# API Headers: Generally
headers = {
    'authorization' : 'Bearer '+API_KEY,
    'Accept'        : 'application/json'
}


############################################################################################
### Dimensions #############################################################################
############################################################################################

### Get Player Labels (Reference Data) ###
playerLabels_df = apiHelpers.getPlayerLabels(headers, overwrite_pkl=0)

### Get Clan Labels (Reference Data) ###
clanLabels_df = apiHelpers.getClanLabels(headers, overwrite_pkl=0)

### Get Leauges (Reference Data) ###
leauges_df = apiHelpers.getLeauges(headers, overwrite_pkl=0)

### Get War Leauges (Reference Data) ###
warLeauges_df = apiHelpers.getWarLeauges(headers, overwrite_pkl=0)

### Get Goldpass Current Season (Reference Data) ###
currentGoldpassSeason_df = apiHelpers.getCurrentGoldpassSeason(headers, overwrite_pkl=0)

### Get All Locations Globally (Reference Data) ###
locations_df = apiHelpers.getLocations(headers, overwrite_pkl=0)


##########################################################################################
### Facts ################################################################################
##########################################################################################

# Get Single Clan
sinfleClan_df = apiHelpers.getSingleClan(headers, clan_tag, overwrite_pkl=0)

# Get Single Clan's Members
singleClansMembers_df = apiHelpers.getSingleClanMembers(headers, clan_tag, overwrite_pkl=0)

# Get Single Clan's WarLog
singleClanWarLog_df = apiHelpers.getSingleClanWarLog(headers, clan_tag, overwrite_pkl=0)

# Get Single Clan's Current War
# Working on improvements:
#   - Needs Storage Methodology (pkl)
#   - May Need Clan Tag Column  
singleClanCurrentWar_df =  apiHelpers.getSingleClanCurrentWar(headers, clan_tag)

# Get Single Player's Info
player_df, playerAchievements_df, playerTroops_df, playerHeroes_df, playerSpells_df =  apiHelpers.getSinglePlayer(headers, player_tag, overwrite_pkl=0):

### Loop through all locations across the globe, Get Clan Rankings for all Countries  ###
globalClanRankings_df =  apiHelpers.getGlobalClanRankings(headers, overwrite_pkl=0)

### Loop through all locations across the globe, Get Player Rankings for all Countries  ###
globalPlayerRankings_df =  apiHelpers.getGlobalPlayerRankings(headers, overwrite_pkl=0)

### Loop through all locations across the globe, Get Clan Versus Rankings for all Countries  ###
globalClanVesusRankings_df =  apiHelpers.getGlobalClanVersusRankings(headers, overwrite_pkl=0)

### Loop through all locations across the globe, Get Player Versus Rankings for all Countries  ###
globalPlayerVersusRankings_df =  apiHelpers.getGlobalPlayerVersusRankings(headers, overwrite_pkl=0)

# Get All Global Rankings
#   - Gives Option to refresh the Locations pkl first incase new countries/locations get added over time
#   - Returns data Frames in this order:
#       - Clan Rankings, Player Rankings, Clan Versus Rankings, Player Versus Rankings
allGlobalRankings_df = apiHelpers.getAllGlobalRankings(headers, overwrite_pkl=0, refreshLocations=0)

############################################################################################################
### Gives you your clan member's details. You can plug this into tableau to find out who you should drop ###
### Saves as xlsx and pkl files locally. Load these into the tableau workbook ##############################
############################################################################################################
cln = apiHelpers.getSingleClan(headers, clan_tag=clan_tag)
cln_mem = apiHelpers.getSingleClanMembers(headers, clan_tag=clan_tag)
print(cln_mem)
p, pa, pt, ph, ps = pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([]), pd.DataFrame([])
for player_tag in cln_mem['tag']:
    print(player_tag)
    p_df, pa_df, pt_df, ph_df, ps_df = apiHelpers.getSinglePlayer(headers, player_tag=player_tag)
    p_df['player_tag'], pa_df['player_tag'], pt_df['player_tag'], ph_df['player_tag'], ps_df['player_tag'] = player_tag, player_tag, player_tag, player_tag, player_tag
    p, pa, pt, ph, ps = pd.concat([p, p_df]), pd.concat([pa, pa_df]), pd.concat([pt, pt_df]), pd.concat([ph, ph_df]), pd.concat([ps, ps_df])
pa_pvt = pa.reset_index().pivot_table(index='player_tag', columns='name', values='value')
pa_pvt = pa_pvt[['Gold Grab', 'Elixir Escapade', 'Heroic Heist', 'Unbreakable', 'Conqueror', 'Humiliator', 'Not So Easy This Time', 'Sweet Victory!', 'Un-Build It', 'Champion Builder', 'War Hero', 'Clan War Wealth', 'War League Legend', 'Well Seasoned', 'Games Champion', 'Friend in Need', 'Sharing is caring', 'Siege Sharer']]
clan_playervalue = p.merge(pa_pvt, left_on='player_tag', right_on='player_tag', how='left')
clan_playervalue.to_excel('clan_playervalue.xlsx')
clan_playervalue.to_pickle('pickles\clan_playervalue.pkl')


#####################################################################################################################################################
#### *!*!*!*    DO NOT RUN THIS UNLESS YOU MEET THE REQUIREMENTS BELOW OR IT"LL BE A WASTE OF TIME    *!*!*!* #######################################
#### *!*!*!*    This requires >2gb of RAM, >2gb of Storage, and Runs for 18-24 hours                  *!*!*!* #######################################
#### *!*!*!*    This prints info in your console, showing progress and current tag for debugging      *!*!*!* #######################################
#####################################################################################################################################################
### Gather All distinct, non-null clans from clan list, your war log, and global clan versus, clan rankings, player versus, and player rankings
### Loop through All Clan dataframe, pull clan info and all member info    
### Save all clan info & member info to pkl files
#AllGlobalClansAndMembers_df =  apiHelpers.getAllGlobalClansAndClanMembers(headers, overwrite_pkl=1, refreshGlobalRankings=0)





##########################################################################################################################
### Future Work ##########################################################################################################
##########################################################################################################################

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



