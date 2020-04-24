import requests
import json


def peers(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
            # PEER COMPARISON WITH INFO(52 wk high-low with dates,Revenue,PAT,Equity,Shareholdings) 
            # RATIOS(OPM,NPM,RONW,EPS,CEPS,PE)
            baseurl7 = "https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode="+str(script_code)+"&scripcomare="
            data7 = requests.get(baseurl7)
            peer_comp = data7.json()
            if peer_comp['Table'][0]['scrip_cd'] == None:
                peer_comp = {'info' : 'incorrect script_code'}
            return peer_comp
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg